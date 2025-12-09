-- Backup all documents metadata for a specific application
-- Note: This backs up metadata only; actual file content should be backed up separately

SELECT
    BIN_TO_UUID(document_id) as document_id,
    BIN_TO_UUID(application_id) as application_id,
    document_name,
    document_type,
    document_size,
    upload_date
FROM Documents
WHERE application_id = UUID_TO_BIN(%s)
ORDER BY upload_date DESC;
