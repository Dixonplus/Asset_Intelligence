-- AB Afric Asset Intelligence - safe manual migration for the current known issue.
-- This migration is non-destructive. Back up the database before changing it.
USE asset_intelligence;

SET @sql = IF(
    EXISTS(
        SELECT 1 FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'part' AND COLUMN_NAME = 'reorder_level'
    ),
    'SELECT 1',
    'ALTER TABLE `part` ADD COLUMN `reorder_level` DECIMAL(14,2) NULL DEFAULT 0 AFTER `quantity_on_hand`'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- The application also contains a Python schema synchronizer. For complete
-- synchronization of an older database, run:
--     python database_sync.py
