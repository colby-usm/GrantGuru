import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ThemeToggle } from './ThemeToggle';

export default function SettingsPage() {
  const navigate = useNavigate();
  const [personalInfo, setPersonalInfo] = useState({
    firstName: '',
    middleName: '',
    lastName: '',
    organization: ''
  });

  const [emailInfo, setEmailInfo] = useState({
    email: ''
  });

  const [passwordInfo, setPasswordInfo] = useState({
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const handlePersonalInfoChange = (e) => {
    setPersonalInfo({
      ...personalInfo,
      [e.target.name]: e.target.value
    });
  };

  const handleEmailChange = (e) => {
    setEmailInfo({
      ...emailInfo,
      [e.target.name]: e.target.value
    });
  };

  const handlePasswordChange = (e) => {
    setPasswordInfo({
      ...passwordInfo,
      [e.target.name]: e.target.value
    });
  };

  const handlePersonalInfoSubmit = (e) => {
    e.preventDefault();
    console.log('Personal Info:', personalInfo);
    // Add your submit logic here
  };

  const handleEmailSubmit = (e) => {
    e.preventDefault();
    console.log('Email:', emailInfo);
    // Add your submit logic here
  };

  const handlePasswordSubmit = (e) => {
    e.preventDefault();
    if (passwordInfo.newPassword !== passwordInfo.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }
    console.log('Password update submitted');
    // Add your submit logic here
  };

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
            <span className="dark:text-white text-lg font-semibold">User Settings</span>
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


     <main className="flex-1 container mx-auto px-4 py-12">
        <div className="h-8"></div>
        <div className="flex flex-col gap-12">
          {/* Personal Info Form */}
		<Card className="p-8 space-y-2 dark:bg-slate-800 dark:border-slate-700">
		  <div className="h-4"></div>
		  <h2 className="text-2xl dark:text-white">Update Personal Info</h2>
		  <form className="space-y-6" onSubmit={handlePersonalInfoSubmit}>
		    <div>
		      <Label htmlFor="firstName">First Name</Label>
		      <Input name="firstName" value={personalInfo.firstName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="middleName">Middle Name</Label>
		      <Input name="middleName" value={personalInfo.middleName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="lastName">Last Name</Label>
		      <Input name="lastName" value={personalInfo.lastName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="organization">Organization</Label>
		      <Input name="organization" value={personalInfo.organization} onChange={handlePersonalInfoChange} />
		    </div>
		    <Button type="submit">Save Personal Info</Button>
		    <div className="h-4"></div>
		  </form>
		</Card>

          {/* Email Update Form */}
	<Card className="p-8 space-y-2 dark:bg-slate-800 dark:border-slate-700">
	  <div className="h-4"></div>
	  <h2 className="text-2xl dark:text-white">Update Email</h2>
	  <form className="space-y-6" onSubmit={handleEmailSubmit}>
	    <div>
	      <Label htmlFor="email">Email</Label>
	      <Input name="email" type="email" value={emailInfo.email} onChange={handleEmailChange} />
	    </div>
	    <Button type="submit">Save Email</Button>
	    <div className="h-4"></div>
	  </form>
	</Card>

          {/* Password Update Form */}
	<Card className="p-8 space-y-2 dark:bg-slate-800 dark:border-slate-700">
	  <div className="h-4"></div>
	  <h2 className="text-2xl dark:text-white">Update Password</h2>
	  <form className="space-y-6" onSubmit={handlePasswordSubmit}>
	    <div>
	      <Label htmlFor="oldPassword">Old Password</Label>
	      <Input name="oldPassword" type="password" value={passwordInfo.oldPassword} onChange={handlePasswordChange} />
	    </div>
	    <div>
	      <Label htmlFor="newPassword">New Password</Label>
	      <Input name="newPassword" type="password" value={passwordInfo.newPassword} onChange={handlePasswordChange} />
	    </div>
	    <div>
	      <Label htmlFor="confirmPassword">Confirm New Password</Label>
	      <Input name="confirmPassword" type="password" value={passwordInfo.confirmPassword} onChange={handlePasswordChange} />
	    </div>
	    <Button type="submit">Save Password</Button>
	    <div className="h-4"></div>
	  </form>
	</Card>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-slate-50 dark:bg-slate-900/50 dark:border-slate-800 py-8">
        <div className="container mx-auto px-4 text-center text-slate-600 dark:text-slate-400">
          <p>&copy; 2025 GrantGuru. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
