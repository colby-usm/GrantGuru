import { useState } from "react";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Calendar, Clock, FileText, Link as LinkIcon, Plus, Trash2, Upload } from "lucide-react";

// --- Interfaces based on Schema ---

interface Grant {
  grant_id: string;
  grant_title: string;
  opportunity_number: string;
  description: string;
  provider: string;
  award_max_amount?: number;
  award_min_amount?: number;
  date_posted?: string;
  date_closed?: string; // Grant Deadline
  link_to_source: string;
}

interface Application {
  application_id: string;
  status: string;
  application_date: string;
  grant: Grant; // Nested for this view
}

interface InternalDeadline {
  internal_deadline_id: string;
  deadline_name: string;
  deadline_date: string; // DATETIME
  application_id: string;
}

interface Document {
  document_id: string;
  document_name: string;
  document_type: string;
  document_size: number; // bytes
  upload_date: string; // DATETIME
  application_id: string;
}

// --- Mock Data ---

const MOCK_GRANT: Grant = {
  grant_id: "550e8400-e29b-41d4-a716-446655440001",
  grant_title: "Community Development Block Grant",
  opportunity_number: "CDBG-2025-001",
  description: "The Community Development Block Grant (CDBG) program provides annual grants on a formula basis to states and local governments to develop viable urban communities by providing decent housing and a suitable living environment, and by expanding economic opportunities, principally for low- and moderate-income persons.",
  provider: "Department of Housing and Urban Development",
  award_max_amount: 500000,
  award_min_amount: 50000,
  date_posted: "2025-09-01",
  date_closed: "2025-12-31",
  link_to_source: "https://www.grants.gov/web/grants/view-opportunity.html?oppId=12345",
};

const MOCK_APPLICATION: Application = {
  application_id: "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  status: "in_review",
  application_date: "2025-10-15",
  grant: MOCK_GRANT,
};

const INITIAL_DEADLINES: InternalDeadline[] = [
  {
    internal_deadline_id: "d1",
    deadline_name: "First Draft Submission",
    deadline_date: "2025-11-15T17:00:00",
    application_id: MOCK_APPLICATION.application_id,
  },
  {
    internal_deadline_id: "d2",
    deadline_name: "Internal Review Meeting",
    deadline_date: "2025-11-20T14:00:00",
    application_id: MOCK_APPLICATION.application_id,
  },
];

const INITIAL_DOCUMENTS: Document[] = [
  {
    document_id: "doc1",
    document_name: "Project_Proposal_v1.pdf",
    document_type: "pdf",
    document_size: 1024 * 1024 * 2.5, // 2.5 MB
    upload_date: "2025-11-10T09:30:00",
    application_id: MOCK_APPLICATION.application_id,
  },
  {
    document_id: "doc2",
    document_name: "Budget_Sheet.xlsx",
    document_type: "xlsx",
    document_size: 1024 * 500, // 500 KB
    upload_date: "2025-11-12T11:15:00",
    application_id: MOCK_APPLICATION.application_id,
  },
];

// --- Helper Functions ---

const formatCurrency = (amount?: number) => {
  if (amount === undefined) return "N/A";
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};

const formatDate = (dateString?: string) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString();
};

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString();
};

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

