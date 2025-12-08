import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import DOMPurify from "dompurify";
const API_BASE_URL = "http://127.0.0.1:5000";

export function GrantsSearchPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [researchField, setResearchField] = useState("");
  const [opportunityNum, setOpportunityNum] = useState(""); // <--- NEW STATE
  const [sortBy, setSortBy] = useState("title_asc");
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
      if (field) params.set("field", field);
      if (opNum) params.set("op_num", opNum); // <--- Add to URL params
      params.set("sort_by", sort);

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
        console.error("Failed to parse JSON", e);
        setError("Invalid JSON response");
        setResults([]);
        return;
      }

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
    fetchResults(query.trim(), researchField.trim(), opportunityNum.trim(), sortBy, 1);
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = e.target.value;
    setSortBy(newSort);
    fetchResults(query.trim(), researchField.trim(), opportunityNum.trim(), newSort, 1);
  };

  useEffect(() => {
    fetchResults("", "", "", "title_asc", 1);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
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
        
        {/* LAYOUT: Flex column on mobile, Row on Desktop */}
        <form onSubmit={doSearch} className="flex flex-col md:flex-row gap-2 mb-4">
          
          {/* Main Search - Flex 1 fills remaining space */}
          <input
            className="flex-1 p-2 rounded border dark:bg-slate-900 dark:border-slate-700 min-w-[200px]"
            placeholder="Search title/desc..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          
          {/* Opportunity Number - Fixed width on Desktop */}
          <input
            className="w-full md:w-36 shrink-0 p-2 rounded border dark:bg-slate-900 dark:border-slate-700"
            placeholder="Opp #"
            value={opportunityNum}
            onChange={(e) => setOpportunityNum(e.target.value)}
          />

          {/* Research Field - Fixed width on Desktop */}
          <input
            className="w-full md:w-36 shrink-0 p-2 rounded border dark:bg-slate-900 dark:border-slate-700"
            placeholder="Field"
            value={researchField}
            onChange={(e) => setResearchField(e.target.value)}
          />
          
          {/* Sort Dropdown - Auto width */}
          <select
            className="w-full md:w-auto shrink-0 p-2 rounded border dark:bg-slate-900 dark:border-slate-700 cursor-pointer"
            value={sortBy}
            onChange={handleSortChange}
          >
            <option value="title_asc">Title (A-Z)</option>
            <option value="title_desc">Title (Z-A)</option>
            <option value="posted_date_desc">Newest</option>
            <option value="posted_date_asc">Oldest</option>
            <option value="close_date_asc">Deadline (Soon)</option>
            <option value="close_date_desc">Deadline (Late)</option>
          </select>

          <button className="px-6 py-2 bg-slate-700 text-white rounded hover:bg-slate-600 md:w-auto w-full" disabled={loading}>
            {loading ? "..." : "Search"}
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
            </>
          ) : (
            results.map((g) => (
              <Link key={g.grant_id} to={`/grant/${g.grant_id}`} className="block p-4 border rounded hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                <div className="flex justify-between items-start">
                    <div className="font-medium dark:text-white text-lg">{g.grant_title}</div>
                    <div className="flex flex-col items-end gap-1">
                         {/* Display Op# if matched? Optional, but helpful context */}
                         {g.opportunity_number && (
                           <span className="text-xs text-slate-500 font-mono">#{g.opportunity_number}</span>
                         )}
                        {g.research_field && (
                            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded dark:bg-blue-900 dark:text-blue-200 whitespace-nowrap">
                                {g.research_field}
                            </span>
                        )}
                    </div>
                </div>
                <div className="text-sm text-slate-600 dark:text-slate-400 mt-1 flex gap-2 items-center flex-wrap">
                   <span className="font-semibold">{g.provider}</span> 
                   <span className="text-slate-300 dark:text-slate-600">•</span>
                   <span>Posted: {g.date_posted || "N/A"}</span>
                   <span className="text-slate-300 dark:text-slate-600">•</span>
                   <span>Deadline: {g.date_closed || "No Deadline"}</span>
                </div>
                <div
                  className="text-sm text-slate-700 dark:text-slate-300 mt-2 line-clamp-2"
                  dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(g.description || "") }}
                />
              </Link>
            ))
          )}
        </div>

        {/* Pagination controls */}
        {total !== null && total > PAGE_SIZE && (
          <div className="flex items-center justify-between mt-6 pt-4 border-t dark:border-slate-800">
            <div className="text-sm text-slate-600 dark:text-slate-400">
                Page {page} of {Math.ceil(total / PAGE_SIZE)} 
                <span className="mx-2 text-slate-300">|</span> 
                {total} results
            </div>
            <div className="flex gap-2">
              <button 
                className="px-4 py-2 border rounded hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:hover:bg-transparent transition-colors" 
                onClick={() => fetchResults(query.trim(), researchField.trim(), opportunityNum.trim(), sortBy, page - 1)} 
                disabled={page <= 1 || loading}
              >
                Previous
              </button>
              <button 
                className="px-4 py-2 border rounded hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-50 disabled:hover:bg-transparent transition-colors" 
                onClick={() => fetchResults(query.trim(), researchField.trim(), opportunityNum.trim(), sortBy, page + 1)} 
                disabled={page * PAGE_SIZE >= total || loading}
              >
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