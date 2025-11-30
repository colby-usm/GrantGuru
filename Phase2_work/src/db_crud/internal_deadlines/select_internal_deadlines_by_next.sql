/*
    Select Internal Deadlines by Next
    Version: 15 November 2025
    Author: Mathieu Poulin
    Description: Retrieves the next upcoming internal deadline (earliest deadline that hasn't passed yet)

    Disclaimer: A portion of this code was generated with the assistance of AI.
*/

SELECT 
    internal_deadline_id,
    deadline_name,
    deadline_date,
    application_id
FROM 
    InternalDeadlines
WHERE 
    deadline_date >= NOW()
ORDER BY 
    deadline_date ASC
LIMIT 1;
