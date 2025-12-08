import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Search, TrendingUp, Clock, Award } from "lucide-react";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { AuthDialog } from "./AuthDialog";

export function LandingPage() {
  const [authOpen, setAuthOpen] = useState(false);
  const [authTab, setAuthTab] = useState<"login" | "signup">("login");
  const [aggregateGrants, setAggregateGrants] = useState<string>("0");
  const [aggregateFunding, setAggregateFunding] = useState<string>("0");

  const handleOpenLogin = () => {
    setAuthTab("login");
    setAuthOpen(true);
  };

  const handleOpenSignup = () => {
    setAuthTab("signup");
    setAuthOpen(true);
  };


useEffect(() => {
  async function fetchAggregateFunding() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/public/aggregate-grants");
      const data = await response.json();
      if (data.total) {
        setAggregateFunding(data.total);
      }
    } catch (err) {
      console.error("Failed to fetch aggregate grants:", err);
    }
  }

  fetchAggregateFunding();
}, []);



useEffect(() => {
  async function fetchAllGrants() {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/public/fetch_grant_count");
      const data = await response.json();

      if (data.total) {
        setAggregateGrants(data.total);
      }
    } catch (err) {
      console.error("Failed to fetch grant counts:", err);
    }
  }

  fetchAllGrants();
}, []);


  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white dark:from-slate-950 dark:to-slate-900">
      {/* Navigation */}
      <nav className="border-b bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50 dark:border-slate-800">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="dark:text-white">GrantGuru</span>
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" onClick={handleOpenLogin}>
              Log In
            </Button>
            <Button onClick={handleOpenSignup}>
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h1 className="text-5xl dark:text-white">
              Find the Perfect Grant for Your Research
            </h1>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Access thousands of funding opportunities from government agencies, foundations, and corporations. 
            </p>
            <div className="flex gap-4">
              <Button size="lg" onClick={handleOpenSignup}>
                Start Searching for Free
              </Button>
              <Button size="lg" variant="outline" onClick={handleOpenLogin}>
                Log In
              </Button>
            </div>
            <div className="flex gap-8 pt-4">
              <div>
                <div className="dark:text-white">{aggregateGrants}</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">  Active Grants </div>
              </div>
              <div>
                <div className="dark:text-white">{aggregateFunding}</div>
                <div className="text-sm text-slate-600 dark:text-slate-400">Current Funding </div>
              </div>
            </div>
          </div>
          <div className="relative">
            <ImageWithFallback 
              src="https://images.unsplash.com/photo-1630344745991-fb948c5bf9d1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxidXNpbmVzcyUyMGdyb3d0aCUyMHN1Y2Nlc3N8ZW58MXx8fHwxNzYzNzg3NTgwfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
              alt="Business growth"
              className="rounded-2xl shadow-2xl w-full"
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h2 className="text-4xl mb-4 dark:text-white">Why Choose GrantGuru?</h2>
          <p className="text-xl text-slate-600 dark:text-slate-300">
            Powerful tools to streamline your grant search and application process
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="p-6 space-y-4 dark:bg-slate-800 dark:border-slate-700">
            <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
              <Search className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="dark:text-white">Smart Search</h3>
            <p className="text-slate-600 dark:text-slate-300">
		Free-to-use database with the latest grants from top grant websites
            </p>
          </Card>
          <Card className="p-6 space-y-4 dark:bg-slate-800 dark:border-slate-700">
            <div className="w-12 h-12 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
              <TrendingUp className="h-6 w-6 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="dark:text-white">Preemptive Notifications</h3>
            <p className="text-slate-600 dark:text-slate-300">
		Opt-in notifications for forecasted and posted grants
            </p>
          </Card>
          <Card className="p-6 space-y-4 dark:bg-slate-800 dark:border-slate-700">
            <div className="w-12 h-12 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
              <Clock className="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="dark:text-white">Deadline Tracking</h3>
            <p className="text-slate-600 dark:text-slate-300">
              Automated reminders and deadline notifications
            </p>
          </Card>
          <Card className="p-6 space-y-4 dark:bg-slate-800 dark:border-slate-700">
            <div className="w-12 h-12 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
              <Award className="h-6 w-6 text-amber-600 dark:text-amber-400" />
            </div>
            <h3 className="dark:text-white">Document Storage</h3>
            <p className="text-slate-600 dark:text-slate-300">
		Upload and manage documents associated with your applications for easy management
            </p>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-slate-50 dark:bg-slate-900/50 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 dark:text-white">How It Works</h2>
            <p className="text-xl text-slate-600 dark:text-slate-300">
              Get started in three simple steps
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-blue-600 dark:bg-blue-500 text-white flex items-center justify-center mx-auto">
                1
              </div>
              <h3 className="dark:text-white">Create Your Profile</h3>
              <p className="text-slate-600 dark:text-slate-300">
                Tell us about your organization, project, and funding needs
              </p>
            </div>
            <div className="text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-blue-600 dark:bg-blue-500 text-white flex items-center justify-center mx-auto">
                2
              </div>
              <h3 className="dark:text-white">Discover Grants</h3>
              <p className="text-slate-600 dark:text-slate-300">
                Browse personalized grant recommendations matched to your profile
              </p>
            </div>
            <div className="text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-blue-600 dark:bg-blue-500 text-white flex items-center justify-center mx-auto">
                3
              </div>
              <h3 className="dark:text-white">Apply with Confidence</h3>
              <p className="text-slate-600 dark:text-slate-300">
                Track deadlines and build grant applications with our tools
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20">
        <Card className="p-12 bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-700 dark:to-blue-800 text-white text-center space-y-6 border-0">
          <h2 className="text-4xl">Ready to Find Your Funding?</h2>
          <p className="text-xl opacity-90">
		Get Started Now
          </p>
          <Button size="lg" variant="secondary" onClick={handleOpenSignup}>
            Create Free Account
          </Button>
        </Card>
      </section>

      {/* Footer */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>

      {/* Auth Dialog */}
      <AuthDialog open={authOpen} onOpenChange={setAuthOpen} defaultTab={authTab} />
    </div>
  );
}
