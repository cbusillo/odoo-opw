#!/usr/bin/env python3
import logging
import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import psycopg2

from psycopg2 import sql
from psycopg2.extensions import connection
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class OdooRestorerError(Exception):
    pass


class OdooDatabaseUpdateError(OdooRestorerError):
    pass


class SqlCallType(Enum):
    UPDATE = "UPDATE"
    INSERT = "INSERT"
    DELETE = "DELETE"
    SELECT = "SELECT"


@dataclass
class KeyValuePair:
    key: str
    value: str | int | float | bool | None = None


@dataclass
class SqlCall:
    model: str
    data: KeyValuePair | None = None
    where: KeyValuePair | None = None


class LocalServerSettings(BaseSettings):
    # noinspection Pydantic
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
    host: str = Field(..., alias="ODOO_DB_HOST")
    port: int = Field(5432, alias="ODOO_DB_PORT")
    db_user: str = Field(..., alias="ODOO_DB_USER")
    db_password: SecretStr = Field(..., alias="ODOO_DB_PASSWORD")
    db_name: str = Field(..., alias="ODOO_DB_NAME")
    db_conn: connection | None = None
    filestore_path: Path = Field(..., alias="ODOO_FILESTORE_PATH")
    base_url: str = Field(None, alias="ODOO_BASE_URL")


class UpstreamServerSettings(BaseSettings):
    # noinspection Pydantic
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
    host: str = Field(..., alias="ODOO_UPSTREAM_HOST")
    user: str = Field(..., alias="ODOO_UPSTREAM_USER")
    db_name: str = Field(..., alias="ODOO_UPSTREAM_DB_NAME")
    db_user: str = Field(..., alias="ODOO_UPSTREAM_DB_USER")
    filestore_path: Path = Field(..., alias="ODOO_UPSTREAM_FILESTORE_PATH")


class ShopifySettings(BaseSettings):
    # noinspection Pydantic
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")
    shop_url_key: str = Field(..., alias="SHOPIFY_STORE_URL_KEY")
    api_token: SecretStr = Field(..., alias="SHOPIFY_API_TOKEN")
    api_version: str = Field(..., alias="SHOPIFY_API_VERSION")
    webhook_key: str = Field(..., alias="SHOPIFY_WEBHOOK_KEY")

    def validate_safe_environment(self) -> None:
        production_indicators = ["yps-your-part-supplier", "outboardpartswarehouse", "opw-prod", "production", "live"]

        shop_url_lower = self.shop_url_key.lower()
        for indicator in production_indicators:
            if indicator in shop_url_lower:
                raise OdooDatabaseUpdateError(
                    f"SAFETY CHECK FAILED: shop_url_key '{self.shop_url_key}' appears to be production. "
                    f"This script should only run on development/test environments. "
                    f"Found production indicator: '{indicator}'. Database will be dropped for safety."
                )


