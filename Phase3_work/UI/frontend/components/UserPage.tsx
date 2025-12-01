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
    fName: '',
    mName: '',
    lName: '',
    institution: ''
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


const handlePersonalInfoSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // Check for missing or empty required fields
  const requiredFields = ["fName", "mName", "lName", "institution"];
  const missingFields = requiredFields.filter(field => !personalInfo[field].trim());

  if (missingFields.length > 0) {
    alert(`Please fill out all fields`);
    return; // Stop submission
  }

  console.log("Personal Info:", personalInfo);

  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      alert("You are not logged in.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/user/personal-info", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
      body: JSON.stringify(personalInfo),
    });

    const contentType = response.headers.get("Content-Type") || "";
    let result: any = null;
    if (contentType.includes("application/json")) {
      result = await response.json();
    } else {
      result = { error: await response.text() };
    }

    if (response.ok) {
      alert(result.msg || "Personal info updated successfully");
    } else {
      alert(result.error || "Error updating personal info");
    }
  } catch (err) {
    console.error("Network error:", err);
    alert("Failed to update personal info");
  }
};

const handleEmailSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  const { email } = emailInfo;

  // Frontend validation
  if (!email) {
    alert("Email is required.");
    return;
  }

  // email regex validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert("Please enter a valid email address.");
    return;
  }

  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      alert("You are not logged in.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/user/email", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ email }),
    });

    const contentType = response.headers.get("Content-Type") || "";
    let result: any = null;
    if (contentType.includes("application/json")) {
      result = await response.json();
    } else {
      result = { error: await response.text() };
    }

    if (response.ok) {
      alert(result.msg || "Email updated successfully");
    } else {
      alert(result.error || "Error updating email");
    }
  } catch (err) {
    console.error("Network error:", err);
    alert("Failed to update email");
  }
};

const handlePasswordSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // Check that new password and confirm password match
  if (passwordInfo.newPassword !== passwordInfo.confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  if (passwordInfo.newPassword.length < 8) {
    alert('Password must be at least 8 characters long.');
    return;
  }

  try {
    const accessToken = sessionStorage.getItem("access_token");
    if (!accessToken) {
      alert("You are not logged in.");
      return;
    }

    const response = await fetch("http://127.0.0.1:5000/api/user/password", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        oldPassword: passwordInfo.oldPassword,
        newPassword: passwordInfo.newPassword
      }),
    });

    const contentType = response.headers.get("Content-Type") || "";
    let result: any = null;
    if (contentType.includes("application/json")) {
      result = await response.json();
    } else {
      result = { error: await response.text() };
    }

    if (response.ok) {
      alert(result.msg || "Password updated successfully");
      setPasswordInfo({ oldPassword: "", newPassword: "", confirmPassword: "" }); // clear fields
    } else {
      alert(result.error || "Error updating password");
    }
  } catch (err) {
    console.error("Network error:", err);
    alert("Failed to update password");
  }
};


  const handleLogout = () => {
    sessionStorage.removeItem('user_id');
    sessionStorage.removeItem('access_token');
    
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
		  <h2 className="text-2xl dark:text-white">&nbsp;Update Personal Info</h2>
		  <form className="space-y-6" onSubmit={handlePersonalInfoSubmit}>
		    <div>
		      <Label htmlFor="fName">&nbsp;First Name</Label>
		      <Input name="fName" value={personalInfo.fName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="mName">&nbsp;Middle Name</Label>
		      <Input name="mName" value={personalInfo.mName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="lName">&nbsp;Last Name</Label>
		      <Input name="lName" value={personalInfo.lName} onChange={handlePersonalInfoChange} />
		    </div>
		    <div>
		      <Label htmlFor="institution">&nbsp;Organization</Label>
		      <Input name="institution" value={personalInfo.institution} onChange={handlePersonalInfoChange} />
		    </div>
		    <Button type="submit">Save Personal Info</Button>
		    <div className="h-4"></div>
		  </form>
		</Card>

          {/* Email Update Form */}
	<Card className="p-8 space-y-2 dark:bg-slate-800 dark:border-slate-700">
	  <div className="h-4"></div>
	  <h2 className="text-2xl dark:text-white">&nbsp;Update Email</h2>
	  <form className="space-y-6" onSubmit={handleEmailSubmit}>
	    <div>
	      <Label htmlFor="email">&nbsp;Email</Label>
	      <Input name="email" type="email" value={emailInfo.email} onChange={handleEmailChange} />
	    </div>
	    <Button type="submit">Save Email</Button>
	    <div className="h-4"></div>
	  </form>
	</Card>

          {/* Password Update Form */}
	<Card className="p-8 space-y-2 dark:bg-slate-800 dark:border-slate-700">
	  <div className="h-4"></div>
	  <h2 className="text-2xl dark:text-white">&nbsp;Update Password</h2>
	  <form className="space-y-6" onSubmit={handlePasswordSubmit}>
	    <div>
	      <Label htmlFor="oldPassword">&nbsp;Old Password</Label>
	      <Input name="oldPassword" type="password" value={passwordInfo.oldPassword} onChange={handlePasswordChange} />
	    </div>
	    <div>
	      <Label htmlFor="newPassword">&nbsp;New Password</Label>
	      <Input name="newPassword" type="password" value={passwordInfo.newPassword} onChange={handlePasswordChange} />
	    </div>
	    <div>
	      <Label htmlFor="confirmPassword">&nbsp;Confirm New Password</Label>
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
