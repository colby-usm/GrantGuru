/*
    Select Internal Deadlines by Soonest
    Version: 15 November 2025
    Author: Mathieu Poulin
    Description: Retrieves internal deadlines ordered by deadline date (soonest first)

    Disclaimer: A portion of this code was generated with the assistance of AI.
*/

SELECT 
    internal_deadline_id,
    deadline_name,
    deadline_date,
    application_id
FROM 
    InternalDeadlines
ORDER BY 
    deadline_date ASC;
