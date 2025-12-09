import React, { useEffect, useState } from "react";
import DOMPurify from "dompurify";
import { useParams, Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { Label } from "./ui/label";
import { Calendar, LinkIcon, Upload, AlertCircle, X, Building2 } from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:5000";

interface DocumentUpload {
  id: string;
  files: File[];
  type: string;
}

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

export function GrantDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [grant, setGrant] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Form State (removed applicant name/email - users track their own applications)

  // Document Uploads State
  const [documents, setDocuments] = useState<DocumentUpload[]>([
    { id: "1", type: "Proposal", files: [] },
    { id: "2", type: "Budget", files: [] },
    { id: "3", type: "CV/Resume", files: [] },
    { id: "4", type: "Cover Letter", files: [] },
  ]);

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('access_token');
    navigate('/');
  };

  const scrollToApplication = () => {
    const applicationSection = document.getElementById('application-form');
    if (applicationSection) {
      applicationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
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

  const handleSaveDraft = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const token = sessionStorage.getItem("access_token");
      if (!token) {
        alert("Please log in to apply for grants");
        navigate("/");
        return;
      }

      // Step 1: Create the application
      const response = await fetch("http://127.0.0.1:5000/api/user/applications", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          grant_id: grant.grant_id,
          submission_status: "started",
          status: "pending",
        }),
      });

      const data = await response.json();

      if (response.ok) {
        const applicationId = data.application.application_id;

        // Step 2: Upload documents if any files were selected
        const hasFiles = documents.some(doc => doc.files.length > 0);

        if (hasFiles) {
          for (const doc of documents) {
            if (doc.files.length > 0) {
              const formData = new FormData();
              doc.files.forEach(file => {
                formData.append('files', file);
              });
              formData.append('document_type', doc.type);

              const uploadResponse = await fetch(
                `http://127.0.0.1:5000/api/user/applications/${applicationId}/documents`,
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
      } else if (response.status === 409) {
        alert(data.error || "You have already applied to this grant");
        setIsSubmitting(false);
      } else if (response.status === 401) {
        alert("Session expired. Please log in again.");
        sessionStorage.removeItem("user_id");
        sessionStorage.removeItem("access_token");
        navigate("/");
      } else {
        alert(data.error || "Failed to save application");
        setIsSubmitting(false);
      }
    } catch (error) {
      console.error("Error with application:", error);
      alert(
        "Unable to connect to the server. Please ensure:\n" +
        "1. The Flask API server is running (port 5000)\n" +
        "2. You have network connectivity\n\n" +
        "Error: " + (error instanceof Error ? error.message : "Unknown error")
      );
      setIsSubmitting(false);
    }
  };

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
      {/* Navigation Header */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Grant Details & Application</span>
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
        <Link to="/searchGrants" className="text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200">
          ← Back to search
        </Link>

        {/* Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Grants</span>
            <span>/</span>
            <span>{grant.research_field || "General"}</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-bold dark:text-white">{grant.grant_title}</h1>
          <div className="flex flex-wrap gap-4 items-center pt-2">
            <Badge variant="secondary" className="text-sm">
              {grant.provider}
            </Badge>
            <span className="text-sm text-muted-foreground flex items-center gap-1">
              <Calendar className="h-4 w-4" />
              Deadline: <span className="text-red-500 font-medium">{formatDate(grant.date_closed)}</span>
            </span>
            <span className="text-sm text-muted-foreground">
              Opp #: {grant.opportunity_number || "N/A"}
            </span>
          </div>
        </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Grant Details */}
        <div className="lg:col-span-2 space-y-8">
          <Card className="dark:bg-slate-800 dark:border-slate-700">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Grant Details</CardTitle>
                <Button
                  onClick={scrollToApplication}
                  size="sm"
                  className="bg-blue-600 hover:bg-blue-700 text-white"
                >
                  Start Application
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="font-semibold mb-2">Description</h3>
                <div
                  className="text-muted-foreground leading-relaxed prose dark:prose-invert max-w-none"
                  dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(grant.description || "") }}
                />
              </div>

              <Separator />

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold mb-2">Funding Information</h3>
                  <ul className="space-y-2 text-sm">
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Total Program Funding:</span>
                      <span className="font-medium">{formatCurrency(grant.program_funding)}</span>
                    </li>
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Award Ceiling:</span>
                      <span className="font-medium">{formatCurrency(grant.award_max_amount)}</span>
                    </li>
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Award Floor:</span>
                      <span className="font-medium">{formatCurrency(grant.award_min_amount)}</span>
                    </li>
                    <li className="flex justify-between">
                      <span className="text-muted-foreground">Expected Awards:</span>
                      <span className="font-medium">{grant.expected_award_count || "N/A"}</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Eligibility</h3>
                  <div className="space-y-4 text-sm">
                    <div>
                      <span className="text-muted-foreground block mb-1">Eligible Applicants:</span>
                      <p>{grant.eligibility || "N/A"}</p>
                    </div>
                  </div>
                </div>
              </div>

              {grant.link_to_source && (
                <div className="bg-slate-50 dark:bg-slate-900 p-4 rounded-lg border dark:border-slate-700">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="h-5 w-5 text-blue-500 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-sm">External Link</h4>
                      <p className="text-sm text-muted-foreground mb-2">
                        View the full opportunity announcement on the provider's website.
                      </p>
                      <a
                        href={grant.link_to_source}
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm text-blue-600 hover:underline flex items-center gap-1"
                      >
                        Visit Source <LinkIcon className="h-3 w-3" />
                      </a>
                    </div>
                  </div>
                </div>
              )}
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
                  <CardDescription>
                    Get in touch with the grant provider for questions and support
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {contact.name && (
                    <div className="p-5 bg-slate-50 dark:bg-slate-900 rounded-lg border dark:border-slate-700">
                      <p className="text-xs font-medium text-muted-foreground mb-1">Organization</p>
                      <p className="font-semibold text-slate-900 dark:text-white">{contact.name}</p>
                    </div>
                  )}

                  {contact.email && (
                    <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border dark:border-slate-700">
                      <p className="text-xs  font-medium text-muted-foreground mb-1">Email Address</p>
                      <a
                        href={`mailto:${contact.email}`}
                        className="text-blue-600 dark:text-blue-400 hover:underline font-medium break-all"
                      >
                        {contact.email}
                      </a>
                      {contact.email_desc && (
                        <p className="text-sm text-muted-foreground mt-2 leading-relaxed">
                          {contact.email_desc}
                        </p>
                      )}
                    </div>
                  )}

                  {contact.phone && (
                    <div className="p-4 bg-slate-50 dark:bg-slate-900 rounded-lg border dark:border-slate-700">
                      <p className="text-xs font-medium text-muted-foreground mb-1">Phone Number</p>
                      <a
                        href={`tel:${contact.phone}`}
                        className="text-green-600 dark:text-green-400 hover:underline font-medium"
                      >
                        {contact.phone}
                      </a>
                    </div>
                  )}

                  {contact.desc && (
                    <div className="p-4 bg-blue-50 dark:bg-blue-950/30 rounded-lg border border-blue-200 dark:border-blue-900">
                      <p className="text-xs font-medium text-blue-900 dark:text-blue-300 mb-1">Additional Information</p>
                      <p className="text-sm text-blue-800 dark:text-blue-200 leading-relaxed whitespace-pre-wrap">
                        {contact.desc}
                      </p>
                    </div>
                  )}
                </CardContent>
              </Card>
            );
          })()}
        </div>

        {/* Right Column: Application Form */}
        <div className="lg:col-span-1" id="application-form">
          <Card className="sticky top-6 dark:bg-slate-800 dark:border-slate-700 border-t-4 border-t-blue-600 shadow-lg">
            <CardHeader>
              <CardTitle className="dark:text-white">Application Form</CardTitle>
              <CardDescription className="dark:text-slate-400">
                Save your application progress.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSaveDraft} className="space-y-4">
                <div className="space-y-3">
                  <Label className="dark:text-slate-300">Required Documents</Label>
                  {documents.map((doc) => (
                    <div key={doc.id} className="space-y-2">
                      <span className="text-xs font-medium text-muted-foreground dark:text-slate-400">{doc.type}</span>

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
                              <Upload className="mr-2 h-3 w-3" /> Browse Files
                            </label>
                          </Button>
                        </div>
                        {doc.files.length > 0 && (
                          <div className="space-y-1">
                            <p className="text-xs text-muted-foreground dark:text-slate-500">Files to upload:</p>
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
                  ))}
                </div>

                <div className="mt-4">
                  <Button
                    type="submit"
                    className="w-full"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? "Saving..." : "Save Application"}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
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

      {/* Footer */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default GrantDetailsPage;
