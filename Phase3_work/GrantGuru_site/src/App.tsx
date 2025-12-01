import { useState } from "react";
import { LandingPage } from "./components/LandingPage";
import { ApplicationsPage } from "./components/ApplicationsPage";
import { ApplicationDetailsPage } from "./components/ApplicationDetailsPage";
import { GrantApplyPage } from "./components/GrantApplyPage";
import { ThemeProvider } from "./components/ThemeProvider";
import { ThemeToggle } from "./components/ThemeToggle";
import { Award } from "lucide-react";

export default function App() {
  const [currentView, setCurrentView] = useState<"landing" | "applications" | "application-details" | "grant-apply">("landing");

  return (
    <ThemeProvider>
      {currentView === "landing" ? (
        <LandingPage onNavigateToApplications={() => setCurrentView("applications")} />
      ) : (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-950">
          <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
              <div 
                className="flex items-center gap-2 cursor-pointer" 
                onClick={() => setCurrentView("landing")}
              >
                <Award className="h-8 w-8 text-blue-600 dark:text-blue-500" />
                <span className="font-bold text-xl dark:text-white">GrantGuru</span>
              </div>
              <div className="flex items-center gap-3">
                <ThemeToggle />
                <button 
                  onClick={() => setCurrentView("landing")} 
                  className="text-sm font-medium hover:underline dark:text-white"
                >
                  Back to Home
                </button>
              </div>
            </div>
          </nav>
          {currentView === "applications" && (
            <ApplicationsPage 
              onViewDetails={() => setCurrentView("application-details")} 
              onApply={() => setCurrentView("grant-apply")}
            />
          )}
          {currentView === "application-details" && (
            <div className="container mx-auto py-6">
              <button 
                onClick={() => setCurrentView("applications")}
                className="mb-4 text-sm text-blue-600 hover:underline dark:text-blue-400 px-4"
              >
                &larr; Back to Applications
              </button>
              <ApplicationDetailsPage />
            </div>
          )}
          {currentView === "grant-apply" && (
            <div className="container mx-auto py-6">
              <button 
                onClick={() => setCurrentView("applications")}
                className="mb-4 text-sm text-blue-600 hover:underline dark:text-blue-400 px-4"
              >
                &larr; Back to Applications
              </button>
              <GrantApplyPage />
            </div>
          )}
        </div>
      )}
    </ThemeProvider>
  );
}