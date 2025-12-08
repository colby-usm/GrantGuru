// HomePage.tsx
import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { ThemeToggle } from "./ThemeToggle";
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
// Interfaces
// ----------------------
interface Application {
  application_id: string;
  user_id: string;
  grant_id: string;
  submission_status: string;
  status: string;
  application_date: string;
}

interface ApplicationUI extends Application {
  grant_name?: string;
}

// ----------------------
// HomePage Component
// ----------------------
export function HomePage() {
  const navigate = useNavigate();
  const [applications, setApplications] = useState<ApplicationUI[]>([]);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editingApp, setEditingApp] = useState<ApplicationUI | null>(null);
  const [status, setStatus] = useState<string>("pending");
  const [filterStatus, setFilterStatus] = useState<string>("all");

  // Fetch user's applications on mount
  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const token = sessionStorage.getItem("access_token");
        if (!token) {
          navigate("/");
          return;
        }

        const response = await fetch("http://127.0.0.1:5000/api/user/applications", {
          method: "GET",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          setApplications(data.applications);
        } else if (response.status === 401) {
          // Token expired or invalid
          sessionStorage.removeItem("user_id");
          sessionStorage.removeItem("access_token");
          navigate("/");
        } else {
          console.error("Failed to fetch applications");
        }
      } catch (error) {
        console.error("Error fetching applications:", error);
      }
    };

    fetchApplications();
  }, [navigate]);

  const handleLogout = () => {
    sessionStorage.removeItem("user_id");
    sessionStorage.removeItem("access_token");
    navigate("/");
  };

  const handleViewDetails = (applicationId: string) => {
    navigate(`/application/${applicationId}`);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm("Are you sure you want to delete this application?")) {
      return;
    }

    try {
      const token = sessionStorage.getItem("access_token");
      const response = await fetch(`http://127.0.0.1:5000/api/user/applications/${id}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        setApplications(applications.filter((app) => app.application_id !== id));
      } else {
        const data = await response.json();
        alert(data.error || "Failed to delete application");
      }
    } catch (error) {
      console.error("Error deleting application:", error);
      alert("Failed to delete application");
    }
  };

  const openEditDialog = (app: ApplicationUI) => {
    setEditingApp(app);
    setStatus(app.status);
    setIsEditDialogOpen(true);
  };

  const handleUpdateStatus = async () => {
    if (!editingApp) return;

    try {
      const token = sessionStorage.getItem("access_token");
      const response = await fetch(`http://127.0.0.1:5000/api/user/applications/${editingApp.application_id}`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status }),
      });

      if (response.ok) {
        setApplications(
          applications.map((app) =>
            app.application_id === editingApp.application_id ? { ...app, status } : app
          )
        );
        setEditingApp(null);
        setIsEditDialogOpen(false);
        setStatus("pending");
      } else {
        const data = await response.json();
        alert(data.error || "Failed to update status");
      }
    } catch (error) {
      console.error("Error updating status:", error);
      alert("Failed to update status");
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
            <ThemeToggle />
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
            <Button onClick={() => navigate("/searchGrants")}>
              <Plus className="mr-2 h-4 w-4" /> Find Grant to Apply
            </Button>
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
                <TableHead className="dark:text-slate-400">Type</TableHead>
                <TableHead className="dark:text-slate-400">Status</TableHead>
                <TableHead className="text-right dark:text-slate-400">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredApplications.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-muted-foreground dark:text-slate-500">
                    No applications found.
                  </TableCell>
                </TableRow>
              ) : (
                filteredApplications.map((app) => (
                  <TableRow key={app.application_id} className="dark:border-slate-700">
                    <TableCell className="font-medium dark:text-white max-w-xs break-words whitespace-normal">{app.grant_name}</TableCell>
                    <TableCell className="dark:text-slate-300 whitespace-nowrap">{app.application_date}</TableCell>
                    <TableCell className="whitespace-nowrap">
                      <Badge variant={app.submission_status === "started" ? "outline" : "default"} className="dark:text-white">
                        {app.submission_status === "started" ? "STARTED" : "SUBMITTED"}
                      </Badge>
                    </TableCell>
                    <TableCell className="whitespace-nowrap">
                      <Badge className={`${getStatusColor(app.status)} text-slate-900 dark:text-white`}>
                        {app.status.replace('_', ' ').toUpperCase()}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right whitespace-nowrap">
                      <Button variant="ghost" size="icon" onClick={() => handleViewDetails(app.application_id)} title={app.submission_status === "started" ? "Edit application" : "View application"}>
                        <Eye className="h-4 w-4 text-slate-500" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => openEditDialog(app)} title="Quick edit status">
                        <Edit className="h-4 w-4 text-blue-500" />
                      </Button>
                      <Button variant="ghost" size="icon" onClick={() => handleDelete(app.application_id)} title="Delete application">
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
