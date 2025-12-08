import React, { useEffect, useState } from "react";
import DOMPurify from "dompurify";
import { useParams, Link } from "react-router-dom";

const API_BASE_URL = "http://127.0.0.1:5000";

export function GrantDetailsPage() {
  const { id } = useParams();
  const [grant, setGrant] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    setError(null);

    fetch(`${API_BASE_URL}/api/public/grant/${id}`)
      .then((r) => r.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
        } else {
          setGrant(data.grant || null);
        }
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load grant");
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6 text-red-500">{error}</div>;
  if (!grant) return <div className="p-6">Grant not found.</div>;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Grant Details</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/homepage">
              <button className="px-3 py-1 text-sm rounded hover:bg-slate-100 dark:hover:bg-slate-800">Home</button>
            </Link>
            <Link to="/searchGrants">
              <button className="px-3 py-1 text-sm rounded hover:bg-slate-100 dark:hover:bg-slate-800">Search Grants</button>
            </Link>
            <Link to="/user">
              <button className="px-3 py-1 text-sm rounded hover:bg-slate-100 dark:hover:bg-slate-800">User Settings</button>
            </Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8 px-4">
      <div className="mb-4">
        <Link to="/searchGrants" className="text-slate-600 dark:text-slate-300">← Back to search</Link>
      </div>
      <h1 className="text-3xl font-bold dark:text-white">{grant.grant_title}</h1>
      <div className="text-sm text-slate-600 dark:text-slate-400">Provided by {grant.provider}</div>
      <div className="mt-4 prose dark:prose-invert max-w-none">
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(grant.description || "") }} />
        <dl>
          <dt className="font-medium">Opportunity #</dt>
          <dd>{grant.opportunity_number || "—"}</dd>
          <dt className="font-medium">Research Field</dt>
          <dd>{grant.research_field || "—"}</dd>
          <dt className="font-medium">Award Range</dt>
          <dd>{grant.award_min_amount || "—"} — {grant.award_max_amount || "—"}</dd>
          <dt className="font-medium">Deadline</dt>
          <dd>{grant.date_closed || "—"}</dd>
        </dl>
        {grant.link_to_source && (
          <p>
            <a href={grant.link_to_source} target="_blank" rel="noreferrer" className="text-blue-600 break-all hover:underline">
              {grant.link_to_source}
            </a>
          </p>
        )}
      </div>
    </div>
  </div>
  );
}

export default GrantDetailsPage;