class OdooUpstreamRestorer:
    def __init__(self, local: LocalServerSettings, upstream: UpstreamServerSettings) -> None:
        self.local = local
        self.upstream = upstream
        self.os_env = os.environ.copy()
        self.os_env["PGPASSWORD"] = self.local.db_password.get_secret_value()

    def run_command(self, cmd: str) -> None:
        _logger.info(f"Running command: {cmd}")
        try:
            subprocess.run(cmd, shell=True, env=self.os_env, check=True)
        except subprocess.CalledProcessError as command_error:
            raise OdooRestorerError(f"Command failed: {cmd}\nError: {command_error}") from command_error

    def overwrite_filestore(self) -> subprocess.Popen:
        _logger.info("Overwriting filestore...")
        cmd = f"rsync -az --delete {self.upstream.user}@{self.upstream.host}:{self.upstream.filestore_path} {self.local.filestore_path}"
        return subprocess.Popen(cmd, shell=True, env=self.os_env)

    def overwrite_database(self) -> None:
        backup_path = "/tmp/upstream_db_backup.sql.gz"
        dump_cmd = (
            f"ssh {self.upstream.user}@{self.upstream.host} \"cd /tmp && sudo -u '{self.upstream.db_user}' "
            f"pg_dump -Fc '{self.upstream.db_name}'\" | gzip > {backup_path}"
        )
        self.run_command(dump_cmd)
        self.terminate_all_db_connections()
        self.run_command(f"dropdb --if-exists -h {self.local.host} -U {self.local.db_user} {self.local.db_name}")
        self.run_command(f"createdb -h {self.local.host} -U {self.local.db_user} {self.local.db_name}")
        restore_cmd = (
            f"gunzip < {backup_path} | pg_restore -d {self.local.db_name} -h {self.local.host} "
            f"-U {self.local.db_user} --no-owner --role={self.local.db_user}"
        )
        self.run_command(restore_cmd)
        self.run_command(f"rm {backup_path}")

    def connect_to_db(self) -> connection:
        if not self.local.db_conn:
            self.local.db_conn = psycopg2.connect(
                dbname=self.local.db_name,
                user=self.local.db_user,
                password=self.local.db_password.get_secret_value(),
                host=self.local.host,
                port=self.local.port,
            )
        return self.local.db_conn

    def terminate_all_db_connections(self) -> None:
        with psycopg2.connect(
            dbname="postgres",
            user=self.local.db_user,
            password=self.local.db_password.get_secret_value(),
            host=self.local.host,
            port=self.local.port,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='{self.local.db_name}' "
                    f"AND pid <> pg_backend_pid();"
                )
                conn.commit()
        _logger.info("All database connections terminated.")

    def call_odoo_sql(self, sql_call: SqlCall, call_type: SqlCallType) -> list[tuple] | None:
        self.connect_to_db()

        table = sql_call.model.replace(".", "_")
        if call_type == SqlCallType.UPDATE or call_type == SqlCallType.INSERT:
            if sql_call.data is None:
                raise ValueError("Data must be provided for UPDATE SQL call.")

            if sql_call.where:
                if sql_call.where.value is None:
                    raise ValueError("Value must be provided for WHERE clause.")

                query = sql.SQL(
                    "INSERT INTO {table} ({where_col}, {data_col}) "
                    "VALUES ({where_val}, {data_val}) "
                    "ON CONFLICT ({where_col}) DO UPDATE "
                    "SET {data_col} = EXCLUDED.{data_col}"
                ).format(
                    table=sql.Identifier(table),
                    where_col=sql.Identifier(sql_call.where.key),
                    data_col=sql.Identifier(sql_call.data.key),
                    where_val=sql.Literal(sql_call.where.value),
                    data_val=sql.Literal(sql_call.data.value),
                )
            else:
                query = sql.SQL("UPDATE {table} SET {key} = {value}").format(
                    table=sql.Identifier(table),
                    key=sql.Identifier(sql_call.data.key),
                    value=sql.Literal(sql_call.data.value),
                )
        elif call_type == SqlCallType.SELECT:
            if sql_call.data and sql_call.data.key:
                query = sql.SQL("SELECT {key} FROM {table}").format(
                    table=sql.Identifier(table),
                    key=sql.Identifier(sql_call.data.key),
                )
            else:
                query = sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table))
        else:
            raise ValueError(f"Unsupported SQL call type: {call_type}")

        if call_type == SqlCallType.SELECT and sql_call.where:
            if sql_call.where.value is None:
                raise ValueError("Value must be provided for WHERE clause.")

            query += sql.SQL(" WHERE {key} = {value}").format(
                key=sql.Identifier(sql_call.where.key),
                value=sql.Literal(sql_call.where.value),
            )

        with self.local.db_conn.cursor() as cursor:
            cursor.execute(query)
            if call_type == SqlCallType.SELECT:
                return cursor.fetchall()
            else:
                return []

    def sanitize_database(self) -> None:
        sql_calls: list[SqlCall] = [
            SqlCall("ir.mail_server", KeyValuePair("active", "False")),
            SqlCall("ir.config_parameter", KeyValuePair("value", "False"), KeyValuePair("key", "mail.catchall.domain")),
            SqlCall("ir.config_parameter", KeyValuePair("value", "False"), KeyValuePair("key", "mail.catchall.alias")),
            SqlCall("ir.config_parameter", KeyValuePair("value", "False"), KeyValuePair("key", "mail.bounce.alias")),
            SqlCall("ir.cron", KeyValuePair("active", "False")),
        ]
        if self.local.base_url:
            sql_calls.append(
                SqlCall(
                    "ir.config_parameter",
                    KeyValuePair("value", self.local.base_url),
                    KeyValuePair("key", "web.base.url"),
                )
            )

        _logger.info("Sanitizing database...")
        for sql_call in sql_calls:
            _logger.debug(f"Executing SQL call: {sql_call}")
            self.call_odoo_sql(sql_call, SqlCallType.UPDATE)

        active_crons = self.call_odoo_sql(SqlCall("ir.cron", where=KeyValuePair("active", "True")), SqlCallType.SELECT)

        if active_crons:
            errors = "\n".join(f"- {cron[7]} (id: {cron[0]})" for cron in active_crons)
            raise OdooDatabaseUpdateError(f"Error: The following cron jobs are still active:\n{errors}")

    def update_shopify_config(self) -> None:
        # noinspection PyArgumentList
        settings = ShopifySettings()

        # Safety check: prevent setting production values, allow replacing production with development
        production_indicators = ["yps-your-part-supplier", "outboardpartswarehouse", "opw-prod", "production", "live"]

        # Check if we're trying to SET a production value (dangerous)
        new_value_lower = settings.shop_url_key.lower()
        for indicator in production_indicators:
            if indicator in new_value_lower:
                raise OdooDatabaseUpdateError(
                    f"SAFETY CHECK FAILED: Attempting to set shop_url_key to '{settings.shop_url_key}' which appears to be production. "
                    f"Found production indicator: '{indicator}'. Database will be dropped for safety."
                )

        # Log what we're doing for transparency
        current_shop_url = self.call_odoo_sql(
            SqlCall("ir.config_parameter", KeyValuePair("value"), KeyValuePair("key", "shopify.shop_url_key")), SqlCallType.SELECT
        )

        if current_shop_url and current_shop_url[0]:
            current_value = current_shop_url[0][0]
            _logger.info(f"Replacing shop_url_key: '{current_value}' → '{settings.shop_url_key}'")
        else:
            _logger.info(f"Setting shop_url_key to: '{settings.shop_url_key}'")

        settings.validate_safe_environment()

        sql_calls: list[SqlCall] = [
            SqlCall(
                "ir.config_parameter",
                KeyValuePair("value", settings.shop_url_key),
                KeyValuePair("key", "shopify.shop_url_key"),
            ),
            SqlCall(
                "ir.config_parameter",
                KeyValuePair("value", settings.api_token.get_secret_value()),
                KeyValuePair("key", "shopify.api_token"),
            ),
            SqlCall(
                "ir.config_parameter",
                KeyValuePair("value", settings.webhook_key),
                KeyValuePair("key", "shopify.webhook_key"),
            ),
            SqlCall(
                "ir.config_parameter",
                KeyValuePair("value", True),
                KeyValuePair("key", "shopify.test_store"),
            ),
        ]
        _logger.info("Updating Shopify configuration...")
        for sql_call in sql_calls:
            _logger.debug(f"Executing SQL call: {sql_call}")
            try:
                self.call_odoo_sql(sql_call, SqlCallType.UPDATE)
            except psycopg2.Error as error:
                raise OdooDatabaseUpdateError(f"Failed to update Shopify configuration: {error}") from error

    def clear_shopify_ids(self) -> None:
        with self.local.db_conn.cursor() as cursor:
            cursor.execute(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'product_product' AND column_name LIKE 'shopify%'"
            )
            existing_fields = [row[0] for row in cursor.fetchall()]

        fields_to_clear = [
            "shopify_created_at",
            "shopify_last_exported",
            "shopify_last_exported_at",
            "shopify_condition_id",
            "shopify_variant_id",
            "shopify_product_id",
            "shopify_ebay_category_id",
        ]

        for field in fields_to_clear:
            if field in existing_fields:
                sql_call = SqlCall("product.product", KeyValuePair(field))
                try:
                    self.call_odoo_sql(sql_call, SqlCallType.UPDATE)
                except psycopg2.Error as error:
                    raise OdooDatabaseUpdateError(f"Failed to clear Shopify ID {field}: {error}") from error
            else:
                _logger.info(f"Skipping field {field} - does not exist in database")

    def drop_database(self) -> None:
        _logger.info("Rolling back database update: dropping database")
        self.terminate_all_db_connections()
        drop_cmd = f"dropdb --if-exists -h {self.local.host} -U {self.local.db_user} {self.local.db_name}"
        self.run_command(drop_cmd)

    def update_addons(self) -> None:
        try:
            addons_folder = Path("/volumes/addons")
            if not addons_folder.exists():
                addons_folder = Path("/opt/project/addons")
            if not addons_folder.exists():
                addons_folder = Path("/opt/odoo/odoo-addons")

            addon_list = ",".join(d.name for d in addons_folder.iterdir() if d.is_dir())
            if not addon_list:
                _logger.info("No addons found to update.")
                return
            odoo_bin = Path("/odoo/odoo-bin")
            if not odoo_bin.exists():
                odoo_bin = f"{Path('/opt/odoo/venv/bin/python')} {odoo_bin}"
            command = f"{odoo_bin} --stop-after-init -d {self.local.db_name} --no-http -u {addon_list}"
            conf = Path("/etc/odoo.conf")
            if conf.exists():
                command += f" --config {conf}"
            self.run_command(command)
        except subprocess.CalledProcessError as update_error:
            raise OdooRestorerError(f"Failed to update addons: {update_error}") from update_error

    def run(self, do_sanitize: bool = True) -> None:
        filestore_proc = self.overwrite_filestore()
        self.overwrite_database()
        filestore_proc.wait()
        if filestore_proc.returncode != 0:
            raise OdooRestorerError("Filestore rsync failed.")
        _logger.info("Filestore overwrite completed.")
        if do_sanitize:
            try:
                self.sanitize_database()
                self.local.db_conn.commit()
            except OdooDatabaseUpdateError:
                self.drop_database()
                raise

        self.update_addons()

        if do_sanitize:
            try:
                self.update_shopify_config()
                self.clear_shopify_ids()
                self.local.db_conn.commit()
            except OdooDatabaseUpdateError:
                self.drop_database()
                raise

        _logger.info("Upstream overwrite completed successfully.")


if __name__ == "__main__":
    # noinspection PyArgumentList
    local_settings = LocalServerSettings()
    # noinspection PyArgumentList
    upstream_settings = UpstreamServerSettings()
    restore_upstream_to_local = OdooUpstreamRestorer(local_settings, upstream_settings)
    restore_upstream_to_local.run()
