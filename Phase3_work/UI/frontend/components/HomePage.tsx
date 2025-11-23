// HomePage.tsx
import { Link } from "react-router-dom";
import { Button } from "./ui/button";
import { ThemeToggle } from "./ThemeToggle";

export function HomePage() {
  const userId = localStorage.getItem("user_id");

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950">
      {/* Navigation (same style as LandingPage) */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white text-lg font-semibold">GrantGuru</span>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            {/* Go to User Settings */}
            <Link to="/user">
              <Button variant="ghost">User Settings</Button>
            </Link>

            {/* Log Out (optional, remove if you don't want) */}
            {/* <Button variant="outline">Log Out</Button> */}
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