export function ApplicationDetailsPage() {
  const [application] = useState<Application>(MOCK_APPLICATION);
  const [deadlines, setDeadlines] = useState<InternalDeadline[]>(INITIAL_DEADLINES);
  const [documents, setDocuments] = useState<Document[]>(INITIAL_DOCUMENTS);

  // Deadline Form State
  const [isDeadlineDialogOpen, setIsDeadlineDialogOpen] = useState(false);
  const [newDeadlineName, setNewDeadlineName] = useState("");
  const [newDeadlineDate, setNewDeadlineDate] = useState("");

  // Document Form State
  const [isDocumentDialogOpen, setIsDocumentDialogOpen] = useState(false);
  const [newDocumentName, setNewDocumentName] = useState("");

  const handleAddDeadline = () => {
    if (!newDeadlineName || !newDeadlineDate) return;
    const newDeadline: InternalDeadline = {
      internal_deadline_id: crypto.randomUUID(),
      deadline_name: newDeadlineName,
      deadline_date: newDeadlineDate,
      application_id: application.application_id,
    };
    setDeadlines([...deadlines, newDeadline]);
    setIsDeadlineDialogOpen(false);
    setNewDeadlineName("");
    setNewDeadlineDate("");
  };

  const handleDeleteDeadline = (id: string) => {
    setDeadlines(deadlines.filter(d => d.internal_deadline_id !== id));
  };

  const handleAddDocument = () => {
    // Simulating file upload
    if (!newDocumentName) return;
    const newDoc: Document = {
      document_id: crypto.randomUUID(),
      document_name: newDocumentName,
      document_type: newDocumentName.split('.').pop() || "unknown",
      document_size: Math.floor(Math.random() * 10000000),
      upload_date: new Date().toISOString(),
      application_id: application.application_id,
    };
    setDocuments([...documents, newDoc]);
    setIsDocumentDialogOpen(false);
    setNewDocumentName("");
  };

  const handleDeleteDocument = (id: string) => {
    setDocuments(documents.filter(d => d.document_id !== id));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved": return "bg-green-500 hover:bg-green-600";
      case "rejected": return "bg-red-500 hover:bg-red-600";
      case "in_review": return "bg-blue-500 hover:bg-blue-600";
      default: return "bg-slate-500 hover:bg-slate-600";
    }
  };

  return (
    <div className="container mx-auto py-10 px-4 space-y-6">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold dark:text-white">{application.grant.grant_title}</h1>
            <Badge className={`${getStatusColor(application.status)} text-white`}>
              {application.status.replace('_', ' ').toUpperCase()}
            </Badge>
          </div>
          <p className="text-muted-foreground dark:text-slate-400 flex items-center gap-2">
            Provided by {application.grant.provider}
            <span className="text-slate-300">•</span>
            Opportunity #{application.grant.opportunity_number}
          </p>
        </div>
        <Button variant="outline" asChild>
          <a href={application.grant.link_to_source} target="_blank" rel="noreferrer">
            <LinkIcon className="mr-2 h-4 w-4" /> View Source
          </a>
        </Button>
      </div>

      <Separator className="dark:bg-slate-700" />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Grant Details */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="dark:bg-slate-800 dark:border-slate-700">
            <CardHeader>
              <CardTitle className="dark:text-white">Grant Overview</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <h3 className="font-semibold mb-2 dark:text-slate-200">Description</h3>
                <p className="text-sm text-muted-foreground dark:text-slate-400 leading-relaxed">
                  {application.grant.description}
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4">
                <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                  <h4 className="text-sm font-medium text-muted-foreground mb-1">Award Amount</h4>
                  <p className="text-lg font-semibold dark:text-white">
                    {formatCurrency(application.grant.award_min_amount)} - {formatCurrency(application.grant.award_max_amount)}
                  </p>
                </div>
                <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-900">
                  <h4 className="text-sm font-medium text-muted-foreground mb-1">Key Dates</h4>
                  <div className="flex justify-between text-sm">
                    <span className="dark:text-slate-400">Posted:</span>
                    <span className="font-medium dark:text-white">{formatDate(application.grant.date_posted)}</span>
                  </div>
                  <div className="flex justify-between text-sm mt-1">
                    <span className="dark:text-slate-400">Closing:</span>
                    <span className="font-medium text-red-500">{formatDate(application.grant.date_closed)}</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="deadlines" className="w-full">
            <TabsList className="grid w-full grid-cols-2 dark:bg-slate-900">
              <TabsTrigger value="deadlines">Internal Deadlines</TabsTrigger>
              <TabsTrigger value="documents">Documents</TabsTrigger>
            </TabsList>
            
            {/* Internal Deadlines Tab */}
            <TabsContent value="deadlines">
              <Card className="dark:bg-slate-800 dark:border-slate-700">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="dark:text-white">Internal Deadlines</CardTitle>
                    <CardDescription className="dark:text-slate-400">Track your team's milestones for this application.</CardDescription>
                  </div>
                  <Dialog open={isDeadlineDialogOpen} onOpenChange={setIsDeadlineDialogOpen}>
                    <DialogTrigger asChild>
                      <Button size="sm">
                        <Plus className="mr-2 h-4 w-4" /> Add Deadline
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="dark:bg-slate-800 dark:border-slate-700">
                      <DialogHeader>
                        <DialogTitle className="dark:text-white">Add Internal Deadline</DialogTitle>
                      </DialogHeader>
                      <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                          <Label htmlFor="deadline-name" className="dark:text-slate-300">Name</Label>
                          <Input 
                            id="deadline-name" 
                            value={newDeadlineName} 
                            onChange={(e) => setNewDeadlineName(e.target.value)}
                            placeholder="e.g., Draft Review"
                            className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                          />
                        </div>
                        <div className="grid gap-2">
                          <Label htmlFor="deadline-date" className="dark:text-slate-300">Date & Time</Label>
                          <Input 
                            id="deadline-date" 
                            type="datetime-local"
                            value={newDeadlineDate} 
                            onChange={(e) => setNewDeadlineDate(e.target.value)}
                            className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                          />
                        </div>
                      </div>
                      <DialogFooter>
                        <Button onClick={handleAddDeadline}>Save Deadline</Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow className="dark:border-slate-700">
                        <TableHead className="dark:text-slate-400">Milestone</TableHead>
                        <TableHead className="dark:text-slate-400">Due Date</TableHead>
                        <TableHead className="text-right dark:text-slate-400">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {deadlines.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={3} className="text-center py-6 text-muted-foreground">No deadlines set.</TableCell>
                        </TableRow>
                      ) : (
                        deadlines.map((deadline) => (
                          <TableRow key={deadline.internal_deadline_id} className="dark:border-slate-700">
                            <TableCell className="font-medium dark:text-white flex items-center gap-2">
                              <Clock className="h-4 w-4 text-blue-500" />
                              {deadline.deadline_name}
                            </TableCell>
                            <TableCell className="dark:text-slate-300">{formatDateTime(deadline.deadline_date)}</TableCell>
                            <TableCell className="text-right">
                              <Button variant="ghost" size="icon" onClick={() => handleDeleteDeadline(deadline.internal_deadline_id)}>
                                <Trash2 className="h-4 w-4 text-red-500" />
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Documents Tab */}
            <TabsContent value="documents">
              <Card className="dark:bg-slate-800 dark:border-slate-700">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle className="dark:text-white">Documents</CardTitle>
                    <CardDescription className="dark:text-slate-400">Manage files associated with this application.</CardDescription>
                  </div>
                  <Dialog open={isDocumentDialogOpen} onOpenChange={setIsDocumentDialogOpen}>
                    <DialogTrigger asChild>
                      <Button size="sm">
                        <Upload className="mr-2 h-4 w-4" /> Upload Document
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="dark:bg-slate-800 dark:border-slate-700">
                      <DialogHeader>
                        <DialogTitle className="dark:text-white">Upload Document</DialogTitle>
                      </DialogHeader>
                      <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                          <Label htmlFor="doc-name" className="dark:text-slate-300">File Name (Simulated)</Label>
                          <Input 
                            id="doc-name" 
                            value={newDocumentName} 
                            onChange={(e) => setNewDocumentName(e.target.value)}
                            placeholder="e.g., Proposal.pdf"
                            className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                          />
                        </div>
                      </div>
                      <DialogFooter>
                        <Button onClick={handleAddDocument}>Upload</Button>
                      </DialogFooter>
                    </DialogContent>
                  </Dialog>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow className="dark:border-slate-700">
                        <TableHead className="dark:text-slate-400">Name</TableHead>
                        <TableHead className="dark:text-slate-400">Size</TableHead>
                        <TableHead className="dark:text-slate-400">Uploaded</TableHead>
                        <TableHead className="text-right dark:text-slate-400">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {documents.length === 0 ? (
                        <TableRow>
                          <TableCell colSpan={4} className="text-center py-6 text-muted-foreground">No documents uploaded.</TableCell>
                        </TableRow>
                      ) : (
                        documents.map((doc) => (
                          <TableRow key={doc.document_id} className="dark:border-slate-700">
                            <TableCell className="font-medium dark:text-white flex items-center gap-2">
                              <FileText className="h-4 w-4 text-slate-500" />
                              {doc.document_name}
                            </TableCell>
                            <TableCell className="dark:text-slate-300">{formatFileSize(doc.document_size)}</TableCell>
                            <TableCell className="dark:text-slate-300">{formatDateTime(doc.upload_date)}</TableCell>
                            <TableCell className="text-right">
                              <Button variant="ghost" size="icon" onClick={() => handleDeleteDocument(doc.document_id)}>
                                <Trash2 className="h-4 w-4 text-red-500" />
                              </Button>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* Right Column: Status & Quick Actions */}
        <div className="space-y-6">
          <Card className="dark:bg-slate-800 dark:border-slate-700">
            <CardHeader>
              <CardTitle className="text-lg dark:text-white">Application Status</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-900 rounded-md">
                  <span className="text-sm font-medium dark:text-slate-300">Current Status</span>
                  <Badge className={getStatusColor(application.status)}>
                    {application.status.replace('_', ' ').toUpperCase()}
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 bg-slate-50 dark:bg-slate-900 rounded-md">
                  <span className="text-sm font-medium dark:text-slate-300">Applied On</span>
                  <span className="text-sm dark:text-white">{formatDate(application.application_date)}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="dark:bg-slate-800 dark:border-slate-700">
            <CardHeader>
              <CardTitle className="text-lg dark:text-white">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              <Button className="w-full" variant="secondary">
                <Calendar className="mr-2 h-4 w-4" /> Sync to Calendar
              </Button>
              <Button className="w-full" variant="outline">
                Export Application Data
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
