import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import DOMPurify from "dompurify";
const API_BASE_URL = "http://127.0.0.1:5000";

export function GrantsSearchPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Array<any>>([]);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number | null>(null);
  const PAGE_SIZE = 10;
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [debugText, setDebugText] = useState<string | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);

  const handleLogout = () => {
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("access_token");
    navigate("/");
  };

  const fetchResults = async (q = "", p = 1) => {
    setError(null);
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.set("page", String(p));
      params.set("page_size", String(PAGE_SIZE));
      if (q) params.set("q", q);
      const url = `${API_BASE_URL}/api/public/search_grants?${params.toString()}`;
      const res = await fetch(url);
      setStatusCode(res.status);

      const text = await res.text();
      setDebugText(text.slice(0, 20000));

      if (!res.ok) {
        setError(`HTTP ${res.status}`);
        setResults([]);
        return;
      }

      let data: any = null;
      try {
        data = JSON.parse(text);
      } catch (e) {
        console.error("Failed to parse JSON from response", e);
        setError("Invalid JSON response from API");
        setResults([]);
        return;
      }

      console.debug("search_grants response:", data);
      setResults(data.grants || []);
      setTotal(typeof data.total === "number" ? data.total : null);
      setPage(typeof data.page === "number" ? data.page : p);
    } catch (err) {
      console.error(err);
      setError("Search failed");
      setDebugText(String(err));
    } finally {
      setLoading(false);
    }
  };

  const doSearch = (e?: React.FormEvent) => {
    e?.preventDefault();
    fetchResults(query.trim(), 1);
  };

  React.useEffect(() => {
    // Fetch initial top 10 alphabetical grants (page 1)
    fetchResults("", 1);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Search Grants</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/homepage">
              <Button variant="ghost">Home</Button>
            </Link>
            <Link to="/searchGrants">
              <Button variant="ghost">Search Grants</Button>
            </Link>
            <Link to="/user">
              <Button variant="ghost">User Settings</Button>
            </Link>
            <Button variant="outline" onClick={handleLogout}>Logout</Button>
          </div>
        </div>
      </nav>

    <div className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-semibold dark:text-white mb-4">Search Grants</h1>
      <form onSubmit={doSearch} className="flex gap-2 mb-4">
        <input
          className="flex-1 p-2 rounded border dark:bg-slate-900 dark:border-slate-700"
          placeholder="Search by title or description..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button className="px-4 py-2 bg-slate-700 text-white rounded" disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && <div className="text-red-500 mb-4">{error}</div>}

      <div className="grid gap-3">
        {results.length === 0 ? (
          <>
            <div className="text-slate-500">No results.</div>
            {statusCode !== null && (
              <div className="text-xs text-slate-500 mt-2">API status: {statusCode}</div>
            )}
            {debugText && (
              <details className="mt-2 p-2 border rounded bg-slate-50 dark:bg-slate-800">
                <summary className="text-sm text-slate-700 dark:text-slate-300">Show API response (debug)</summary>
                <pre className="text-xs overflow-auto whitespace-pre-wrap mt-2">{debugText}</pre>
              </details>
            )}
          </>
        ) : (
          results.map((g) => (
            <Link key={g.grant_id} to={`/grant/${g.grant_id}`} className="block p-4 border rounded hover:bg-slate-50 dark:hover:bg-slate-800">
              <div className="font-medium dark:text-white">{g.grant_title}</div>
              <div className="text-sm text-slate-600 dark:text-slate-400">{g.provider} — {g.date_closed || "no deadline"}</div>
              <div
                className="text-sm text-slate-700 dark:text-slate-300 mt-1 line-clamp-3"
                dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(g.description || "") }}
              />
            </Link>
          ))
        )}
      </div>

      {/* Pagination controls */}
      {total !== null && total > PAGE_SIZE && (
        <div className="flex items-center justify-between mt-4">
          <div className="text-sm text-slate-600">Page {page} of {Math.ceil(total / PAGE_SIZE)}</div>
          <div className="flex gap-2">
            <button className="px-3 py-1 border rounded" onClick={() => fetchResults(query.trim(), page - 1)} disabled={page <= 1 || loading}>
              Previous
            </button>
            <button className="px-3 py-1 border rounded" onClick={() => fetchResults(query.trim(), page + 1)} disabled={page * PAGE_SIZE >= total || loading}>
              Next
            </button>
          </div>
        </div>
      )}
    </div>
    </div>
  );
}

export default GrantsSearchPage;
