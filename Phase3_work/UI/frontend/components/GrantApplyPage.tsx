import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "./ui/card";
import { Badge } from "./ui/badge";
import { Separator } from "./ui/separator";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Textarea } from "./ui/textarea";
import { Calendar, CheckCircle2, FileText, Link as LinkIcon, Upload, AlertCircle, X } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "./ui/alert";

// --- Interfaces based on Schema ---

interface Grant {
  grant_id: string;
  grant_title: string;
  opportunity_number: string;
  description: string;
  research_field: string;
  expected_award_count?: number;
  eligibility?: string;
  award_max_amount?: number;
  award_min_amount?: number;
  program_funding?: number;
  provider: string;
  link_to_source: string;
  point_of_contact?: string;
  date_posted?: string;
  archive_date?: string;
  date_closed?: string;
  last_update_date?: string;
}

interface DocumentUpload {
  id: string;
  files: File[];
  type: string;
}

// --- Mock Data ---

const MOCK_GRANT: Grant = {
  grant_id: "550e8400-e29b-41d4-a716-446655440001",
  grant_title: "Sustainable Urban Development Initiative",
  opportunity_number: "SUDI-2025-XYZ",
  description: "This grant aims to support innovative projects that promote sustainable urban development, focusing on green infrastructure, energy efficiency, and community resilience. Proposals should demonstrate a clear impact on reducing carbon footprints and improving quality of life in urban areas.",
  research_field: "Urban Planning / Environmental Science",
  expected_award_count: 10,
  eligibility: "Local governments, non-profit organizations, and academic institutions.",
  award_max_amount: 250000,
  award_min_amount: 50000,
  program_funding: 2500000,
  provider: "Department of Environmental Conservation",
  link_to_source: "https://www.grants.gov/web/grants/view-opportunity.html?oppId=98765",
  point_of_contact: "grants@dec.gov",
  date_posted: "2025-10-01",
  date_closed: "2025-12-15",
  last_update_date: "2025-10-05",
};

// --- Helper Functions ---

const formatCurrency = (amount?: number) => {
  if (amount === undefined) return "N/A";
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
};

const formatDate = (dateString?: string) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString();
};

export function GrantApplyPage() {
  const navigate = useNavigate();
  const [grant] = useState<Grant>(MOCK_GRANT);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  // Form State
  const [applicantName, setApplicantName] = useState("");
  const [applicantEmail, setApplicantEmail] = useState("");

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('access_token');
    navigate('/');
  };
  
  // Document Uploads State
  const [documents, setDocuments] = useState<DocumentUpload[]>([
    { id: "1", type: "Proposal", files: [] },
    { id: "2", type: "Budget", files: [] },
    { id: "3", type: "CV/Resume", files: [] },
    { id: "4", type: "Cover Letter", files: [] },
  ]);

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSuccess(true);
      // In a real app, this would create the Application record and upload Documents
    }, 2000);
  };

  if (isSuccess) {
    return (
      <div className="container mx-auto py-20 px-4 max-w-2xl text-center space-y-6">
        <div className="flex justify-center">
          <CheckCircle2 className="h-24 w-24 text-green-500" />
        </div>
        <h1 className="text-3xl font-bold dark:text-white">Application Submitted!</h1>
        <p className="text-muted-foreground dark:text-slate-400">
          Your application for <strong>{grant.grant_title}</strong> has been successfully submitted. 
          You will receive a confirmation email at {applicantEmail}.
        </p>
        <div className="flex justify-center gap-4 pt-4">
          <Button variant="outline" onClick={() => setIsSuccess(false)}>Return to Grant</Button>
          <Button>View My Applications</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation Header */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">Apply for Grant</span>
          </div>
          <div className="flex items-center gap-3">
            <Link to="/homepage">
              <Button variant="ghost">Home</Button>
            </Link>
            <Link to="/applications">
              <Button variant="ghost">My Applications</Button>
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
        {/* Header */}
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>Grants</span>
            <span>/</span>
            <span>{grant.research_field}</span>
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
              Opp #: {grant.opportunity_number}
            </span>
          </div>
        </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Grant Details */}
        <div className="lg:col-span-2 space-y-8">
          <Card className="dark:bg-slate-800 dark:border-slate-700">
            <CardHeader>
              <CardTitle>Grant Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div>
                <h3 className="font-semibold mb-2">Description</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {grant.description}
                </p>
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
                      <span className="font-medium">{grant.expected_award_count}</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Eligibility & Contact</h3>
                  <div className="space-y-4 text-sm">
                    <div>
                      <span className="text-muted-foreground block mb-1">Eligible Applicants:</span>
                      <p>{grant.eligibility}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground block mb-1">Point of Contact:</span>
                      <p>{grant.point_of_contact}</p>
                    </div>
                  </div>
                </div>
              </div>

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
            </CardContent>
          </Card>
        </div>

        {/* Right Column: Application Form */}
        <div className="lg:col-span-1">
          <Card className="sticky top-6 dark:bg-slate-800 dark:border-slate-700 border-t-4 border-t-blue-600 shadow-lg">
            <CardHeader>
              <CardTitle>Apply Now</CardTitle>
              <CardDescription>
                Submit your application for this grant.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Applicant Name</Label>
                  <Input 
                    id="name" 
                    placeholder="Your Name or Organization" 
                    required 
                    value={applicantName}
                    onChange={(e) => setApplicantName(e.target.value)}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="email">Contact Email</Label>
                  <Input 
                    id="email" 
                    type="email" 
                    placeholder="email@example.com" 
                    required 
                    value={applicantEmail}
                    onChange={(e) => setApplicantEmail(e.target.value)}
                  />
                </div>

                <Separator />

                <div className="space-y-3">
                  <Label>Required Documents</Label>
                  {documents.map((doc) => (
                    <div key={doc.id} className="space-y-2">
                      <span className="text-xs font-medium text-muted-foreground">{doc.type}</span>
                      <div className="space-y-2">
                        <div className="items-center gap-2">
                           <input
                              type="file"
                              multiple
                              className="hidden"
                              id={`file-upload-${doc.id}`}
                              onChange={(e) => {
                                handleFileChange(doc.id, e.target.files);
                                e.target.value = ''; // Reset input
                              }}
                           />
                           <Button asChild variant="outline" size="sm" className="w-full cursor-pointer">
                              <label htmlFor={`file-upload-${doc.id}`}>
                                <Upload className="mr-2 h-3 w-3" /> Browse Files
                              </label>
                           </Button>
                        </div>
                        {doc.files.length > 0 && (
                          <div className="space-y-1">
                            {doc.files.map((file, index) => (
                              <div key={index} className="flex items-center justify-between text-xs bg-slate-100 dark:bg-slate-900 p-2 rounded">
                                <span className="truncate max-w-[180px]">{file.name}</span>
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

                <Button type="submit" className="w-full mt-4" disabled={isSubmitting}>
                  {isSubmitting ? "Submitting..." : "Submit Application"}
                </Button>
              </form>
            </CardContent>
            <CardFooter className="text-center">
              By submitting, you agree to our Terms of Service and Privacy Policy.
            </CardFooter>
          </Card>
        </div>
      </div>
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
