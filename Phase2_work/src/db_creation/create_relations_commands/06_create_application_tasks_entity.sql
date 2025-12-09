/*
  ApplicationTasks Table Relation
  Version: 7 December 2025
  Author: Abdullahi Abdullahi
  Description: Tracks multiple internal deadlines/tasks for draft applications
*/
CREATE TABLE ApplicationTasks (
    task_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),

    application_id BINARY(16) NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    task_description TEXT NULL,
    deadline DATE NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (application_id) REFERENCES Applications(application_id) ON DELETE CASCADE
);

-- Indexes for faster queries
CREATE INDEX idx_task_application ON ApplicationTasks(application_id);
CREATE INDEX idx_task_deadline ON ApplicationTasks(deadline);
CREATE INDEX idx_task_completed ON ApplicationTasks(completed);
