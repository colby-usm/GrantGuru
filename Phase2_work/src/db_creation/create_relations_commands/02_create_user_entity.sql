/* 
  Users Table Relation
  Version: 1 November 2025
  Author: Colby Wirth
  Description: A Users entity and their research fields
*/

CREATE TABLE Users (
    user_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID()))

    -- Composite attribute: Name = (f_name, m_name, l_name)
    f_name VARCHAR(50) NOT NULL,
    m_name VARCHAR(50),
    l_name VARCHAR(50) NOT NULL,

    institution VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE ResearchField (
    research_field_id INT AUTO_INCREMENT PRIMARY KEY,
    research_field VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE UserResearchFields (
    user_id INT,
    research_field_id INT,
    PRIMARY KEY (user_id, research_field_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (research_field_id) REFERENCES ResearchField(research_field_id) ON DELETE CASCADE
);
