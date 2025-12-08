// HomePage.tsx
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
//import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import { Badge } from "./ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./ui/dialog";
import { Label } from "./ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Plus, Trash2, Edit, Eye } from "lucide-react";

// ----------------------
// Mock Data & Interfaces
// ----------------------
interface Application {
  application_id: string;
  user_id: string;
  grant_id: string;
  status: string;
  application_date: string;
}

interface ApplicationUI extends Application {
  grant_name?: string;
}

const MOCK_GRANTS = [
  { id: "550e8400-e29b-41d4-a716-446655440001", name: "Community Development Grant" },
  { id: "550e8400-e29b-41d4-a716-446655440002", name: "Tech Innovation Fund" },
  { id: "550e8400-e29b-41d4-a716-446655440003", name: "Green Energy Initiative" },
  { id: "550e8400-e29b-41d4-a716-446655440004", name: "Small Business Support" },
  { id: "550e8400-e29b-41d4-a716-446655440005", name: "Arts & Culture Fund" },
];

const INITIAL_APPLICATIONS: ApplicationUI[] = [
  {
    application_id: "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    user_id: "u1b2c3d4-e5f6-7890-1234-567890abcdef",
    grant_id: "550e8400-e29b-41d4-a716-446655440001",
    status: "pending",
    application_date: "2025-11-01",
    grant_name: "Community Development Grant",
  },
  {
    application_id: "b2c3d4e5-f678-9012-3456-7890abcdef12",
    user_id: "u1b2c3d4-e5f6-7890-1234-567890abcdef",
    grant_id: "550e8400-e29b-41d4-a716-446655440002",
    status: "in_review",
    application_date: "2025-10-15",
    grant_name: "Tech Innovation Fund",
  },
];



interface ApplicationsPageProps {
  onViewDetails?: (applicationId: string) => void;
  onApply?: () => void;
}

