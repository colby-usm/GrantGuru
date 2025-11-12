/*
    delete_documents.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Delete a document by its UUID

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - document_id: The UUID of the document to delete
*/

DELETE FROM Documents
WHERE document_id = UUID_TO_BIN(%s);
