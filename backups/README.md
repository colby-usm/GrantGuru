# GrantGuru Backups Directory

This directory contains backup files for GrantGuru application data.

## Backup Files

Backup files are stored in JSON format with the naming convention:
```
backup_user_<user_id>_<timestamp>.json
```

Example: `backup_user_123e4567-e89b-12d3-a456-426614174000_20251208_143000.json`

## Contents

Each backup file contains:
- Application records
- Associated tasks
- Document metadata
- Grant information (for context)
- User information (for verification)

**Note**: Actual document file contents are NOT included, only metadata.

## Managing Backups

### Via Web Interface

1. Navigate to Applications page
2. Click "Backup & Recovery" button
3. Use the interface to:
   - Create new backups
   - View existing backups
   - Download backups
   - Restore from backups
   - Delete old backups

### Via API

See the main documentation at: `/BACKUP_RECOVERY_DOCUMENTATION.md`

## Important Notes

- **Keep backups secure**: These files contain sensitive application data
- **Regular backups**: Create backups before major changes
- **Test restores**: Periodically test backup restoration
- **Storage**: Ensure sufficient disk space for backup files

## File Size

Typical backup sizes:
- Small (1-10 applications): 10-50 KB
- Medium (10-50 applications): 50-200 KB
- Large (50+ applications): 200 KB - 2 MB

## Retention Policy

Recommended:
- Keep last 5 daily backups
- Keep last 4 weekly backups
- Keep last 12 monthly backups
- Archive important milestones

## Disaster Recovery

If you need to restore from backup:

1. Ensure database is running
2. Use the Web UI or API to restore
3. Verify restoration results
4. Check for any errors in the restoration report

For detailed instructions, see `/BACKUP_RECOVERY_DOCUMENTATION.md`

## Support

For issues or questions about backups, consult the main documentation or contact your system administrator.

---

**Last Updated**: 2025-12-08
