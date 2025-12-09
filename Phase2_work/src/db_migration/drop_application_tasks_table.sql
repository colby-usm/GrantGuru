/*
    Cleanup Script: Drop ApplicationTasks Table
    Version: 8 December 2025
    Description: Drops the ApplicationTasks table as task functionality has been merged into InternalDeadlines.

    Note: This will delete all existing task data. Run only if you don't need to preserve existing tasks.
*/

-- Drop the ApplicationTasks table
DROP TABLE IF EXISTS ApplicationTasks;

-- Verification query (uncomment to verify table is dropped)
-- SHOW TABLES LIKE 'ApplicationTasks';