// ----------------------
// HomePage Component
// ----------------------
export function HomePage({ onViewDetails, onApply }) {
  const navigate = useNavigate();
  const [applications, setApplications] = useState<ApplicationUI[]>(INITIAL_APPLICATIONS);
  const [isNewDialogOpen, setIsNewDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingApp, setEditingApp] = useState<ApplicationUI | null>(null);
  const [selectedGrantId, setSelectedGrantId] = useState("");
  const [status, setStatus] = useState<string>("pending");
  const [filterStatus, setFilterStatus] = useState<string>("all");

  const handleLogout = () => {
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("access_token");
    navigate("/");
  };

  const handleCreateApplication = () => {
    const grant = MOCK_GRANTS.find((g) => g.id === selectedGrantId);
    const newApp: ApplicationUI = {
      application_id: crypto.randomUUID(),
      user_id: "u1b2c3d4-e5f6-7890-1234-567890abcdef",
      grant_id: selectedGrantId,
      status,
      application_date: new Date().toISOString().split("T")[0],
      grant_name: grant?.name || "Unknown Grant",
    };
    setApplications([...applications, newApp]);
    setIsNewDialogOpen(false);
    setSelectedGrantId("");
    setStatus("pending");
  };

  const handleDelete = (id: string) => {
    setApplications(applications.filter((app) => app.application_id !== id));
  };

  const openEditDialog = (app: ApplicationUI) => {
    setEditingApp(app);
    setStatus(app.status);
    setIsEditDialogOpen(true);
  };

  const handleUpdateStatus = () => {
    if (editingApp) {
      setApplications(
        applications.map((app) =>
          app.application_id === editingApp.application_id ? { ...app, status } : app
        )
      );
      setEditingApp(null);
      setIsEditDialogOpen(false);
      setStatus("pending");
    }
  };

  const filteredApplications = applications.filter(
    (app) => filterStatus === "all" || app.status === filterStatus
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case "approved":
        return "bg-green-500 hover:bg-green-600";
      case "rejected":
        return "bg-red-500 hover:bg-red-600";
      case "in_review":
        return "bg-blue-500 hover:bg-blue-600";
      default:
        return "bg-slate-500 hover:bg-slate-600";
    }
  };


  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Home</span>
          </div>
          <div className="flex items-center gap-3">
            {/* Go to Home */}
            <Link to="/homepage">
              <Button variant="ghost">Home</Button>
            </Link>
            {/* Search Grants */}
            <Link to="/searchGrants">
              <Button variant="ghost">Search Grants</Button>
            </Link>
            {/* User Settings */}
            <Link to="/user">
              <Button variant="ghost">User Settings</Button>
            </Link>
            {/* Logout Button */}
            <Button variant="outline" onClick={handleLogout}>Logout</Button>
          </div>
        </div>
      </nav>









    <div className="container mx-auto py-10 px-4">
      <Card className="dark:bg-slate-800 dark:border-slate-700">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle className="dark:text-white">My Applications</CardTitle>
            <CardDescription className="dark:text-slate-400">Manage your grant applications and track their status.</CardDescription>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={() => navigate("/searchGrants")}>
              Find Grant to Apply
            </Button>
            <Dialog open={isNewDialogOpen} onOpenChange={setIsNewDialogOpen}>
            <DialogTrigger asChild>
              <Button>
                <Plus className="mr-2 h-4 w-4" /> New Application
              </Button>
            </DialogTrigger>
            <DialogContent className="dark:bg-slate-800 dark:border-slate-700">
              <DialogHeader>
                <DialogTitle className="dark:text-white">Create New Application</DialogTitle>
                <DialogDescription className="dark:text-slate-400">
                  Record a new grant application manually.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="grant" className="text-right dark:text-slate-300">
                    Grant
                  </Label>
                  <Select value={selectedGrantId} onValueChange={setSelectedGrantId}>
                    <SelectTrigger className="col-span-3 dark:bg-slate-900 dark:border-slate-700 dark:text-white">
                      <SelectValue placeholder="Select a grant" />
                    </SelectTrigger>
                    <SelectContent className="dark:bg-slate-800 dark:border-slate-700">
                      {MOCK_GRANTS.map((grant) => (
                        <SelectItem key={grant.id} value={grant.id} className="dark:text-white dark:focus:bg-slate-700">
                          {grant.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="status" className="text-right dark:text-slate-300">
                    Status
                  </Label>
                  <Select value={status} onValueChange={setStatus}>
                    <SelectTrigger className="col-span-3 dark:bg-slate-900 dark:border-slate-700 dark:text-white">
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent className="dark:bg-slate-800 dark:border-slate-700">
                      <SelectItem value="pending" className="dark:text-white dark:focus:bg-slate-700">Pending</SelectItem>
                      <SelectItem value="in_review" className="dark:text-white dark:focus:bg-slate-700">In Review</SelectItem>
                      <SelectItem value="approved" className="dark:text-white dark:focus:bg-slate-700">Approved</SelectItem>
                      <SelectItem value="rejected" className="dark:text-white dark:focus:bg-slate-700">Rejected</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button onClick={handleCreateApplication} disabled={!selectedGrantId}>Save Application</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
          </div>

          <Dialog open={isEditDialogOpen} onOpenChange={setIsEditDialogOpen}>
            <DialogContent className="dark:bg-slate-800 dark:border-slate-700">
              <DialogHeader>
                <DialogTitle className="dark:text-white">Update Application Status</DialogTitle>
                <DialogDescription className="dark:text-slate-400">
                  Update the status of your application for {editingApp?.grant_name}.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="edit-status" className="text-right dark:text-slate-300">
                    Status
                  </Label>
                  <Select value={status} onValueChange={setStatus}>
                    <SelectTrigger className="col-span-3 dark:bg-slate-900 dark:border-slate-700 dark:text-white">
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent className="dark:bg-slate-800 dark:border-slate-700">
                      <SelectItem value="pending" className="dark:text-white dark:focus:bg-slate-700">Pending</SelectItem>
                      <SelectItem value="in_review" className="dark:text-white dark:focus:bg-slate-700">In Review</SelectItem>
                      <SelectItem value="approved" className="dark:text-white dark:focus:bg-slate-700">Approved</SelectItem>
                      <SelectItem value="rejected" className="dark:text-white dark:focus:bg-slate-700">Rejected</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button onClick={handleUpdateStatus}>Update Status</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        </CardHeader>



        <CardContent>
          <div className="flex justify-end mb-4">
            <Select value={filterStatus} onValueChange={setFilterStatus}>
              <SelectTrigger className="w-[180px] dark:bg-slate-900 dark:border-slate-700 dark:text-white">
                <SelectValue placeholder="Filter by status" />
              </SelectTrigger>
              <SelectContent className="dark:bg-slate-800 dark:border-slate-700">
                <SelectItem value="all" className="dark:text-white dark:focus:bg-slate-700">All Statuses</SelectItem>
                <SelectItem value="pending" className="dark:text-white dark:focus:bg-slate-700">Pending</SelectItem>
                <SelectItem value="in_review" className="dark:text-white dark:focus:bg-slate-700">In Review</SelectItem>
                <SelectItem value="approved" className="dark:text-white dark:focus:bg-slate-700">Approved</SelectItem>
                <SelectItem value="rejected" className="dark:text-white dark:focus:bg-slate-700">Rejected</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Table>
            <TableHeader>
              <TableRow className="dark:border-slate-700">
                <TableHead className="dark:text-slate-400">Grant Name</TableHead>
                <TableHead className="dark:text-slate-400">Date Applied</TableHead>
                <TableHead className="dark:text-slate-400">Status</TableHead>
                <TableHead className="text-right dark:text-slate-400">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredApplications.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={4} className="text-center py-8 text-muted-foreground dark:text-slate-500">
                    No applications found.
                  </TableCell>
                </TableRow>
              ) : (
                filteredApplications.map((app) => (
                  <TableRow key={app.application_id} className="dark:border-slate-700">
                    <TableCell className="font-medium dark:text-white">{app.grant_name}</TableCell>
                    <TableCell className="dark:text-slate-300">{app.application_date}</TableCell>
                    <TableCell>
                      <Badge className={`${getStatusColor(app.status)} text-slate-900 dark:text-white`}>
                        {app.status.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="icon" onClick={() => onViewDetails?.(app.application_id)}>
                        <Eye className="h-4 w-4 text-slate-500" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => openEditDialog(app)}>
                        <Edit className="h-4 w-4 text-blue-500" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => handleDelete(app.application_id)}>
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
    </div>




      {/* Footer (same styling as LandingPage) */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
