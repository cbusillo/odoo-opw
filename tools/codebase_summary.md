
You are an expert Odoo 18 core developer with extensive experience in Odoo 18 Enterprise and the Owl.js 2.0 framework.

# Company Details

- Outboard Parts Warehouse
- Production site: https://odoo.outboardpartswarehouse.com/
- Local development: http://localhost:8069/
- Primary Business: Buying outboard motors and parting them out on eBay and Shopify
- GitHub Repository: cbusillo/odoo-addons
- Permanent Branches: opw-prod, opw-testing

# Development Tools

- IntelliJ IDEA Ultimate 2024.3.1.1
- Odoo Framework Integration plugin
- Odoo 18 Enterprise
- Owl.js 2.0
- Python 3.13
- Shopify GraphQL API
- Docker

# Code Standards

- Pythonic, clean, and elegant code
- Follow Odoo core development patterns and best practices
- Proper use of inheritance and extension mechanisms
- Follow standard Odoo project structure and logging patterns
- PEP 8 compliance
- Descriptive function and variable names that convey purpose clearly instead of comments
- No comments or docstrings in returned code

# Workflow

## Code Review Process:

- Retrieve and examine relevant code, models, and views before analysis or explanation. For example, check model fields,
  XML views, and dependencies.
- Check for dependencies that may be relevant to the issue.
- Validate modifications through manual or automated testing.

# Project Structure

## Base Path
- JetBrains Project Root: /Users/cbusillo/Developer/odoo-addons/
- Module location: addons/product_connect

## Key Directories
- models/: Business logic and database models
- views/: XML view definitions
- static/: Static assets (CSS, JS, images)
- security/: Access rights and rules
- data/: Data files and demo data

