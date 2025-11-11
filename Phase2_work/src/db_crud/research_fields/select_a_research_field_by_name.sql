/*
  select_a_research_field_by_name.sql
  Author: Colby Wirth
  Version: 9 November 2025
  Description: Find if a research field exists in the DB
*/

SELECT research_field_id FROM ResearchField WHERE research_field = %(research_field)s;
