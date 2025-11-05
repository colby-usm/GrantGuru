/* 
  Application Table Relation
  Version: 3 November 2025
  Author: Abdullahi Abdullahi
  Description: The Application entity 
*/
CREATE TABLE Application (
    application_id CHAR(20) PRIMARY KEY,
    user_id CHAR(20) NOT NULL,
    grant_id CHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    application_date DATE NOT NULL,
    
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (grant_id) REFERENCES Grants(grant_id) ON DELETE CASCADE,
    
    -- Ensure a user can only apply once to a specific grant
    UNIQUE KEY unique_user_grant (user_id, grant_id)
);

-- Indexes for faster queries
CREATE INDEX idx_application_status ON Application(status);
CREATE INDEX idx_application_user ON Application(user_id);
CREATE INDEX idx_application_grant ON Application(grant_id);