## Common File Patterns
- Model files: models/*.py
- View files: views/*.xml
- JavaScript files: static/src/js/*.js
# Codebase Summary

## .
- **docker-compose.override.yml**
- **docker-compose.yml**
- **mypy.ini**
- **odoo.local.conf**
- **odoo.prod.conf**
- **odoo.testing.conf**

## addons

## addons/disable_odoo_online
- **__init__.py**
- **__manifest__.py**

## addons/disable_odoo_online/models
- **__init__.py**
- **publisher_warranty_contract.py**
  - Class `PublisherWarrantyContract` with methods: update_notification

## addons/disable_odoo_online/security
- **ir.model.access.csv**

## addons/product_connect
- **__init__.py**
- **__manifest__.py**
- **requirements-dev.txt**
- **requirements.txt**
- **tsconfig.json**
- **webpack.config.js**

## addons/product_connect/.github

## addons/product_connect/.github/workflows
- **opw-prod.yml**
- **opw-testing.yml**

## addons/product_connect/controllers
- **__init__.py**
- **download_controllers.py**
  - Class `SingleDownloadController` with methods: download_single
- **shopify_webhook.py**
  - Class `ShopifyWebhook` with methods: webhook

## addons/product_connect/data
- **mail_templates.xml**
- **motor_part_template_data.xml**
- **motor_stat_data.xml**
- **motor_test_section_data.xml**
- **motor_test_selection_data.xml**
- **motor_test_template_data.xml**
- **product_condition_data.xml**
- **res_config_data.xml**

## addons/product_connect/graphql

## addons/product_connect/graphql/schema
- **shopify_schema_2025-04.json**
- **shopify_schema_2025-04.sdl**

## addons/product_connect/graphql/shopify
- **graphql.config.yml**
- **shopify_bulk_operation.graphql**
- **shopify_customers.graphql**
- **shopify_general_types.graphql**
- **shopify_order.graphql**
- **shopify_product.graphql**

## addons/product_connect/mixins
- **__init__.py**
- **image_mixin.py**
  - Class `ImageMixin` with methods: _mark_for_shopify_product_export, create, write, unlink, _compute_attachment, _compute_file_size_kb, _compute_image_dimensions, _reset_image_details, remove_missing_images, action_open_full_image
- **label_mixin.py**
  - Class `LabelMixin` with methods: _print_labels, wrap_text, generate_label_base64, combine_labels_base64
- **motor_test_condition_mixin.py**
  - Class `MotorTestConditionMixin` with methods: is_condition_met
- **notification_manager_mixin.py**
  - Class `NotificationHistory` with methods: create, cleanup, count_of_recent_notifications, recent_notifications
  - Class `NotificationManagerMixin` with methods: notify_channel, notify_channel_on_error, send_email_notification_to_admin

## addons/product_connect/models
- **__init__.py**
- **delivery_carrier.py**
  - Class `DeliveryCarrier` (no methods)
  - Class `DeliveryCarrierServiceMap` (no methods)
- **motor.py**
  - Class `MotorStage` with methods: _compute_fold
  - Class `MotorTag` (no methods)
  - Class `Motor` with methods: _read_group_stages, _compute_product_count, _compute_completed_test_count, _compute_applicable_test_count, action_view_products, action_view_tests, _get_years, _compute_product_repair_states_with_icons, create, write, _compute_products_with_reference, _compute_image_count, _compute_missing_parts_names, _compute_shaft_length, _compute_hours, _compute_has_notes, _compute_icon, _compute_horsepower_formatted, _compute_display_name, _compute_hide_compression_page, set_all_cylinders_untestable, generate_qr_code, get_horsepower_formatted, _check_horsepower, _check_unique_location, _sanitize_vals, _create_motor_tests, _create_motor_parts, _check_product_conditions, _should_exclude_product, _should_repair_product, create_motor_products, _get_cylinder_count, _compute_compression, _create_default_images, download_zip_of_images, _compute_price_of_motor, apply_cost, enable_ready_for_sale, print_motor_product_labels, print_motor_pull_list, notify_changes, print_motor_labels
- **motor_part.py**
  - Class `MotorPartTemplate` (no methods)
  - Class `MotorPart` (no methods)
- **motor_product.py**
  - Class `MotorDismantleResult` (no methods)
  - Class `MotorProductTemplateCondition` (no methods)
  - Class `MotorProductTemplate` with methods: get_template_tags_list, get_template_tags, get_template_tags_from_test_tags, get_template_tags_from_motor_model
- **motor_stat.py**
  - Class `MotorCylinder` (no methods)
  - Class `MotorImage` (no methods)
  - Class `MotorStroke` with methods: __str__
  - Class `MotorConfiguration` with methods: __str__
- **motor_test.py**
  - Class `MotorTestSection` (no methods)
  - Class `MotorTestTemplate` with methods: _compute_value
  - Class `MotorTestTemplateCondition` (no methods)
  - Class `MotorTestSelection` with methods: __str__
  - Class `MotorTest` with methods: write, _compute_result, _compute_is_applicable
- **printnode_interface.py**
  - Class `PrintNodeInterface` with methods: get_gateway, get_printers, get_printer_tuple, print_label
- **product_base.py**
  - Class `ProductType` (no methods)
  - Class `ProductCondition` (no methods)
- **product_color.py**
  - Class `ProductColorTag` (no methods)
  - Class `ProductColor` with methods: __str__
- **product_manufacturer.py**
  - Class `ProductManufacturer` with methods: _compute_name_normalized, normalize_name, __str__
- **product_product.py**
  - Class `ProductProduct` with methods: update_quantity
- **product_template.py**
  - Class `ProductTemplate` with methods: read_group, create, write, _track_template, _compute_initial_price_total, _compute_initial_cost_total, _compute_is_ready_for_sale_last_enabled_date, _compute_name_with_tags_length, _compute_repairs, _compute_open_repair_count, _compute_repair_state, _compute_image_1920, _inverse_image_1920, _compute_shopify_urls, check_sku, get_next_sku, _check_dimension_values, _compute_first_mpn, get_list_of_mpns, _compute_image_count, _compute_has_recent_messages, name_get, _check_mpn_bin, _onchange_format_mpn_upper, _onchange_format_bin_upper, find_new_products_with_same_mpn, check_for_conflicting_products, _check_fields_and_images, _check_missing_fields, _check_missing_images_or_small_images, _post_missing_data_message, print_bin_labels, print_product_labels, enable_ready_for_sale, _compute_reference_product, _compute_template_name_with_dismantle_notes, _compute_display_name, _compute_motor_product_computed_name, _compute_ready_to_list, reset_name, replace_template_tags, _resolve_tag_value, _apply_tag_values, create_repair_order, action_open_repairs
- **repair_order.py**
  - Class `RepairOrder` with methods: _compute_total_estimated_cost, action_repair_done
- **res_partner.py**
  - Class `ResPartner` with methods: _compute_shopify_urls, _compute_ebay_profile_url
- **res_users.py**
  - Class `Users` with methods: __str__
- **sale_order.py**
  - Class `SaleOrder` (no methods)
- **sale_order_line.py**
  - Class `SaleOrderLine` (no methods)
- **shopify_sync.py**
  - Class `ShopifySync` with methods: fields_get, _is_duplicate, create, unlink, _compute_progress_percent, _compute_create_time_human, _compute_start_time_human, _compute_end_time_human, _compute_run_time, _fail_stale_runs, _cron_dispatch_next, _dispatch_lock, run_async, create_and_run_async, duplicate_and_run_async, duplicate, _execute_mode, _prepare_failure_vals, _mark_failed, _run_guard, completed_str, _run_reset_shopify, _run_import_all_products, _run_export_all_products, _run_import_then_export_products, _run_import_changed_products, _run_export_changed_products, _run_import_one_product, _run_export_batch_products, _run_import_products_since_date, _run_export_products_since_date, _run_import_all_orders, _run_import_changed_orders, _run_import_one_order, _run_import_all_customers, _run_import_changed_customers, _run_import_one_customer
- **stock_move.py**
  - Class `StockMove` with methods: _compute_line_cost_price

## addons/product_connect/report
- **motor_product_reports.xml**
- **motor_reports.xml**
- **product_reports.xml**

## addons/product_connect/security
- **ir.model.access.csv**

## addons/product_connect/services

## addons/product_connect/services/shopify
- **__init__.py**
- **helpers.py**
  - Functions: normalize_str, normalize_phone, normalize_email, image_order_key, last_import_config_key, write_if_changed, parse_shopify_datetime_to_utc, format_datetime_for_shopify, parse_shopify_id_from_gid, format_shopify_gid_from_id, parse_shopify_sku_field_to_sku_and_bin, format_sku_bin_for_shopify, determine_latest_odoo_product_modification_time
  - Class `SyncMode` with methods: __new__, display_name, resource_type, choices
  - Class `OdooDataError` with methods: __init__, sku, odoo_product_id, name, __str__
  - Class `OdooMissingSkuError` (no methods)
  - Class `ShopifySyncRunFailed` (no methods)
  - Class `ShopifyApiError` with methods: __init__, __str__, sku, shopify_product_id, name
  - Class `ShopifyDataError` (no methods)
  - Class `ShopifyMissingSkuFieldError` (no methods)
  - Class `ShopifyStaleRunTimeout` (no methods)
- **service.py**
  - Class `ShopifyService` with methods: __init__, client, get_first_location_gid, _create_client, _create_http_client, _compute_throttle_delay, _throttle_info

## addons/product_connect/services/shopify/sync
- **base.py**
  - Class `_PageInfo` (no methods)
  - Class `ShopifyPage` (no methods)
  - Class `ShopifyBase` with methods: __init__, _maybe_commit, _iterate_pages
  - Class `ShopifyBaseImporter` with methods: run, _fetch_page, run_since_last_import, run_by_id, _import_one
  - Class `ShopifyBaseExporter` with methods: run, _export_one
  - Class `ShopifyBaseDeleter` with methods: collect_nodes, run, _delete_one

## addons/product_connect/services/shopify/sync/deleters
- **product_deleter.py**
  - Class `ProductDeleter` with methods: __init__, _fetch_product_ids_page, delete_all_products, _delete_one

## addons/product_connect/services/shopify/sync/exporters
- **product_exporter.py**
  - Class `ProductExporter` with methods: __init__, export_products_since_last_export, export_products_since_datetime, _find_products_to_export, export_products, _export_one, _update_odoo_product, _sync_images_after_export, is_published_on_all_channels, is_published_on_channel, _publish_product, metafield_from_id_value_key, _map_odoo_product_to_shopify_product_set_input

## addons/product_connect/services/shopify/sync/importers
- **customer_importer.py**
  - Class `CustomerImporter` with methods: __init__, _fetch_page, _import_one, _get_or_create_category, _get_tax_exempt_fiscal_position, import_customers_since_last_import, _format_phone_number, import_customer, process_address
- **order_importer.py**
  - Class `OrderImporter` with methods: __init__, _normalise_carrier_name, _get_amount_for_order_currency, _get_discount_allocation_amount, _fetch_page, import_orders_since_last_import, _import_one, _sync_order_lines, _apply_shipping, _apply_global_discount, _apply_tracking, _extract_tracking_numbers, _get_special_product, _resolve_address
- **product_importer.py**
  - Class `ProductImporter` with methods: __init__, _fetch_page, import_products_since_last_import, _import_one, _images_are_in_sync, get_or_create_manufacturer, get_or_create_part_type, import_images_from_shopify, fetch_image_data, _ordered_odoo_media_ids, _ordered_shopify_media_ids, _sync_images_bidirectional, save_odoo_product

## addons/product_connect/static

## addons/product_connect/static/src

## addons/product_connect/static/src/js

## addons/product_connect/static/src/js/external
- **qr-scanner-worker.min.js**
- **qr-scanner.umd.min.js**

## addons/product_connect/static/src/js/forms
- **motor_form.js**

## addons/product_connect/static/src/js/lists
- **list_autorefresh.js**

## addons/product_connect/static/src/js/types
- **qr-scanner.d.ts**

## addons/product_connect/static/src/js/utils
- **image_utils.js**
- **testing_banner.js**

## addons/product_connect/static/src/js/widgets
- **date_only_widget.js**
- **file_drop_widget.js**
- **html_template_widget.js**
- **image_upload_widget.js**
- **motor_test_widget.js**
- **qr_code_widget.js**
- **repair_states_widget.js**
- **resettable_badge_selection_widget.js**
- **search_mpn_online_widget.js**

## addons/product_connect/static/src/scss
- **file_drop_widget.scss**
- **motor.scss**
- **product_import_tree_view.scss**
- **search_mpn_online_widget.scss**
- **testing_banner.scss**
- **theme_opw.scss**

## addons/product_connect/static/src/xml
- **date_only_widget.xml**
- **file_drop_widget.xml**
- **image_upload_widget.xml**
- **motor_test_widget.xml**
- **qr_code_widget.xml**
- **repair_states_widget.xml**
- **resettable_badge_selection_widget.xml**
- **search_mpn_online_widget.xml**
- **testing_banner.xml**

## addons/product_connect/tests

## addons/product_connect/utils
- **__init__.py**
- **constants.py**

## addons/product_connect/views
- **delivery_carrier_views.xml**
- **motor_part_template_views.xml**
- **motor_product_template_views.xml**
- **motor_product_views.xml**
- **motor_test_section_views.xml**
- **motor_test_selection_views.xml**
- **motor_test_template_views.xml**
- **motor_views.xml**
- **printnode_interface_views.xml**
- **product_color_views.xml**
- **product_condition_views.xml**
- **product_image_views.xml**
- **product_import_views.xml**
- **product_inventory_wizard_views.xml**
- **product_manufacturer_views.xml**
- **product_product_views.xml**
- **product_template_views.xml**
- **product_type_views.xml**
- **repair_order_views.xml**
- **res_partner_views.xml**
- **res_users_views.xml**
- **shopify_sync_views.xml**

## addons/product_connect/wizards
- **__init__.py**
- **product_inventory_wizard.py**
  - Class `ProductInventoryWizardLine` (no methods)
  - Class `ProductInventoryWizard` with methods: _compute_products_not_selected, _compute_bin_needs_update, _compute_total_product_labels_to_print, notify_user, _handle_product_scan, _handle_bin_scan, _load_bin_products, _onchange_scan_box, action_apply_bin_changes, action_print_product_labels, action_print_bin_label
- **product_label_layout.py**
  - Class `ProductLabelLayout` with methods: _prepare_report_data, process

## docker
- **Dockerfile**

## docker/config
- **odoo.conf**

## docker/scripts
- **generate_shopify_models.py**
  - Functions: fetch_shopify_introspection, save_introspection_json, save_schema_sdl, main
- **install_addon_requirements.sh**
- **overwrite_from_upstream.py**
  - Class `OdooRestorerError` (no methods)
  - Class `OdooDatabaseUpdateError` (no methods)
  - Class `SqlCallType` (no methods)
  - Class `KeyValuePair` (no methods)
  - Class `SqlCall` (no methods)
  - Class `LocalServerSettings` (no methods)
  - Class `UpstreamServerSettings` (no methods)
  - Class `ShopifySettings` (no methods)
  - Class `OdooUpstreamRestorer` with methods: __init__, run_command, overwrite_filestore, overwrite_database, connect_to_db, terminate_all_db_connections, call_odoo_sql, sanitize_database, update_shopify_config, clear_shopify_ids, drop_database, update_addons, run

## pyproject.toml

## tests
- **__init__.py**
- **test_shopify_sync.py**
  - Class `TestShopifySync` with methods: setUp, create_products, test_is_duplicate_detects_existing_batch, test_create_skips_duplicate_batches, test_run_guard_sets_state, test_run_guard_failure_marks_failed, test_dispatch_lock_false_when_taken

## tools
- **codebase_summary.md**
- **files_loc_and_size.py**
  - Functions: matches_pattern, calculate_loc_and_size
- **init-and-run-odoo-dev-server.sh**
- **init-and-run-odoo-dev.sh**
- **project_indexer.py**
  - Functions: set_parents, parse_python_file, index_codebase, generate_markdown_summary, main
