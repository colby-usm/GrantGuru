# GrantGuru Backup and Recovery System

## Overview

The GrantGuru Backup and Recovery system provides comprehensive data protection for user applications, including related tasks and document metadata. This system allows users to create backups, restore from backups, and manage their backup files through a user-friendly interface.

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [API Endpoints](#api-endpoints)
4. [Frontend Usage](#frontend-usage)
5. [Backend Implementation](#backend-implementation)
6. [File Structure](#file-structure)
7. [Backup Format](#backup-format)
8. [Recovery Procedures](#recovery-procedures)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Architecture

The backup system follows a three-tier architecture:

```
┌─────────────────────────────────────────────────────┐
│              Frontend (React/TypeScript)            │
│         BackupManagement Component                  │
│         - Create Backups                            │
│         - List Backups                              │
│         - Download/Restore/Delete Backups           │
└────────────────────┬────────────────────────────────┘
                     │ REST API
                     │
┌────────────────────▼────────────────────────────────┐
│                 API Layer (Flask)                   │
│         /api/applications/backup/*                  │
│         - routes_backup.py                          │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│             Business Logic (Python)                 │
│         backup_operations.py                        │
│         - Create/Load/Restore Backups               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│               Database (MySQL)                      │
│         - Applications                              │
│         - ApplicationTasks                          │
│         - Documents                                 │
└─────────────────────────────────────────────────────┘
```

---

## Features

### Core Features

1. **Create Backups**
   - Backup all applications for a specific user
   - Include related tasks and document metadata
   - Store grant and user information for context
   - Generate JSON files with timestamps

2. **List Backups**
   - View all available backups
   - Filter by user
   - Display backup metadata (size, date, application count)

3. **Download Backups**
   - Download backup files to local storage
   - JSON format for portability

4. **Restore Backups**
   - Restore applications from backup files
   - Restore related tasks and documents
   - Handle conflicts with existing data
   - Detailed restoration reports

5. **Delete Backups**
   - Remove old or unnecessary backup files
   - Confirmation required

### Data Included in Backups

- **Applications**: All application records with full details
- **Tasks**: All tasks associated with applications
- **Documents**: Document metadata (file names, types, sizes, dates)
- **Grant Information**: Grant details for context
- **User Information**: User details for verification

**Note**: Actual document file content is NOT backed up, only metadata. File content should be backed up separately using file system backups.

---

## API Endpoints

All backup endpoints are prefixed with `/api/applications/backup/`

### 1. Create Backup

**Endpoint**: `POST /api/applications/backup/create/<user_id>`

**Description**: Create a complete backup of all applications for a user.

**Request Body** (optional):
```json
{
  "save_to_file": true,
  "return_data": false
}
```

**Response**:
```json
{
  "success": true,
  "message": "Backup created successfully",
  "backup_metadata": {
    "timestamp": "2025-12-08T10:30:00",
    "user_id": "uuid",
    "application_count": 5,
    "total_tasks": 15,
    "total_documents": 8,
    "backup_version": "1.0"
  },
  "filepath": "/path/to/backup.json",
  "filename": "backup_user_123_20251208_103000.json"
}
```

### 2. List Backups

**Endpoint**: `GET /api/applications/backup/list/<user_id>`

**Description**: List all available backup files for a user.

**Response**:
```json
{
  "success": true,
  "backups": [
    {
      "filename": "backup_user_123_20251208_103000.json",
      "filepath": "/path/to/backup.json",
      "size": 12345,
      "created": "2025-12-08T10:30:00",
      "timestamp": "2025-12-08T10:30:00",
      "user_id": "uuid",
      "application_count": 5
    }
  ],
  "count": 1
}
```

### 3. Download Backup

**Endpoint**: `GET /api/applications/backup/download/<filename>`

**Description**: Download a backup file.

**Response**: File download (application/json)

### 4. Restore Backup

**Endpoint**: `POST /api/applications/backup/restore`

**Description**: Restore applications from a backup file.

**Request Body** (Option 1 - from file):
```json
{
  "filename": "backup_user_123_20251208_103000.json"
}
```

**Request Body** (Option 2 - from data):
```json
{
  "backup_data": { /* full backup data object */ }
}
```

**Response**:
```json
{
  "success": true,
  "message": "Backup restored successfully",
  "results": {
    "applications_restored": 5,
    "tasks_restored": 15,
    "documents_restored": 8,
    "errors": []
  }
}
```

### 5. Delete Backup

**Endpoint**: `DELETE /api/applications/backup/delete/<filename>`

**Description**: Delete a backup file.

**Response**:
```json
{
  "success": true,
  "message": "Backup deleted successfully"
}
```

### 6. Get Backup Info

**Endpoint**: `GET /api/applications/backup/info/<filename>`

**Description**: Get detailed information about a backup without downloading.

**Response**:
```json
{
  "success": true,
  "backup_metadata": { /* metadata object */ },
  "application_count": 5,
  "sample_applications": [ /* first 3 applications */ ]
}
```

---

## Frontend Usage

### Opening Backup Management

From the Applications page, click the "Backup & Recovery" button in the top right.

### Creating a Backup

1. Click "Create New Backup" button
2. Wait for the backup to complete
3. Success message will display the number of applications backed up
4. The new backup will appear in the list

### Restoring a Backup

1. Locate the backup you want to restore in the list
2. Click the "Restore" button
3. Confirm the restoration
4. View the restoration results showing:
   - Number of applications restored
   - Number of tasks restored
   - Number of documents restored
   - Any errors that occurred

**Important**: Restoring a backup will update existing applications with matching IDs or insert new ones.

### Downloading a Backup

1. Click the "Download" button on any backup
2. The JSON file will be downloaded to your default downloads folder
3. Keep these files in a safe location for disaster recovery

### Deleting a Backup

1. Click the "Delete" button on any backup
2. Confirm the deletion
3. The backup file will be permanently removed

---

## Backend Implementation

### Business Logic Functions

Located in: `Phase2_work/src/application_functions/backup_operations.py`

#### Key Functions:

**`create_backup_for_user(user_id: str) -> Dict`**
- Creates a complete backup of all applications for a user
- Includes tasks, documents, grant info, and user info
- Returns a dictionary with backup data

**`save_backup_to_file(backup_data: Dict, user_id: str, backup_dir: str) -> str`**
- Saves backup data to a JSON file
- Generates filename with timestamp
- Returns the file path

**`load_backup_from_file(filepath: str) -> Dict`**
- Loads backup data from a JSON file
- Returns backup data dictionary

**`restore_backup_for_user(backup_data: Dict) -> Dict`**
- Restores complete backup for a user
- Restores applications, tasks, and documents
- Returns restoration results with counts and errors

**`list_available_backups(backup_dir: str, user_id: Optional[str]) -> List[Dict]`**
- Lists all available backup files
- Can filter by user_id
- Returns list of backup file information

### SQL Queries

Located in: `Phase2_work/src/db_crud/applications/`

- `backup_applications_by_user.sql` - Backup all applications for a user
- `backup_application_tasks.sql` - Backup tasks for an application
- `backup_application_documents.sql` - Backup document metadata
- `restore_application.sql` - Restore a single application
- `restore_application_task.sql` - Restore a single task
- `restore_application_document.sql` - Restore document metadata

All restore queries use `INSERT ... ON DUPLICATE KEY UPDATE` to handle conflicts gracefully.

---

## File Structure

```
GrantGuru/
├── backups/                                    # Backup files directory
│   └── backup_user_<uuid>_<timestamp>.json   # Individual backup files
│
├── Phase2_work/
│   └── src/
│       ├── application_functions/
│       │   └── backup_operations.py          # Business logic
│       └── db_crud/applications/
│           ├── backup_applications_by_user.sql
│           ├── backup_application_tasks.sql
│           ├── backup_application_documents.sql
│           ├── restore_application.sql
│           ├── restore_application_task.sql
│           └── restore_application_document.sql
│
└── Phase3_work/
    ├── api/applications/
    │   └── routes_backup.py                   # API endpoints
    └── UI/frontend/components/
        ├── BackupManagement.tsx               # Backup UI component
        └── ApplicationsPage.tsx               # Integration point
```

---

## Backup Format

Backups are stored as JSON files with the following structure:

```json
{
  "backup_metadata": {
    "timestamp": "2025-12-08T10:30:00.000000",
    "user_id": "uuid-string",
    "backup_version": "1.0",
    "application_count": 5,
    "total_tasks": 15,
    "total_documents": 8
  },
  "applications": [
    {
      "application_id": "uuid-string",
      "user_id": "uuid-string",
      "grant_id": "uuid-string",
      "submission_status": "started",
      "status": "pending",
      "application_date": "2025-12-01",
      "submitted_at": null,
      "internal_deadline": "2025-12-31",
      "notes": "Application notes",
      "grant_info": {
        "grant_title": "Grant Title",
        "opportunity_number": "OPP-123",
        "provider": "Provider Name",
        "award_max_amount": 100000,
        "award_min_amount": 50000
      },
      "user_info": {
        "email": "user@example.com",
        "f_name": "John",
        "l_name": "Doe",
        "institution": "University"
      }
    }
  ],
  "tasks": {
    "application-uuid": [
      {
        "task_id": "uuid-string",
        "application_id": "uuid-string",
        "task_name": "Task name",
        "task_description": "Description",
        "deadline": "2025-12-15",
        "completed": false,
        "created_at": "2025-12-01T10:00:00",
        "updated_at": "2025-12-01T10:00:00"
      }
    ]
  },
  "documents": {
    "application-uuid": [
      {
        "document_id": "uuid-string",
        "application_id": "uuid-string",
        "document_name": "document.pdf",
        "document_type": "pdf",
        "document_size": 12345,
        "upload_date": "2025-12-01T10:00:00"
      }
    ]
  }
}
```

---

## Recovery Procedures

### Disaster Recovery

If the database is lost or corrupted:

1. **Restore Database Structure**
   ```bash
   cd Phase2_work
   python src/system_functions/create_db_script.py
   ```

2. **Restore from Backup via UI**
   - Log in to the application
   - Navigate to Applications > Backup & Recovery
   - Upload or select a backup file
   - Click "Restore"

3. **Restore from Backup via API** (if UI unavailable)
   ```bash
   curl -X POST http://127.0.0.1:5000/api/applications/backup/restore \
     -H "Content-Type: application/json" \
     -d '{"filename": "backup_user_<uuid>_<timestamp>.json"}'
   ```

### Migrating to New Environment

1. Copy all backup files from `backups/` directory
2. Set up new database and application
3. Use the restore procedure above

### Rolling Back Changes

1. Create a backup before making major changes
2. If changes cause issues, restore the previous backup
3. Review restoration results for any conflicts

---

## Best Practices

### Backup Frequency

- **Daily**: For active grant application periods
- **Weekly**: For normal usage
- **Before Major Changes**: Always backup before:
  - Bulk updates
  - Status changes
  - Deletions
  - System upgrades

### Backup Retention

- Keep at least 3-5 recent backups
- Keep weekly backups for 1 month
- Keep monthly backups for 1 year
- Archive important milestones indefinitely

### Security

- Backup files contain sensitive data
- Store backups in secure locations
- Use encryption for backup storage
- Limit access to backup files
- Don't share backup files via insecure channels

### Automation

Consider setting up automated backups:

```python
# Example cron job (Linux/Mac)
# Run daily at 2 AM
0 2 * * * curl -X POST http://127.0.0.1:5000/api/applications/backup/create/<user_id>
```

### Testing

- Test restoration periodically (monthly recommended)
- Verify backup integrity
- Practice disaster recovery procedures
- Document recovery times

---

## Troubleshooting

### Backup Creation Fails

**Problem**: Backup creation returns an error

**Solutions**:
1. Check database connectivity
2. Verify user_id exists
3. Check disk space in backups directory
4. Review backend logs for SQL errors

### Restore Fails

**Problem**: Restore operation fails or returns errors

**Solutions**:
1. Verify backup file is valid JSON
2. Check for foreign key constraint violations
3. Ensure grants referenced in backup exist
4. Review error messages in restoration results
5. Try restoring to a test environment first

### Backup File Too Large

**Problem**: Backup file exceeds reasonable size

**Solutions**:
1. This is normal for users with many applications
2. Consider archiving old applications
3. Split backups by date range if needed
4. Compress backup files for storage

### Missing Backup Directory

**Problem**: Backups fail with "directory not found"

**Solution**:
```bash
mkdir -p backups
chmod 755 backups
```

### Permission Denied

**Problem**: Cannot read/write backup files

**Solution**:
```bash
chmod 755 backups
chmod 644 backups/*.json
```

### Backup Restoration Partial Success

**Problem**: Some items restored, others failed

**Solutions**:
1. Review the errors array in restoration results
2. Common issues:
   - Missing grant references (restore grants first)
   - Duplicate key violations (expected for updates)
   - Foreign key constraints
3. Failed items can be restored individually after fixing issues

---

## Advanced Usage

### Manual Backup Editing

Backup files are JSON and can be edited manually:

1. Download a backup
2. Edit with a text editor
3. Restore the edited backup

**Warning**: Ensure JSON remains valid and all required fields are present.

### Selective Restoration

To restore only specific applications:

1. Download a backup
2. Edit the JSON to include only desired applications
3. Update the backup_metadata counts
4. Restore the modified backup

### Backup Comparison

To compare two backups:

```bash
diff backup1.json backup2.json
```

Or use a JSON diff tool for better formatting.

---

## API Authentication

**Note**: Current implementation does not include authentication on backup endpoints. For production use:

1. Add JWT authentication middleware
2. Verify user owns the backup being accessed
3. Implement rate limiting
4. Add audit logging

---

## Support

For issues or questions:

1. Check this documentation
2. Review API error messages
3. Check backend logs
4. Contact system administrator

---

## Version History

- **v1.0** (2025-12-08): Initial implementation
  - Create, list, download, restore, delete backups
  - Support for applications, tasks, and documents
  - Web UI integration

---

## Future Enhancements

Potential improvements for future versions:

- [ ] Automated scheduled backups
- [ ] Backup encryption
- [ ] Cloud storage integration (S3, Azure Blob)
- [ ] Incremental backups
- [ ] Backup compression
- [ ] Email notifications for backup events
- [ ] Backup versioning and diffs
- [ ] Document file content backup (not just metadata)
- [ ] Multi-user bulk restore
- [ ] Backup validation and integrity checks

---

## License

Copyright © 2025 GrantGuru. All rights reserved.
