import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableHead as TableHeadComp } from "./ui/table";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "./ui/card";

export default function SearchGrants() {
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [field, setField] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (field) params.set("field", field);
      const res = await fetch(`/api/public/search-grants?${params.toString()}`);
      const data = await res.json();
      if (data.results) setResults(data.results);
      else setResults([]);
    } catch (e) {
      console.error(e);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Search Grants</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={() => navigate('/homepage')}>Home</Button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto py-8 px-4">
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between w-full">
              <div>
                <CardTitle>Find Grants</CardTitle>
                <CardDescription>Search the grants database by keyword or research field.</CardDescription>
              </div>
              <div className="flex gap-2">
                <Input value={q} onChange={(e:any) => setQ(e.target.value)} placeholder="Keyword or title" />
                <Select value={field} onValueChange={setField}>
                  <SelectTrigger className="w-48">
                    <SelectValue placeholder="Research field" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">Any</SelectItem>
                    <SelectItem value="Health">Health</SelectItem>
                    <SelectItem value="Education">Education</SelectItem>
                    <SelectItem value="Energy">Energy</SelectItem>
                    <SelectItem value="Technology">Technology</SelectItem>
                  </SelectContent>
                </Select>
                <Button onClick={search} disabled={loading}>{loading ? 'Searching...' : 'Search'}</Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHeadComp>Title</TableHeadComp>
                  <TableHeadComp>Funding</TableHeadComp>
                  <TableHeadComp>Research Field</TableHeadComp>
                </TableRow>
              </TableHeader>
              <TableBody>
                {results.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center py-8 text-muted-foreground">No results</TableCell>
                  </TableRow>
                ) : (
                  results.map((r:any) => (
                    <TableRow key={r.id}>
                      <TableCell className="font-medium">{r.title}</TableCell>
                      <TableCell>{r.program_funding}</TableCell>
                      <TableCell>{r.research_field}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
