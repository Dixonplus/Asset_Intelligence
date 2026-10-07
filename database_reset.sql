-- AB Afric Asset Intelligence - development reset ONLY.
-- WARNING: this permanently deletes application data in asset_intelligence.
-- Back up the database before running this file.
CREATE DATABASE IF NOT EXISTS asset_intelligence CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE asset_intelligence;
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS intelligence_recommendation, capital_decision, maintenance_intelligence, failure_prediction,
notification, asset_movement, third_party_work_order, service_report, cost_history, labor_entry,
pm_execution, consumable, maintenance_schedule, part_usage, part, service_history, service_audit,
service_request, technical_asset_detail, asset, vendor, location, user,
-- Known legacy tables from older schema exports; the current application does not use them.
asset_cost_history, capital_allocation, labour_entry, organization, third_party_service;
SET FOREIGN_KEY_CHECKS=1;
-- Start the Flask application after this reset. SQLAlchemy creates the current tables,
-- then app.schema_sync verifies/adds any missing columns before seed data is loaded.
