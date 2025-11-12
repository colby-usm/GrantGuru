/*
    delete_internal_deadlines.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Delete an internal deadline by its UUID

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - internal_deadline_id: The UUID of the internal deadline to delete
*/

DELETE FROM InternalDeadlines
WHERE internal_deadline_id = UUID_TO_BIN(%s);
