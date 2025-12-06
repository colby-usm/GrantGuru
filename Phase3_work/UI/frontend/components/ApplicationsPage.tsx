import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { ThemeToggle } from './ThemeToggle';

const API_BASE_URL = 'http://127.0.0.1:5000';

export function ApplicationsPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [applications, setApplications] = useState<Array<any>>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [grants, setGrants] = useState<Array<any>>([]);
  const [selectedGrantId, setSelectedGrantId] = useState('');
  const [creatingApp, setCreatingApp] = useState(false);
  const [createError, setCreateError] = useState<string | null>(null);

  const userId = localStorage.getItem('user_id') || sessionStorage.getItem('user_id');

  useEffect(() => {
    if (!userId) {
      navigate('/');
      return;
    }

    const fetchApps = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/api/applications/user/${userId}`);
        const data = await res.json();
        if (!res.ok) {
          setError(data.error || 'Failed to load applications');
          setApplications([]);
        } else {
          setApplications(data.applications || []);
        }
      } catch (err: any) {
        setError(err?.message || String(err));
      } finally {
        setLoading(false);
      }
    };

    fetchApps();
  }, [userId, navigate]);

  const fetchGrants = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/applications/grants`);
      const data = await res.json();
      if (res.ok) {
        setGrants(data.grants || []);
      }
    } catch (err) {
      console.error('Failed to fetch grants:', err);
    }
  };

  const handleOpenCreateModal = async () => {
    setShowCreateModal(true);
    setCreateError(null);
    setSelectedGrantId('');
    await fetchGrants();
  };

  const handleCreateApplication = async () => {
    if (!selectedGrantId) {
      setCreateError('Please select a grant');
      return;
    }

    setCreatingApp(true);
    setCreateError(null);

    try {
      const res = await fetch(`${API_BASE_URL}/api/applications/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          grant_id: selectedGrantId,
          status: 'pending'
        })
      });

      const data = await res.json();

      if (!res.ok) {
        setCreateError(data.error || 'Failed to create application');
        return;
      }

      // Refresh applications list
      const appRes = await fetch(`${API_BASE_URL}/api/applications/user/${userId}`);
      const appData = await appRes.json();
      if (appRes.ok) {
        setApplications(appData.applications || []);
      }

      setShowCreateModal(false);
      setSelectedGrantId('');
    } catch (err: any) {
      setCreateError(err?.message || String(err));
    } finally {
      setCreatingApp(false);
    }
  };

  const filteredApplications = applications.filter((app) => {
    const query = searchQuery.toLowerCase();
    return (
      app.application_id.toLowerCase().includes(query) ||
      app.grant_id.toLowerCase().includes(query) ||
      app.status.toLowerCase().includes(query) ||
      app.application_date.toLowerCase().includes(query)
    );
  });

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">My Applications</span>
          </div>
          <div className="flex items-center gap-3">
            <ThemeToggle />
            <Link to="/homepage">
              <Button variant="ghost">Home</Button>
            </Link>
            <Link to="/user">
              <Button variant="ghost">User Settings</Button>
            </Link>
            <Button variant="outline" onClick={handleLogout}>Logout</Button>
          </div>
        </div>
      </nav>

      <main className="flex-1 container mx-auto px-4 py-12">
        <Card className="p-6 dark:bg-slate-800 dark:border-slate-700">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl dark:text-white">Your Applications</h2>
            <Button onClick={handleOpenCreateModal} className="bg-blue-600 hover:bg-blue-700">
              + Create Application
            </Button>
          </div>

          {/* Search Box */}
          {!loading && applications.length > 0 && (
            <div className="mb-4">
              <Input
                type="text"
                placeholder="Search by ID, grant, status, or date..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="dark:bg-slate-900 dark:border-slate-600 dark:text-white"
              />
            </div>
          )}

          {loading && <p className="text-slate-600 dark:text-slate-300">Loading...</p>}
          {error && <p className="text-red-600 dark:text-red-400">{error}</p>}

          {!loading && !error && applications.length === 0 && (
            <p className="text-slate-600 dark:text-slate-300">You have no applications.</p>
          )}

          {!loading && !error && filteredApplications.length === 0 && applications.length > 0 && (
            <p className="text-slate-600 dark:text-slate-300">No applications match your search.</p>
          )}

          {!loading && !error && filteredApplications.length > 0 && (
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="text-slate-700 dark:text-slate-300">
                    <th className="p-2">Application ID</th>
                    <th className="p-2">Grant ID</th>
                    <th className="p-2">Status</th>
                    <th className="p-2">Date</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredApplications.map((app) => (
                    <tr key={app.application_id} className="border-t dark:border-slate-700">
                      <td className="p-2 text-sm text-slate-700 dark:text-slate-200">{app.application_id}</td>
                      <td className="p-2 text-sm text-slate-700 dark:text-slate-200">{app.grant_id}</td>
                      <td className="p-2 text-sm text-slate-700 dark:text-slate-200">{app.status}</td>
                      <td className="p-2 text-sm text-slate-700 dark:text-slate-200">{app.application_date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Card>

        {/* Create Application Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="p-6 w-96 dark:bg-slate-800 dark:border-slate-700">
              <h3 className="text-xl font-semibold mb-4 dark:text-white">Create New Application</h3>

              {createError && <p className="text-red-600 dark:text-red-400 mb-4">{createError}</p>}

              <div className="mb-4">
                <label className="block text-sm font-medium mb-2 dark:text-slate-200">Select a Grant</label>
                <select
                  value={selectedGrantId}
                  onChange={(e) => setSelectedGrantId(e.target.value)}
                  className="w-full p-2 border border-slate-300 rounded dark:bg-slate-900 dark:border-slate-600 dark:text-white"
                >
                  <option value="">-- Choose a grant --</option>
                  {grants.map((grant) => (
                    <option key={grant.grant_id} value={grant.grant_id}>
                      {grant.program_title}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handleCreateApplication}
                  disabled={creatingApp || !selectedGrantId}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                >
                  {creatingApp ? 'Creating...' : 'Create'}
                </Button>
                <Button
                  onClick={() => setShowCreateModal(false)}
                  variant="outline"
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </Card>
          </div>
        )}
      </main>

      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default ApplicationsPage;
