import React, { useEffect, useState } from "react";
import DOMPurify from "dompurify";
import { useParams, Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Calendar, ArrowLeft, Save, Building2, X, Upload } from "lucide-react";

interface DocumentUpload {
  id: string;
  files: File[];
  type: string;
}

interface SavedDocument {
  document_id: string;
  document_name: string;
  document_type: string;
  document_size: number;
  upload_date: string;
}

const API_BASE_URL = "http://127.0.0.1:5000";

const formatCurrency = (amount?: number) => {
  if (amount === undefined || amount === null) return "N/A";
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};

const formatDate = (dateString?: string) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString();
};

const parsePointOfContact = (contactData?: string) => {
  if (!contactData) return null;
  try {
    return typeof contactData === 'string' ? JSON.parse(contactData) : contactData;
  } catch (e) {
    return null;
  }
};

export function ApplicationEditPage() {
  const { applicationId } = useParams();
  const navigate = useNavigate();
  const [application, setApplication] = useState<any | null>(null);
  const [grant, setGrant] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  // Form state
  const [status, setStatus] = useState("pending");

  // Document Uploads State
  const [documents, setDocuments] = useState<DocumentUpload[]>([
    { id: "1", type: "Proposal", files: [] },
    { id: "2", type: "Budget", files: [] },
    { id: "3", type: "CV/Resume", files: [] },
    { id: "4", type: "Cover Letter", files: [] },
  ]);

  // Saved documents from database
  const [savedDocuments, setSavedDocuments] = useState<SavedDocument[]>([]);

  // Task management state
  const [tasks, setTasks] = useState<any[]>([]);
  const [newTaskName, setNewTaskName] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [newTaskDeadline, setNewTaskDeadline] = useState("");
  const [isAddingTask, setIsAddingTask] = useState(false);

  const handleLogout = () => {
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('access_token');
    navigate('/');
  };

  const handleFileChange = (id: string, newFiles: FileList | null) => {
    if (!newFiles) return;
    const filesArray = Array.from(newFiles);

    setDocuments(docs => docs.map(doc => {
        if (doc.id === id) {
            return { ...doc, files: [...doc.files, ...filesArray] };
        }
        return doc;
    }));
  };

  const removeFile = (docId: string, fileIndex: number) => {
    setDocuments(docs => docs.map(doc => {
        if (doc.id === docId) {
            const newFiles = [...doc.files];
            newFiles.splice(fileIndex, 1);
            return { ...doc, files: newFiles };
        }
        return doc;
    }));
  };

  const handleDeleteDocument = async (documentId: string) => {
    if (!confirm("Are you sure you want to delete this document?")) {
      return;
    }

    try {
      const token = sessionStorage.getItem("access_token");
      if (!token) {
        alert("Please log in");
        navigate("/");
        return;
      }

      const response = await fetch(
        `${API_BASE_URL}/api/user/applications/${applicationId}/documents/${documentId}`,
        {
          method: "DELETE",
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        // Remove the deleted document from the saved documents list
        setSavedDocuments(prev => prev.filter(doc => doc.document_id !== documentId));
      } else {
        const data = await response.json();
        alert(data.error || "Failed to delete document");
      }
    } catch (error) {
      console.error("Error deleting document:", error);
      alert("Failed to delete document");
    }
  };

  useEffect(() => {
    if (!applicationId) return;

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const token = sessionStorage.getItem("access_token");
        if (!token) {
          navigate("/");
          return;
        }

        // Fetch application details
        const appResponse = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        if (!appResponse.ok) {
          throw new Error("Failed to load application");
        }

        const appData = await appResponse.json();
        setApplication(appData.application);
        setStatus(appData.application.status);

        // Fetch grant details
        const grantResponse = await fetch(`${API_BASE_URL}/api/public/grant/${appData.application.grant_id}`);
        const grantData = await grantResponse.json();
        setGrant(grantData.grant || null);

        // Fetch tasks if this is a started application
        if (appData.application.submission_status === "started") {
          const tasksResponse = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/tasks`, {
            headers: {
              "Authorization": `Bearer ${token}`,
            },
          });

          if (tasksResponse.ok) {
            const tasksData = await tasksResponse.json();
            setTasks(tasksData.tasks || []);
          }
        }

        // Fetch saved documents
        const documentsResponse = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/documents`, {
          headers: {
            "Authorization": `Bearer ${token}`,
          },
        });

        if (documentsResponse.ok) {
          const documentsData = await documentsResponse.json();
          setSavedDocuments(documentsData.documents || []);
        }

      } catch (err) {
        console.error(err);
        setError(err instanceof Error ? err.message : "Failed to load data");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [applicationId, navigate]);

  const handleSave = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();

    setIsSaving(true);

    try {
      const token = sessionStorage.getItem("access_token");

      // Step 1: Update application details
      const response = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          status,
          submission_status: "started",
        }),
      });

      if (response.ok) {
        // Step 2: Upload any new documents
        const hasNewFiles = documents.some(doc => doc.files.length > 0);

        if (hasNewFiles) {
          for (const doc of documents) {
            if (doc.files.length > 0) {
              const formData = new FormData();
              doc.files.forEach(file => {
                formData.append('files', file);
              });
              formData.append('document_type', doc.type);

              const uploadResponse = await fetch(
                `${API_BASE_URL}/api/user/applications/${applicationId}/documents`,
                {
                  method: "POST",
                  headers: {
                    "Authorization": `Bearer ${token}`,
                  },
                  body: formData,
                }
              );

              if (!uploadResponse.ok) {
                console.error(`Failed to upload ${doc.type} documents`);
              }
            }
          }
        }

        alert("Application and documents saved successfully!");
        navigate("/homepage");
      } else {
        const data = await response.json();
        alert(data.error || "Failed to save application");
      }
    } catch (error) {
      console.error("Error saving application:", error);
      alert("Failed to save application");
    } finally {
      setIsSaving(false);
    }
  };

  const handleAddTask = async () => {
    if (!newTaskName || !newTaskDeadline) {
      alert("Please provide task name and deadline");
      return;
    }

    setIsAddingTask(true);

    try {
      const token = sessionStorage.getItem("access_token");
      const response = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/tasks`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task_name: newTaskName,
          task_description: newTaskDescription,
          deadline: newTaskDeadline,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setTasks([...tasks, data.task]);
        setNewTaskName("");
        setNewTaskDescription("");
        setNewTaskDeadline("");
      } else {
        const data = await response.json();
        alert(data.error || "Failed to add task");
      }
    } catch (error) {
      console.error("Error adding task:", error);
      alert("Failed to add task");
    } finally {
      setIsAddingTask(false);
    }
  };

  const handleToggleTask = async (taskId: string, completed: boolean) => {
    try {
      const token = sessionStorage.getItem("access_token");
      const response = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ completed }),
      });

      if (response.ok) {
        setTasks(tasks.map(task =>
          task.task_id === taskId ? { ...task, completed } : task
        ));
      } else {
        const data = await response.json();
        alert(data.error || "Failed to update task");
      }
    } catch (error) {
      console.error("Error updating task:", error);
      alert("Failed to update task");
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm("Are you sure you want to delete this task?")) {
      return;
    }

    try {
      const token = sessionStorage.getItem("access_token");
      const response = await fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/tasks/${taskId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.task_id !== taskId));
      } else {
        const data = await response.json();
        alert(data.error || "Failed to delete task");
      }
    } catch (error) {
      console.error("Error deleting task:", error);
      alert("Failed to delete task");
    }
  };

  if (loading) return <div className="p-6 dark:text-white">Loading...</div>;
  if (error) return <div className="p-6 text-red-500">{error}</div>;
  if (!application || !grant) return <div className="p-6 dark:text-white">Application not found.</div>;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation Header */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Edit Application</span>
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

      {/* Page Content */}
      <div className="container mx-auto py-10 px-4 space-y-8 max-w-5xl">
        {/* Back Button */}
        <Link to="/homepage" className="inline-flex items-center gap-2 text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200">
          <ArrowLeft className="h-4 w-4" />
          Back to My Applications
        </Link>

        {/* Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground dark:text-slate-400">
            <span>Application Details</span>
            <span>/</span>
            <span>{grant.research_field || "General"}</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold dark:text-white">{grant.grant_title}</h1>
          <div className="flex flex-wrap gap-4 items-center pt-2">
            <Badge variant="secondary" className="text-sm">
              {grant.provider}
            </Badge>
            <span className="text-sm text-muted-foreground dark:text-slate-400 flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              Deadline: <span className="text-red-500 font-medium">{formatDate(grant.date_closed)}</span>
            </span>
            <Badge className={getStatusColor(status)}>
              {status.replace('_', ' ').toUpperCase()}
            </Badge>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column: Grant Details */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="dark:bg-slate-800 dark:border-slate-700">
              <CardHeader>
                <CardTitle>Grant Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h3 className="font-semibold mb-2 dark:text-white">Description</h3>
                  <div
                    className="text-muted-foreground dark:text-slate-300 leading-relaxed prose dark:prose-invert max-w-none"
                    dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(grant.description || "") }}
                  />
                </div>

                <Separator className="dark:bg-slate-700" />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold mb-2 dark:text-white">Funding Information</h3>
                    <ul className="space-y-2 text-sm">
                      <li className="flex justify-between">
                        <span className="text-muted-foreground dark:text-slate-400">Total Program Funding:</span>
                        <span className="font-medium dark:text-white">{formatCurrency(grant.program_funding)}</span>
                      </li>
                      <li className="flex justify-between">
                        <span className="text-muted-foreground dark:text-slate-400">Award Ceiling:</span>
                        <span className="font-medium dark:text-white">{formatCurrency(grant.award_max_amount)}</span>
                      </li>
                      <li className="flex justify-between">
                        <span className="text-muted-foreground dark:text-slate-400">Award Floor:</span>
                        <span className="font-medium dark:text-white">{formatCurrency(grant.award_min_amount)}</span>
                      </li>
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold mb-2 dark:text-white">Eligibility</h3>
                    <p className="text-sm text-muted-foreground dark:text-slate-300">{grant.eligibility || "N/A"}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Point of Contact Card */}
            {(() => {
              const contact = parsePointOfContact(grant.point_of_contact);
              if (!contact) return null;

              return (
                <Card className="dark:bg-slate-800 dark:border-slate-700">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Building2 className="h-5 w-5 text-blue-600" />
                      Point of Contact
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {contact.name && (
                      <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border dark:border-slate-700">
                        <p className="text-xs font-medium text-muted-foreground dark:text-slate-400 mb-1">Organization</p>
                        <p className="font-semibold text-slate-900 dark:text-white">{contact.name}</p>
                      </div>
                    )}
                    {contact.email && (
                      <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border dark:border-slate-700">
                        <p className="text-xs font-medium text-muted-foreground dark:text-slate-400 mb-1">Email</p>
                        <a href={`mailto:${contact.email}`} className="text-blue-600 dark:text-blue-400 hover:underline">
                          {contact.email}
                        </a>
                      </div>
                    )}
                  </CardContent>
                </Card>
              );
            })()}
          </div>

          {/* Right Column: Application Edit Form */}
          <div className="lg:col-span-1 space-y-6">
            <>
              <Card id="application-form" className="sticky top-6 dark:bg-slate-800 dark:border-slate-700 border-t-4 border-t-blue-600 shadow-lg">
                <CardHeader>
                  <CardTitle className="dark:text-white">Application Form</CardTitle>
                  <CardDescription className="dark:text-slate-400">
                    Save your application progress.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <form onSubmit={handleSave} className="space-y-4">
                      <div className="space-y-3">
                        <Label className="dark:text-slate-300">Required Documents</Label>
                        {documents.map((doc) => {
                          // Filter saved documents by type
                          const savedDocsOfType = savedDocuments.filter(
                            (savedDoc) => savedDoc.document_type === doc.type
                          );

                          return (
                            <div key={doc.id} className="space-y-2">
                              <span className="text-xs font-medium text-muted-foreground dark:text-slate-400">{doc.type}</span>

                              {/* Show saved documents */}
                              {savedDocsOfType.length > 0 && (
                                <div className="space-y-1">
                                  <p className="text-xs text-muted-foreground dark:text-slate-500">Previously uploaded:</p>
                                  {savedDocsOfType.map((savedDoc) => (
                                    <div key={savedDoc.document_id} className="flex items-center justify-between text-xs bg-blue-50 dark:bg-blue-950/30 p-2 rounded border border-blue-200 dark:border-blue-900">
                                      <div className="flex-1 truncate">
                                        <a
                                          href="#"
                                          className="font-medium dark:text-blue-300 hover:underline cursor-pointer"
                                          onClick={(e) => {
                                            e.preventDefault();
                                            const token = sessionStorage.getItem("access_token");
                                            fetch(`${API_BASE_URL}/api/user/applications/${applicationId}/documents/${savedDoc.document_id}/download`, {
                                              headers: {
                                                "Authorization": `Bearer ${token}`,
                                              },
                                            })
                                              .then(response => response.blob())
                                              .then(blob => {
                                                const url = window.URL.createObjectURL(blob);
                                                const a = document.createElement('a');
                                                a.href = url;
                                                a.download = savedDoc.document_name;
                                                document.body.appendChild(a);
                                                a.click();
                                                window.URL.revokeObjectURL(url);
                                                document.body.removeChild(a);
                                              })
                                              .catch(err => {
                                                console.error("Download failed:", err);
                                                alert("Failed to download document");
                                              });
                                          }}
                                        >
                                          {savedDoc.document_name}
                                        </a>
                                        <span className="text-muted-foreground dark:text-slate-500 ml-2">
                                          ({(savedDoc.document_size / 1024).toFixed(1)} KB)
                                        </span>
                                      </div>
                                      <div className="flex items-center gap-2">
                                        <span className="text-xs text-muted-foreground dark:text-slate-500">
                                          {new Date(savedDoc.upload_date).toLocaleDateString()}
                                        </span>
                                        <button
                                          type="button"
                                          onClick={() => handleDeleteDocument(savedDoc.document_id)}
                                          className="text-slate-500 hover:text-red-500"
                                          title="Delete document"
                                        >
                                          <X className="h-3 w-3" />
                                        </button>
                                      </div>
                                    </div>
                                  ))}
                                </div>
                              )}

                              {/* Upload new files */}
                              <div className="space-y-2">
                                <div className="items-center gap-2">
                                  <input
                                    type="file"
                                    multiple
                                    className="hidden"
                                    id={`file-upload-${doc.id}`}
                                    onChange={(e) => {
                                      handleFileChange(doc.id, e.target.files);
                                      e.target.value = '';
                                    }}
                                  />
                                  <Button asChild variant="outline" size="sm" className="w-full cursor-pointer dark:border-slate-700 dark:text-white">
                                    <label htmlFor={`file-upload-${doc.id}`}>
                                      <Upload className="mr-2 h-3 w-3" /> {savedDocsOfType.length > 0 ? 'Upload Additional Files' : 'Browse Files'}
                                    </label>
                                  </Button>
                                </div>
                                {doc.files.length > 0 && (
                                  <div className="space-y-1">
                                    <p className="text-xs text-muted-foreground dark:text-slate-500">New files to upload:</p>
                                    {doc.files.map((file, index) => (
                                      <div key={index} className="flex items-center justify-between text-xs bg-green-50 dark:bg-green-950/30 p-2 rounded border border-green-200 dark:border-green-900">
                                        <span className="truncate max-w-[180px] dark:text-green-300">{file.name}</span>
                                        <button
                                          type="button"
                                          onClick={() => removeFile(doc.id, index)}
                                          className="text-slate-500 hover:text-red-500"
                                        >
                                          <X className="h-3 w-3" />
                                        </button>
                                      </div>
                                    ))}
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      <div className="flex gap-3 mt-4">
                        <Button
                          type="submit"
                          className="flex-1"
                          disabled={isSaving}
                        >
                          <Save className="mr-2 h-4 w-4" />
                          {isSaving ? "Saving..." : "Save Application"}
                        </Button>
                        <Button
                          type="button"
                          variant="outline"
                          className="flex-1 dark:border-slate-700 dark:text-white"
                          onClick={() => navigate("/homepage")}
                        >
                          Cancel
                        </Button>
                      </div>
                    </form>
                  </CardContent>
                </Card>

                {/* Task Management Card */}
                <Card className="dark:bg-slate-800 dark:border-slate-700">
                  <CardHeader>
                    <CardTitle className="dark:text-white">Application Tasks</CardTitle>
                    <p className="text-sm text-muted-foreground dark:text-slate-400">
                      Track your progress with internal deadlines
                    </p>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Existing Tasks List */}
                    {tasks.length > 0 && (
                      <div className="space-y-2">
                        {tasks.map((task) => (
                          <div
                            key={task.task_id}
                            className="p-3 border rounded-lg dark:border-slate-700 flex items-start gap-3"
                          >
                            <input
                              type="checkbox"
                              checked={task.completed}
                              onChange={(e) => handleToggleTask(task.task_id, e.target.checked)}
                              className="mt-1"
                            />
                            <div className="flex-1">
                              <h4 className={`font-medium dark:text-white ${task.completed ? "line-through text-muted-foreground" : ""}`}>
                                {task.task_name}
                              </h4>
                              {task.task_description && (
                                <p className="text-sm text-muted-foreground dark:text-slate-400 mt-1">
                                  {task.task_description}
                                </p>
                              )}
                              <p className="text-xs text-muted-foreground dark:text-slate-500 mt-1">
                                Due: {formatDate(task.deadline)}
                              </p>
                            </div>
                            <Button
                              variant="ghost"
                              size="icon"
                              onClick={() => handleDeleteTask(task.task_id)}
                              className="text-red-500 hover:text-red-600"
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          </div>
                        ))}
                      </div>
                    )}

                    {tasks.length === 0 && (
                      <p className="text-sm text-center text-muted-foreground dark:text-slate-400 py-4">
                        No tasks yet. Add tasks below to track your application progress.
                      </p>
                    )}

                    <Separator className="dark:bg-slate-700" />

                    {/* Add New Task Form */}
                    <div className="space-y-3">
                      <h4 className="font-medium dark:text-white">Add New Task</h4>
                      <div className="space-y-2">
                        <Input
                          placeholder="Task name *"
                          value={newTaskName}
                          onChange={(e) => setNewTaskName(e.target.value)}
                          className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                        />
                        <Input
                          placeholder="Description (optional)"
                          value={newTaskDescription}
                          onChange={(e) => setNewTaskDescription(e.target.value)}
                          className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                        />
                        <Input
                          type="date"
                          value={newTaskDeadline}
                          onChange={(e) => setNewTaskDeadline(e.target.value)}
                          max={grant?.date_closed ? grant.date_closed.split('T')[0] : undefined}
                          className="dark:bg-slate-900 dark:border-slate-700 dark:text-white"
                        />
                        <p className="text-xs text-muted-foreground dark:text-slate-500">
                          Task deadline cannot exceed grant deadline: {formatDate(grant?.date_closed)}
                        </p>
                        <Button
                          onClick={handleAddTask}
                          disabled={isAddingTask || !newTaskName || !newTaskDeadline}
                          className="w-full"
                        >
                          {isAddingTask ? "Adding..." : "Add Task"}
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8 mt-auto">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

function getStatusColor(status: string) {
  switch (status) {
    case "approved":
      return "bg-green-500 hover:bg-green-600 text-white";
    case "rejected":
      return "bg-red-500 hover:bg-red-600 text-white";
    case "in_review":
      return "bg-blue-500 hover:bg-blue-600 text-white";
    default:
      return "bg-slate-500 hover:bg-slate-600 text-white";
  }
}

export default ApplicationEditPage;
