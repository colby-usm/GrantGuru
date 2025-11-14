/*
    create_documents.sql
    Author: Mathieu Poulin
    Version: 12 November 2025
    Description: Insert a new document with trimmed and normalized fields

    Disclaimer: A portion of this code was generated with the assistance of AI.

    Parameters:
        - document_name:
            Name of the document (required)

        - document_type:
            Type of the document (required)

        - document_size:
            Size of the document in bytes (required)

        - upload_date:
            Date and time when the document was uploaded (required)

        - application_id:
            Associated application ID (required)

    Returns:
        The newly created document_id as binary UUID
*/

INSERT INTO Documents (
    document_name,
    document_type,
    document_size,
    upload_date,
    application_id
) VALUES (
    TRIM(%(document_name)s),
    TRIM(%(document_type)s),
    %(document_size)s,
    %(upload_date)s,
    %(application_id)s
);