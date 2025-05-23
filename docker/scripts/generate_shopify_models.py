import json
import os
import re
from pathlib import Path

import requests
from graphql import get_introspection_query, build_client_schema, print_schema, IntrospectionQuery

from ariadne_codegen.main import client as codegen_client

ADDONS_PATH = Path("/opt/project/addons/product_connect")


def fetch_shopify_introspection(endpoint: str, token: str) -> dict[str, dict[str, str]]:
    introspection_query = get_introspection_query()
    headers = {
        "Content-Type": "application/json",
        "X-Shopify-Access-Token": token,
    }
    print(f"Fetching introspection schema from {endpoint}...")
    response = requests.post(endpoint, json={"query": introspection_query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching schema: {response.status_code} {response.text}")
    result = response.json()
    if "data" not in result:
        raise Exception(f"Invalid introspection result: {result}")
    return result["data"]


def save_introspection_json(data: dict[str, dict[str, str]], file_path: Path) -> None:
    file_path.write_text(json.dumps(data, indent=2))
    print(f"Saved introspection JSON schema to {file_path}")


def save_schema_sdl(json_data: IntrospectionQuery, output_file_path: Path) -> None:
    schema = build_client_schema(json_data)
    sdl = print_schema(schema)
    sdl = re.sub(r'""".*?"""', '""', sdl, flags=re.DOTALL)
    output_file_path.write_text(sdl)


def main() -> None:
    shopify_store_key = os.getenv("SHOPIFY_STORE_URL_KEY")
    shopify_api_token = os.getenv("SHOPIFY_API_TOKEN")
    shopify_api_version = os.getenv("SHOPIFY_API_VERSION")
    required_env_vars = ["SHOPIFY_STORE_URL_KEY", "SHOPIFY_API_TOKEN", "SHOPIFY_API_VERSION"]

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing_vars)}")

    addon_path = Path(ADDONS_PATH)
    queries_path = addon_path / "graphql" / "shopify"
    schema_path = addon_path / "graphql" / "schema"
    schema_path.mkdir(parents=True, exist_ok=True)
    introspection_file_path = schema_path / f"shopify_schema_{shopify_api_version}.json"
    sdl_file_path = schema_path / f"shopify_schema_{shopify_api_version}.sdl"
    services_path = addon_path / "services" / "shopify"
    client_name = "gql"

    endpoint = f"https://{shopify_store_key}.myshopify.com/admin/api/{shopify_api_version}/graphql.json"
    print(f"Using Shopify endpoint: {endpoint}")

    if not introspection_file_path.exists():
        introspection_data = fetch_shopify_introspection(endpoint, shopify_api_token)
        save_introspection_json(introspection_data, introspection_file_path)
    else:
        introspection_data = json.loads(introspection_file_path.read_text())

    if not sdl_file_path.exists():
        save_schema_sdl(introspection_data, sdl_file_path)

    config_dict = {
        "schema_path": str(sdl_file_path),
        "queries_path": str(queries_path),
        "target_package_name": client_name,
        "target_package_path": str(services_path),
        "convert_to_snake_case": True,
        "async_client": False,
        "plugins": [
            "ariadne_codegen.contrib.shorter_results.ShorterResultsPlugin",
            "ariadne_codegen.contrib.extract_operations.ExtractOperationsPlugin",
        ],
        "scalars": {
            "DateTime": {
                "type": "datetime.datetime",
                "parse": "..helpers.parse_shopify_datetime_to_utc",
                "serialize": "..helpers.format_datetime_for_shopify",
            },
            "Date": {"type": "datetime.date"},
            "Money": {"type": "decimal.Decimal"},
            "Decimal": {"type": "decimal.Decimal"},
            "UnsignedInt64": {"type": "int"},
            "BigInt": {"type": "int"},
            "JSON": {"type": "str"},
            "URL": {"type": "pydantic.AnyUrl"},
            "HTML": {"type": "str"},
            "Color": {"type": "str"},
            "ARN": {"type": "str"},
            "UtcOffset": {"type": "datetime.timedelta"},
            "FormattedString": {"type": "str"},
        },
    }
    codegen_client({"tool": {"ariadne-codegen": config_dict}})

    print("\nGeneration complete.")
    print("You should now have a generated client package (e.g., 'shopify_client')")
    print("in the directory specified by 'target_package_path' as defined in the generated configuration.")


if __name__ == "__main__":
    main()
