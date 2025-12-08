// AuthDialog.tsx
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "./ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Award } from "lucide-react";
import { useNavigate } from "react-router-dom";



const API_BASE_URL = "http://127.0.0.1:5000"; 

interface AuthDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  defaultTab?: "login" | "signup";
}



export function AuthDialog({ open, onOpenChange, defaultTab = "login" }: AuthDialogProps) {
  const navigate = useNavigate(); // ADD THIS LINE
  const [activeTab, setActiveTab] = useState(defaultTab);
 
  // Login form state
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });

  // Sign up form state
  const [signupData, setSignupData] = useState({
    firstName: "",
    middleName: "",
    lastName: "",
    email: "",
    institutionName: "",
    password: "",
    confirmPassword: "",
    acceptTerms: false,
  });


  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Login payload:", loginData);

    const payload = {
      email: loginData.email,
      password: loginData.password
    };

    try {
      const res = await fetch(`${API_BASE_URL}/api/auth/signin`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        alert("Login failed: " + data.error);
        return;
      }

      sessionStorage.setItem("access_token", data.access_token);


      onOpenChange(false); // Close the dialog
      navigate("/homepage");
 
    } catch (err) {
      console.error("Network or server error during login:", err);
      alert("Network error. Please try again.");
    }
  };

const handleSignup = async (e: React.FormEvent) => {
  e.preventDefault();

  const payload = {
    email: signupData.email,
    password: signupData.password,
    firstName: signupData.firstName,
    middleName: signupData.middleName,
    lastName: signupData.lastName,
    institutionName: signupData.institutionName,
  };



if (signupData.password.length < 8) {
  alert("Signup failed.  Password must be at least 8 characters long");
  return;
}
	
if (signupData.password !== signupData.confirmPassword) {
    alert("Signup failed.  Passwords do not match");
    return;
}

  try {
    const res = await fetch(`${API_BASE_URL}/api/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (!res.ok) {
      alert("Signup failed: " + data.error);
      return;
    }

    console.log("User created:", data.user_id);
    alert("[DEBUG] Account created successfully!");
    
  } catch (err: unknown) {
    if (err instanceof Error) {
      console.error(err.stack); // prints stack trace
      alert(`Error: ${err.message}`);
    } else {
      console.error(err);
      alert("Network error");
  }
}
};


  // Update active tab when defaultTab changes
  useEffect(() => {
    setActiveTab(defaultTab);
  }, [defaultTab]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
	<DialogContent className="sm:max-w-[480px] overflow-y-auto dark:bg-slate-800 dark:border-slate-700">
	<DialogHeader />
	<DialogDescription className="sr-only">
	    Authentication dialog for login or signup
	</DialogDescription>
        
        <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as "login" | "signup")} className="w-full">
          <TabsList className="grid w-full grid-cols-2 dark:bg-slate-900">
            <TabsTrigger value="login">Log In</TabsTrigger>
            <TabsTrigger value="signup">Sign Up</TabsTrigger>
          </TabsList>
          
          <TabsContent value="login" className="space-y-4 mt-6">
            <div className="text-center space-y-2 mb-6">
              <DialogTitle className="text-2xl dark:text-white">Welcome Back</DialogTitle>
              <p className="text-slate-600 dark:text-slate-300">
                Log in to continue your grant search
              </p>
            </div>

            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="login-email" className="dark:text-slate-200">Email Address</Label>
                <Input
                  id="login-email"
                  type="email"
                  placeholder="you@example.com"
                  value={loginData.email}
                  onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
                  required
                  className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                />
              </div>

              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="login-password" className="dark:text-slate-200">Password</Label>
                </div>
                <Input
                  id="login-password"
                  type="password"
                  placeholder="••••••••"
                  value={loginData.password}
                  onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                  required
                  className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                />
              </div>

              <Button type="submit" className="w-full" size="lg">
                Log In
              </Button>
            </form>

            <div className="grid grid-cols-2 gap-4">
            </div>
          </TabsContent>
          
          <TabsContent value="signup" className="space-y-4 mt-6">
            <div className="text-center space-y-2 mb-6">
              <DialogTitle className="text-2xl dark:text-white">Create Your Account</DialogTitle>
              <p className="text-slate-600 dark:text-slate-300">
                Start discovering grants today!
              </p>
            </div>

            <form onSubmit={handleSignup} className="space-y-4">
		<div className="grid grid-cols-3 gap-4">
		  <div className="space-y-2">
		    <Label htmlFor="signup-first" className="dark:text-slate-200">First Name</Label>
		    <Input
		      id="signup-first"
		      type="text"
		      placeholder="John"
		      value={signupData.firstName}
		      onChange={(e) => setSignupData({ ...signupData, firstName: e.target.value })}
		      required
		      className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
		    />
		  </div>

		  <div className="space-y-2">
		    <Label htmlFor="signup-middle" className="dark:text-slate-200">Middle</Label>
		    <Input
		      id="signup-middle"
		      type="text"
		      placeholder="A."
		      value={signupData.middleName}
		      onChange={(e) => setSignupData({ ...signupData, middleName: e.target.value })}
		      className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
		    />
		  </div>

		  <div className="space-y-2">
		    <Label htmlFor="signup-last" className="dark:text-slate-200">Last Name</Label>
		    <Input
		      id="signup-last"
		      type="text"
		      placeholder="Doe"
		      value={signupData.lastName}
		      onChange={(e) => setSignupData({ ...signupData, lastName: e.target.value })}
		      required
		      className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
		    />
		  </div>
		</div>

              <div className="space-y-2">
                <Label htmlFor="signup-email" className="dark:text-slate-200">Email Address</Label>
                <Input
                  id="signup-email"
                  type="email"
                  placeholder="you@example.com"
                  value={signupData.email}
                  onChange={(e) => setSignupData({ ...signupData, email: e.target.value })}
                  required
                  className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                />
              </div>

		<div className="space-y-2">
		    <Label htmlFor="signup-org" className="dark:text-slate-200">Institution/Organization Name</Label>
		    <Input
			type="text"
			id="signup-org"
			placeholder=" Your Institution"
			value={signupData.institutionName}
			onChange={(e) => setSignupData({ ...signupData, institutionName: e.target.value })}
			 required
			 className="w-full p-3 border border-slate-300 rounded-lg dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
		    />
		</div>



              <div className="space-y-2">
                <Label htmlFor="signup-password" className="dark:text-slate-200">Password</Label>
                <Input
                  id="signup-password"
                  type="password"
                  placeholder="••••••••"
                  value={signupData.password}
                  onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
                  required
                  className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                />
                <p className="text-sm text-slate-500 dark:text-slate-400">
                  Must be at least 8 characters
                </p>
              </div>

              <div className="space-y-2">
                <Label htmlFor="signup-confirm" className="dark:text-slate-200">Confirm Password</Label>
                <Input
                  id="signup-confirm"
                  type="password"
                  placeholder="••••••••"
                  value={signupData.confirmPassword}
                  onChange={(e) => setSignupData({ ...signupData, confirmPassword: e.target.value })}
                  required
                  className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                />
              </div>

              <Button 
                type="submit" 
                className="w-full" 
                size="lg"
              >
                Create Account
              </Button>
            </form>

          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
