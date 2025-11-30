/*
* Version: 28 November 2025
* Author: Colby Wirth
* Returns a table with the aggregate funding available in the database
*/
SELECT SUM(program_funding) as aggregate_program_funding
WHERE CURRENT_DATE > date_closed;
FROM grants;
