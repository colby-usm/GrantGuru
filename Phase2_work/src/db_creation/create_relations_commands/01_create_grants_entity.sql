/* 
  Grants Table Relation
  Version: 1 November 2025
  Author: James Tedder
  Description: A Grants entity encapsulates all fields scraped from Grants.gov
*/

create table Grants (
    grant_id BINARY(16) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
    grant_title varchar(255),
    -- Need to check opportunity_number constraints on grants.gov but can't right now because it is down for maintenance
    opportunity_number varchar(250) NOT NULL UNIQUE, 
    description TEXT,
    research_field varchar(250),
    expected_award_count int CHECK (expected_award_count >= 0),
    eligibility varchar(4000),
    award_max_amount int CHECK (award_max_amount >= 0),
    award_min_amount int CHECK (award_min_amount >= 0),
    program_funding int CHECK (program_funding >= 0),
    provider varchar(255),
    link_to_source varchar(2048) NOT NULL,
    point_of_contact varchar(300),
    date_posted date,
    archive_date date,
    date_closed date,
    last_update_date date
);

CREATE INDEX idx_grants_research_field ON Grants (research_field);