/*
    update_documents.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Update a document's information by UUID. All fields except document_id can be updated.

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - document_id: UUID of the document to update (required)
        - document_name: Name of the document (optional)
        - document_type: Type of the document (optional)
        - document_size: Size of the document in bytes (optional)
        - upload_date: Date and time when the document was uploaded (optional)
        - application_id: Associated application ID (optional)
*/

UPDATE Documents
SET
    document_name = COALESCE(%(document_name)s, document_name),
    document_type = COALESCE(%(document_type)s, document_type),
    document_size = COALESCE(%(document_size)s, document_size),
    upload_date = COALESCE(%(upload_date)s, upload_date),
    application_id = COALESCE(%(application_id)s, application_id)
WHERE document_id = UUID_TO_BIN(%(document_id)s);
