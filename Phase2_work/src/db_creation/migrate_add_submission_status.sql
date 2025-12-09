/*
  Migration: Add submission_status column to Applications table
  Date: 8 December 2025
  Description: Adds the submission_status column to support tracking whether
               an application has been started or submitted
*/

-- Add submission_status column if it doesn't exist
ALTER TABLE Applications
ADD COLUMN submission_status ENUM('started', 'submitted') NOT NULL DEFAULT 'started'
AFTER grant_id;

-- Create index for faster queries on submission_status
CREATE INDEX idx_application_submission_status ON Applications(submission_status);

-- Optional: Set all existing applications to 'started' status
-- (This is already done by the DEFAULT value above)
