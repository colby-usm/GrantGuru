"""
Backup and Recovery API Routes for Applications

This module provides REST API endpoints for backing up and restoring
application data.
"""

from flask import Blueprint, jsonify, request, send_file
from pathlib import Path
import os
import sys

# Add the Phase2_work directory to the path to import backend modules
phase2_path = Path(__file__).parent.parent.parent.parent / "Phase2_work"
sys.path.insert(0, str(phase2_path))

from src.application_functions.backup_operations import (
    create_backup_for_user,
    save_backup_to_file,
    load_backup_from_file,
    restore_backup_for_user,
    list_available_backups
)

from . import applications_bp

# Configure backup directory - use absolute path relative to project root
BACKUP_DIR = os.path.join(str(phase2_path.parent), "backups")


@applications_bp.route('/backup/create/<user_id>', methods=['POST'])
def create_backup(user_id):
    """
    Create a backup of all applications for a specific user.

    Request:
        POST /api/applications/backup/create/<user_id>
        Optional JSON body:
        {
            "save_to_file": true,  // Save to file (default: true)
            "return_data": false   // Return full backup data in response (default: false)
        }

    Response:
        {
            "success": true,
            "message": "Backup created successfully",
            "backup_metadata": {
                "timestamp": "2025-12-08T10:30:00",
                "user_id": "uuid",
                "application_count": 5,
                "total_tasks": 15,
                "total_documents": 8
            },
            "filepath": "/path/to/backup.json"  // If saved to file
        }
    """
    try:
        # Get request options
        data = request.get_json() or {}
        save_to_file_flag = data.get('save_to_file', True)
        return_data_flag = data.get('return_data', False)

        # Create backup
        backup_data = create_backup_for_user(user_id)

        response = {
            "success": True,
            "message": "Backup created successfully",
            "backup_metadata": backup_data["backup_metadata"]
        }

        # Save to file if requested
        if save_to_file_flag:
            filepath = save_backup_to_file(backup_data, user_id, BACKUP_DIR)
            response["filepath"] = filepath
            response["filename"] = os.path.basename(filepath)

        # Include full backup data if requested
        if return_data_flag:
            response["backup_data"] = backup_data

        return jsonify(response), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to create backup: {str(e)}"
        }), 500


@applications_bp.route('/backup/list', methods=['GET'])
@applications_bp.route('/backup/list/<user_id>', methods=['GET'])
def list_backups(user_id=None):
    """
    List all available backup files.

    Request:
        GET /api/applications/backup/list
        GET /api/applications/backup/list/<user_id>

    Response:
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
    """
    try:
        backups = list_available_backups(BACKUP_DIR, user_id)

        return jsonify({
            "success": True,
            "backups": backups,
            "count": len(backups)
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to list backups: {str(e)}"
        }), 500


@applications_bp.route('/backup/download/<filename>', methods=['GET'])
def download_backup(filename):
    """
    Download a backup file.

    Request:
        GET /api/applications/backup/download/<filename>

    Response:
        File download or error JSON
    """
    try:
        # Security: Prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                "success": False,
                "error": "Invalid filename"
            }), 400

        filepath = os.path.join(BACKUP_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({
                "success": False,
                "error": "Backup file not found"
            }), 404

        return send_file(
            filepath,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to download backup: {str(e)}"
        }), 500


@applications_bp.route('/backup/restore', methods=['POST'])
def restore_backup():
    """
    Restore applications from a backup file or backup data.

    Request:
        POST /api/applications/backup/restore
        JSON body (option 1 - from file):
        {
            "filename": "backup_user_123_20251208_103000.json"
        }

        JSON body (option 2 - from uploaded data):
        {
            "backup_data": { ... full backup data ... }
        }

    Response:
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
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        # Load backup data from file or request
        if "filename" in data:
            filename = data["filename"]

            # Security: Prevent directory traversal
            if '..' in filename or '/' in filename or '\\' in filename:
                return jsonify({
                    "success": False,
                    "error": "Invalid filename"
                }), 400

            filepath = os.path.join(BACKUP_DIR, filename)

            if not os.path.exists(filepath):
                return jsonify({
                    "success": False,
                    "error": "Backup file not found"
                }), 404

            backup_data = load_backup_from_file(filepath)

        elif "backup_data" in data:
            backup_data = data["backup_data"]

        else:
            return jsonify({
                "success": False,
                "error": "Must provide either 'filename' or 'backup_data'"
            }), 400

        # Restore the backup
        results = restore_backup_for_user(backup_data)

        return jsonify({
            "success": results["success"],
            "message": "Backup restored successfully" if results["success"] else "Backup restored with errors",
            "results": results
        }), 200 if results["success"] else 207  # 207 Multi-Status if partial success

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to restore backup: {str(e)}"
        }), 500


@applications_bp.route('/backup/delete/<filename>', methods=['DELETE'])
def delete_backup(filename):
    """
    Delete a backup file.

    Request:
        DELETE /api/applications/backup/delete/<filename>

    Response:
        {
            "success": true,
            "message": "Backup deleted successfully"
        }
    """
    try:
        # Security: Prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                "success": False,
                "error": "Invalid filename"
            }), 400

        filepath = os.path.join(BACKUP_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({
                "success": False,
                "error": "Backup file not found"
            }), 404

        os.remove(filepath)

        return jsonify({
            "success": True,
            "message": "Backup deleted successfully"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to delete backup: {str(e)}"
        }), 500


@applications_bp.route('/backup/info/<filename>', methods=['GET'])
def get_backup_info(filename):
    """
    Get detailed information about a backup file without downloading it.

    Request:
        GET /api/applications/backup/info/<filename>

    Response:
        {
            "success": true,
            "backup_metadata": { ... },
            "application_count": 5,
            "sample_applications": [ ... first 3 applications ... ]
        }
    """
    try:
        # Security: Prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({
                "success": False,
                "error": "Invalid filename"
            }), 400

        filepath = os.path.join(BACKUP_DIR, filename)

        if not os.path.exists(filepath):
            return jsonify({
                "success": False,
                "error": "Backup file not found"
            }), 404

        backup_data = load_backup_from_file(filepath)

        # Return metadata and sample data
        response = {
            "success": True,
            "backup_metadata": backup_data.get("backup_metadata", {}),
            "application_count": len(backup_data.get("applications", [])),
            "sample_applications": backup_data.get("applications", [])[:3]  # First 3 apps
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Failed to get backup info: {str(e)}"
        }), 500
