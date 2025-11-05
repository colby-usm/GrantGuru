/*
    Internal Deadlines Entity Creation
    Version: 4 November 2025
    Author: Mathieu Poulin
    Description: An Internal Deadlines entity and its attributes
*/

CREATE TABLE InternalDeadlines (
    internal_deadline_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),

    deadline_name VARCHAR(100) NOT NULL,
    deadline_date DATETIME NOT NULL,
    application_id BINARY(16) NOT NULL,

    FOREIGN KEY (application_id) REFERENCES Applications(application_id) ON DELETE CASCADE
);
