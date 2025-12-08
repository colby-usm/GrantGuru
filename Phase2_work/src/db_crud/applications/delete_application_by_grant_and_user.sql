/* Application Deletion Script for Applications Table
Version: 15 November 2025
Author: Abdullahi Abdullahi
Description:
 Delet based on user_id and grant_id
 Parameters:
    - user_id: The unique identifier of the user (required)
    - grant_id: The unique identifier of the grant (required)
*/

DELETE FROM Applications
WHERE user_id = UUID_TO_BIN(%(user_id)s) AND grant_id = UUID_TO_BIN(%(grant_id)s);

