/*
    Internal Deadlines Entity Creation
    Version: 8 December 2025
    Author: Mathieu Poulin
    Description: An Internal Deadlines entity combining deadline tracking and task management functionality

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Modified: Merged ApplicationTasks functionality into InternalDeadlines
    - Added task_description field for detailed task information
    - Added completed boolean flag to track task completion status
    - Added timestamps for creation and update tracking
*/

CREATE TABLE InternalDeadlines (
    internal_deadline_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),

    application_id BINARY(16) NOT NULL,
    deadline_name VARCHAR(255) NOT NULL,
    deadline_date DATE NOT NULL,
    task_description TEXT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (application_id) REFERENCES Applications(application_id) ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX idx_deadline_application ON InternalDeadlines(application_id);
CREATE INDEX idx_deadline_date ON InternalDeadlines(deadline_date);
CREATE INDEX idx_deadline_completed ON InternalDeadlines(completed);
