/*
    Documents Entity Creation
    Version: 4 November 2025
    Author: Mathieu Poulin
    Description: A Documents entity and its attributes
*/

CREATE TABLE Documents (
    document_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),

    document_name VARCHAR(50) PRIMARY KEY,
    document_type VARCHAR(10) NOT NULL,
    document_size INT UNSIGNED NOT NULL,
    upload_date DATETIME NOT NULL,
    FOREIGN KEY (application_id) REFERENCES Applications(application_id) ON DELETE CASCADE
);