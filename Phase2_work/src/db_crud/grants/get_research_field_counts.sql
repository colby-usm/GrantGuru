/*
* Author: Colby Wirth
* Description: Returns the total aggregate funding of current grants
*/

SELECT FORMAT(COALESCE(SUM(program_funding), 0), 0) AS aggregate_program_funding
FROM grants
WHERE CURDATE() > date_closed;
