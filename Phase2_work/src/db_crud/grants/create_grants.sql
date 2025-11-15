/*
  create_grants.sql
  Author: James Tedder
  Version: 13 November 2025
  Description: Insert a new grant

  Parameters:
    - grant_title: The title of the grant
    - description: Detailed description of the grant
    - research_field: The research field of the grant
    - expected_award_count: The number of awards expected to be issued
    - eligibilty: Elegibility criteria for the grant
    - award_max_amount: Maximum amount that can be awarded
    - award_min_amount: Minimum amount that can be awarded
    - program_funding: Total funding available for the grant
    - provider: The organization providing the grant
    - link_to_source: Link to the official grant listing
    - point_of_contact: Point of contact for the grant
    - date_posted: The date the grant was posted
    - archive_date: The date the grant was archived
    - date_closed: The date the grant was closed
    - last_update_date: The date the grant information was last updated on grants.gov
  
  Returns: The newly created grant_id as binary UUID
*/

INSERT INTO Grants (

    grant_title,
    description,
    research_field,
    expected_award_count,
    eligibilty,
    award_max_amount,
    award_min_amount,
    program_funding,
    provider,
    link_to_source,
    point_of_contact,
    date_posted,
    archive_date,
    date_closed,
    last_update_date
) VALUES (
    trim(%(grant_title)s),
    trim(%(description)s),
    trim(%(research_field)s),
    %(expected_award_count)s,
    trim(%(eligibility)s),
    %(award_max_amount)s,
    %(award_min_amount)s,
    %(program_funding)s,
    trim(%(provider)s),
    trim(%(link_to_source)s),
    trim(%(point_of_contact)s),
    %(date_posted)s,
    %(archive_date)s,
    %(date_closed)s,
    %(last_update_date)s
);