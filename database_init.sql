CREATE DATABASE IF NOT EXISTS asset_intelligence CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE asset_intelligence;
-- The Flask application creates the synchronized enterprise tables with SQLAlchemy db.create_all().
-- For a clean rebuild, remove existing application tables before first run, then start the app.
