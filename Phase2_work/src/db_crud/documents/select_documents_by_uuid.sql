/*
    select_documents_by_uuid.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Select a document by its UUID

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - document_id: The UUID of the document (required)

    Returns:
        All columns of the Documents table for the given document_id
*/

SELECT 
    BIN_TO_UUID(document_id) AS document_id,
    document_name,
    document_type,
    document_size,
    upload_date,
    BIN_TO_UUID(application_id) AS application_id
FROM Documents
WHERE document_id = UUID_TO_BIN(%s);
