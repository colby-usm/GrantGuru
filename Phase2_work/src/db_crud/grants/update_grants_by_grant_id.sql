/*
  update_grants.sql
  Author: James Tedder
  Version: 13 November 2025
  Description: Update a grant's information by UUID. All fields except grant_id can be updated.

  Parameters:
    - grant_title: The title of the grant (optional)
    - opportunity_number: The number used on grants.gov to identify the grant (required)
    - description: Detailed description of the grant (optional)
    - research_field: The research field of the grant (optional)
    - expected_award_count: The number of awards expected to be issued (optional)
    - eligibilty: Elegibility criteria for the grant (optional)
    - award_max_amount: Maximum amount that can be awarded (optional)
    - award_min_amount: Minimum amount that can be awarded (optional)
    - program_funding: Total funding available for the grant (optional)
    - provider: The organization providing the grant (optional)
    - link_to_source: Link to the official grant listing (optional)
    - point_of_contact: Point of contact for the grant (optional)
    - date_posted: The date the grant was posted (optional)
    - archive_date: The date the grant was archived (optional)
    - date_closed: The date the grant was closed (optional)
    - last_update_date: The date the grant information was last updated on grants.gov (optional)
    - grant_id: The ID of the grant to be updated (required)
*/

UPDATE Grants 
    SET
        grant_title = COALESCE(%(grant_title)s, grant_title),
        opportunity_number = COALESCE(%(opportunity_number)s, opportunity_number),
        description = COALESCE(%(description)s, description),
        research_field = COALESCE(%(research_field)s, research_field),
        expected_award_count = COALESCE(%(expected_award_count)s, expected_award_count),
        eligibility = COALESCE(%(eligibility)s, eligibility),
        award_max_amount = COALESCE(%(award_max_amount)s, award_max_amount),
        award_min_amount = COALESCE(%(award_min_amount)s, award_min_amount),
        program_funding = COALESCE(%(program_funding)s, program_funding),
        provider = COALESCE(%(provider)s, provider),
        link_to_source COALESCE(%(link_to_source)s, link_to_source),
        point_of_contact = COALESCE(%(point_of_contact)s, point_of_contact),
        date_posted = COALESCE(%(date_posted)s, date_posted),
        archive_date = COALESCE(%(archive_date)s, archive_date),
        date_closed = COALESCE(%(date_closed)s, date_closed),
        last_update_date = COALESCE(%(last_update_date)s, last_update_date)
WHERE grant_id = UUID_TO_BIN(%(grant_id)s);