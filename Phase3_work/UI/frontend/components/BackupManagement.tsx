import React, { useState, useEffect } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';

const API_BASE_URL = 'http://127.0.0.1:5000';

interface BackupMetadata {
  timestamp: string;
  user_id: string;
  application_count: number;
  total_tasks?: number;
  total_documents?: number;
  backup_version: string;
}

interface BackupFile {
  filename: string;
  filepath: string;
  size: number;
  created: string;
  modified?: string;
  timestamp?: string;
  application_count?: number;
}

interface BackupManagementProps {
  userId: string;
  onClose?: () => void;
}

export function BackupManagement({ userId, onClose }: BackupManagementProps) {
  const [backups, setBackups] = useState<BackupFile[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [selectedBackup, setSelectedBackup] = useState<string | null>(null);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [actionType, setActionType] = useState<'restore' | 'delete' | null>(null);
  const [restoreResults, setRestoreResults] = useState<any>(null);

  useEffect(() => {
    loadBackups();
  }, [userId]);

  const loadBackups = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/applications/backup/list/${userId}`);
      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Failed to load backups');
        setBackups([]);
      } else {
        setBackups(data.backups || []);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to load backups');
      setBackups([]);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBackup = async () => {
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const res = await fetch(`${API_BASE_URL}/api/applications/backup/create/${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ save_to_file: true })
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || 'Failed to create backup');
        return;
      }

      setSuccessMessage(
        `Backup created successfully! ${data.backup_metadata.application_count} applications backed up.`
      );

      // Reload backups list
      await loadBackups();
    } catch (err: any) {
      setError(err?.message || 'Failed to create backup');
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadBackup = async (filename: string) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/applications/backup/download/${filename}`);

      if (!res.ok) {
        const data = await res.json();
        setError(data.error || 'Failed to download backup');
        return;
      }

      // Create blob and download
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      setSuccessMessage('Backup downloaded successfully!');
    } catch (err: any) {
      setError(err?.message || 'Failed to download backup');
    }
  };

  const handleRestoreBackup = async (filename: string) => {
    setSelectedBackup(filename);
    setActionType('restore');
    setShowConfirmDialog(true);
  };

  const handleDeleteBackup = async (filename: string) => {
    setSelectedBackup(filename);
    setActionType('delete');
    setShowConfirmDialog(true);
  };

  const confirmAction = async () => {
    if (!selectedBackup || !actionType) return;

    setLoading(true);
    setError(null);
    setSuccessMessage(null);
    setShowConfirmDialog(false);

    try {
      if (actionType === 'restore') {
        const res = await fetch(`${API_BASE_URL}/api/applications/backup/restore`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filename: selectedBackup })
        });

        const data = await res.json();

        if (!res.ok) {
          setError(data.error || 'Failed to restore backup');
          return;
        }

        setRestoreResults(data.results);
        setSuccessMessage(
          `Backup restored! Applications: ${data.results.applications_restored}, ` +
          `Tasks: ${data.results.tasks_restored}, Documents: ${data.results.documents_restored}`
        );

        if (data.results.errors && data.results.errors.length > 0) {
          setError(`Some errors occurred: ${data.results.errors.slice(0, 3).join(', ')}`);
        }
      } else if (actionType === 'delete') {
        const res = await fetch(`${API_BASE_URL}/api/applications/backup/delete/${selectedBackup}`, {
          method: 'DELETE'
        });

        const data = await res.json();

        if (!res.ok) {
          setError(data.error || 'Failed to delete backup');
          return;
        }

        setSuccessMessage('Backup deleted successfully!');
        await loadBackups();
      }
    } catch (err: any) {
      setError(err?.message || `Failed to ${actionType} backup`);
    } finally {
      setLoading(false);
      setSelectedBackup(null);
      setActionType(null);
    }
  };

  const cancelAction = () => {
    setShowConfirmDialog(false);
    setSelectedBackup(null);
    setActionType(null);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-4xl max-h-[90vh] overflow-y-auto dark:bg-slate-800 dark:border-slate-700">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold dark:text-white">Backup & Recovery</h2>
            <Button variant="ghost" onClick={onClose} className="text-slate-500">
              ✕
            </Button>
          </div>

          {/* Messages */}
          {error && (
            <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 rounded text-red-700 dark:text-red-300">
              {error}
            </div>
          )}

          {successMessage && (
            <div className="mb-4 p-3 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 rounded text-green-700 dark:text-green-300">
              {successMessage}
            </div>
          )}

          {/* Actions */}
          <div className="mb-6 flex gap-3">
            <Button
              onClick={handleCreateBackup}
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {loading ? 'Creating...' : 'Create New Backup'}
            </Button>
            <Button
              onClick={loadBackups}
              variant="outline"
              disabled={loading}
            >
              Refresh List
            </Button>
          </div>

          {/* Backups List */}
          <div>
            <h3 className="text-lg font-medium mb-3 dark:text-white">Available Backups</h3>

            {loading && <p className="text-slate-600 dark:text-slate-300">Loading...</p>}

            {!loading && backups.length === 0 && (
              <p className="text-slate-600 dark:text-slate-300">
                No backups found. Create your first backup to get started.
              </p>
            )}

            {!loading && backups.length > 0 && (
              <div className="space-y-3">
                {backups.map((backup) => (
                  <Card
                    key={backup.filename}
                    className="p-4 dark:bg-slate-700 dark:border-slate-600"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium dark:text-white mb-1">
                          {backup.filename}
                        </h4>
                        <div className="text-sm text-slate-600 dark:text-slate-300 space-y-1">
                          <p>Created: {formatDate(backup.created)}</p>
                          <p>Size: {formatFileSize(backup.size)}</p>
                          {backup.application_count !== undefined && (
                            <p>Applications: {backup.application_count}</p>
                          )}
                        </div>
                      </div>

                      <div className="flex gap-2 ml-4">
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleDownloadBackup(backup.filename)}
                          className="text-blue-600 dark:text-blue-400"
                        >
                          Download
                        </Button>
                        <Button
                          size="sm"
                          onClick={() => handleRestoreBackup(backup.filename)}
                          className="bg-green-600 hover:bg-green-700"
                        >
                          Restore
                        </Button>
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleDeleteBackup(backup.filename)}
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            )}
          </div>

          {/* Restore Results */}
          {restoreResults && (
            <div className="mt-6 p-4 bg-slate-100 dark:bg-slate-700 rounded">
              <h4 className="font-medium mb-2 dark:text-white">Restore Results</h4>
              <div className="text-sm dark:text-slate-200">
                <p>Applications Restored: {restoreResults.applications_restored}</p>
                <p>Tasks Restored: {restoreResults.tasks_restored}</p>
                <p>Documents Restored: {restoreResults.documents_restored}</p>
                {restoreResults.errors && restoreResults.errors.length > 0 && (
                  <div className="mt-2">
                    <p className="font-medium text-red-600 dark:text-red-400">Errors:</p>
                    <ul className="list-disc list-inside">
                      {restoreResults.errors.map((err: string, idx: number) => (
                        <li key={idx} className="text-red-600 dark:text-red-400">{err}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Confirmation Dialog */}
      {showConfirmDialog && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-[60]">
          <Card className="p-6 w-96 dark:bg-slate-800 dark:border-slate-700">
            <h3 className="text-xl font-semibold mb-4 dark:text-white">
              Confirm {actionType === 'restore' ? 'Restore' : 'Delete'}
            </h3>
            <p className="mb-6 dark:text-slate-200">
              {actionType === 'restore'
                ? 'Are you sure you want to restore this backup? This will add or update applications from the backup.'
                : 'Are you sure you want to delete this backup? This action cannot be undone.'}
            </p>
            <div className="flex gap-2">
              <Button
                onClick={confirmAction}
                className={actionType === 'restore' ? 'bg-green-600 hover:bg-green-700' : 'bg-red-600 hover:bg-red-700'}
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Confirm'}
              </Button>
              <Button onClick={cancelAction} variant="outline" disabled={loading}>
                Cancel
              </Button>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}

export default BackupManagement;
