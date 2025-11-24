// HomePage.tsx
import { Link, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { ThemeToggle } from "./ThemeToggle";

export function HomePage() {
  const userId = localStorage.getItem("user_id");
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear user data from localStorage
    localStorage.removeItem('user_id');
    localStorage.removeItem('access_token');
  
    // Navigate to landing page
    navigate('/');
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
            {/* User Settings */}
            <Link to="/user">
              <Button variant="ghost">User Settings</Button>
            </Link>
            {/* Logout Button */}
            <Button variant="outline" onClick={handleLogout}>Logout</Button>
          </div>
        </div>
      </nav>

      {/* Main Content (intentionally blank) */}
      <main className="flex-1 container mx-auto px-4 py-20">
        {/* blank as requested */}
      </main>

      {/* Footer (same styling as LandingPage) */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
