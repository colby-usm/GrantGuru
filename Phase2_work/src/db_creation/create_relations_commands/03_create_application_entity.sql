/* 
  Applications Table Relation
  Version: 3 November 2025
  Author: Abdullahi Abdullahi
  Description: The Applications entity 
*/
CREATE TABLE Applications (
    application_id CHAR(20) PRIMARY KEY,
    user_id BINARY(16),
    grant_id CHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    application_date DATE NOT NULL,

    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (grant_id) REFERENCES Grants(grant_id) ON DELETE CASCADE,
 
    -- Ensure a user can only apply once to a specific grant
    UNIQUE KEY unique_user_grant (user_id, grant_id)
);

-- Indexes for faster queries
CREATE INDEX idx_application_status ON Applications(status);
CREATE INDEX idx_application_user ON Applications(user_id);
CREATE INDEX idx_application_grant ON Applications(grant_id);
