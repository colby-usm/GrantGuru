-- Restore a single application document metadata

INSERT INTO Documents (
    document_id,
    application_id,
    document_name,
    document_type,
    document_size,
    upload_date
) VALUES (
    UUID_TO_BIN(%s),
    UUID_TO_BIN(%s),
    %s,
    %s,
    %s,
    %s
)
ON DUPLICATE KEY UPDATE
    document_name = VALUES(document_name),
    document_type = VALUES(document_type),
    document_size = VALUES(document_size),
    upload_date = VALUES(upload_date);
