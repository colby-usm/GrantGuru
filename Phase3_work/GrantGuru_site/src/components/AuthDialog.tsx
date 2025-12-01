import React, { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "./ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Checkbox } from "./ui/checkbox";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { Award } from "lucide-react";

interface LoginFormData {
  email: string;
  password: string;
  rememberMe: boolean;
}

interface SignupFormData {
  fullName: string;
  email: string;
  organizationType: string;
  password: string;
  confirmPassword: string;
  acceptTerms: boolean;
}

interface AuthDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  defaultTab?: "login" | "signup";
}

export function AuthDialog({ open, onOpenChange, defaultTab = "login" }: AuthDialogProps) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  // Login form state
  const [loginData, setLoginData] = useState({
    email: "",
    password: "",
    rememberMe: false,
  });

  // Sign up form state
  const [signupData, setSignupData] = useState({
    fullName: "",
    email: "",
    organizationType: "",
    password: "",
    confirmPassword: "",
    acceptTerms: false,
  });

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Login:", loginData);
    // Handle login logic here
  };

  const handleSignup = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Sign up:", signupData);
    // Handle signup logic here
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] dark:bg-slate-800 dark:border-slate-700">
        <DialogHeader>
          <DialogTitle className="sr-only">Authentication</DialogTitle>
        </DialogHeader>
        
        <Tabs value={activeTab} onValueChange={(value: string) => setActiveTab(value as "login" | "signup")} className="w-full">
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
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLoginData({ ...loginData, email: e.target.value })}
                          required
                          className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <Label htmlFor="login-password" className="dark:text-slate-200">Password</Label>
                          <Button 
                            type="button" 
                            variant="link" 
                            className="p-0 h-auto dark:text-blue-400"
                          >
                            Forgot password?
                          </Button>
                        </div>
                        <Input
                          id="login-password"
                          type="password"
                          placeholder="••••••••"
                          value={loginData.password}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLoginData({ ...loginData, password: e.target.value })}
                          required
                          className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                        />
                      </div>

                      <div className="flex items-center space-x-2">
                        <Checkbox 
                          id="remember" 
                          checked={loginData.rememberMe}
                          onCheckedChange={(checked: boolean) => setLoginData({ ...loginData, rememberMe: checked as boolean })}
                        />
                        <Label 
                          htmlFor="remember" 
                          className="cursor-pointer dark:text-slate-300"
                        >
                          Remember me for 30 days
                        </Label>
                      </div>

                      <Button type="submit" className="w-full" size="lg">
                        Log In
                      </Button>
                    </form>

                    <div className="relative">
                      <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t dark:border-slate-700"></div>
                      </div>
                      <div className="relative flex justify-center">
                        <span className="bg-white dark:bg-slate-800 px-4 text-sm text-slate-500 dark:text-slate-400">
                          Or continue with
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <Button variant="outline" type="button" className="dark:bg-slate-900 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700">
                        <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                          <path
                            fill="currentColor"
                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                          />
                          <path
                            fill="currentColor"
                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                          />
                          <path
                            fill="currentColor"
                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                          />
                          <path
                            fill="currentColor"
                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                          />
                        </svg>
                        Google
                      </Button>
                      <Button variant="outline" type="button" className="dark:bg-slate-900 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700">
                        <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
                        </svg>
                        GitHub
                      </Button>
                    </div>
                  </TabsContent>
                  
                  <TabsContent value="signup" className="space-y-4 mt-6">
                    <div className="text-center space-y-2 mb-6">
                      <DialogTitle className="text-2xl dark:text-white">Create Your Account</DialogTitle>
                      <p className="text-slate-600 dark:text-slate-300">
                        Start discovering grants that match your needs
                      </p>
                    </div>

                    <form onSubmit={handleSignup} className="space-y-4">
                      <div className="space-y-2">
                        <Label htmlFor="signup-name" className="dark:text-slate-200">Full Name</Label>
                        <Input
                          id="signup-name"
                          type="text"
                          placeholder="John Doe"
                          value={signupData.fullName}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSignupData({ ...signupData, fullName: e.target.value })}
                          required
                          className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="signup-email" className="dark:text-slate-200">Email Address</Label>
                        <Input
                          id="signup-email"
                          type="email"
                          placeholder="you@example.com"
                          value={signupData.email}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSignupData({ ...signupData, email: e.target.value })}
                          required
                          className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="signup-org" className="dark:text-slate-200">Organization Type</Label>
                        <Select 
                          value={signupData.organizationType}
                          onValueChange={(value: string) => setSignupData({ ...signupData, organizationType: value })}
                        >
                          <SelectTrigger id="signup-org" className="dark:bg-slate-900 dark:border-slate-600 dark:text-white">
                            <SelectValue placeholder="Select your organization type" />
                          </SelectTrigger>
                          <SelectContent className="dark:bg-slate-900 dark:border-slate-700">
                            <SelectItem value="nonprofit" className="dark:text-slate-200">Non-Profit Organization</SelectItem>
                            <SelectItem value="university" className="dark:text-slate-200">University/Research Institution</SelectItem>
                            <SelectItem value="small-business" className="dark:text-slate-200">Small Business</SelectItem>
                            <SelectItem value="government" className="dark:text-slate-200">Government Agency</SelectItem>
                            <SelectItem value="individual" className="dark:text-slate-200">Individual Researcher</SelectItem>
                            <SelectItem value="other" className="dark:text-slate-200">Other</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="signup-password" className="dark:text-slate-200">Password</Label>
                        <Input
                          id="signup-password"
                          type="password"
                          placeholder="••••••••"
                          value={signupData.password}
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSignupData({ ...signupData, password: e.target.value })}
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
                          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSignupData({ ...signupData, confirmPassword: e.target.value })}
                          required
                          className="dark:bg-slate-900 dark:border-slate-600 dark:text-white dark:placeholder:text-slate-400"
                        />
                      </div>

                      <div className="flex items-start space-x-2">
                        <Checkbox 
                          id="terms" 
                          checked={signupData.acceptTerms}
                          onCheckedChange={(checked: boolean) => setSignupData({ ...signupData, acceptTerms: checked as boolean })}
                          className="mt-1"
                        />
                        <Label 
                          htmlFor="terms" 
                          className="cursor-pointer dark:text-slate-300"
                        >
                          I agree to the Terms of Service and Privacy Policy
                        </Label>
                      </div>

                      <Button 
                        type="submit" 
                        className="w-full" 
                        size="lg"
                        disabled={!signupData.acceptTerms}
                      >
                        Create Account
                      </Button>
                    </form>

                    <div className="relative">
                      <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t dark:border-slate-700"></div>
                      </div>
                      <div className="relative flex justify-center">
                        <span className="bg-white dark:bg-slate-800 px-4 text-sm text-slate-500 dark:text-slate-400">
                          Or sign up with
                        </span>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <Button variant="outline" type="button" className="dark:bg-slate-900 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700">
                        <svg className="h-5 w-5 mr-2" viewBox="0 0 24 24">
                          <path
                            fill="currentColor"
                            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                          />
                          <path
                            fill="currentColor"
                            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                          />
                          <path
                            fill="currentColor"
                            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                          />
                          <path
                            fill="currentColor"
                            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                          />
                        </svg>
                        Google
                      </Button>
                      <Button variant="outline" type="button" className="dark:bg-slate-900 dark:border-slate-600 dark:text-slate-200 dark:hover:bg-slate-700">
                        <svg className="h-5 w-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.463-1.11-1.463-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
                        </svg>
                        GitHub
                      </Button>
                    </div>
                  </TabsContent>
                </Tabs>
      </DialogContent>
    </Dialog>
  );
}