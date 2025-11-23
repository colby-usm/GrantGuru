// UserPage.tsx
import { useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

const API_BASE_URL = "http://127.0.0.1:5000";

export function UserPage() {
  // Form states
  const [personalInfo, setPersonalInfo] = useState({
    firstName: "",
    middleName: "",
    lastName: "",
    organization: "",
  });

  const [emailInfo, setEmailInfo] = useState({
    email: "",
  });

  const [passwordInfo, setPasswordInfo] = useState({
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  // Handlers
  const handlePersonalInfoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPersonalInfo({ ...personalInfo, [e.target.name]: e.target.value });
  };

  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEmailInfo({ ...emailInfo, [e.target.name]: e.target.value });
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPasswordInfo({ ...passwordInfo, [e.target.name]: e.target.value });
  };

  const handlePersonalInfoSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/user/update-personal`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(personalInfo),
      });
      const data = await res.json();
      if (!res.ok) alert("Update failed: " + data.error);
      else alert("Personal info updated!");
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE_URL}/user/update-email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(emailInfo),
      });
      const data = await res.json();
      if (!res.ok) alert("Email update failed: " + data.error);
      else alert("Email updated!");
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (passwordInfo.newPassword !== passwordInfo.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/user/update-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(passwordInfo),
      });
      const data = await res.json();
      if (!res.ok) alert("Password update failed: " + data.error);
      else alert("Password updated!");
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 py-16 px-4">
      <h1 className="text-4xl dark:text-white mb-12 text-center">User Settings</h1>
      <div className="max-w-3xl mx-auto space-y-12">
        
        {/* Personal Info Form */}
        <Card className="p-8 space-y-6 dark:bg-slate-800 dark:border-slate-700">
          <h2 className="text-2xl dark:text-white">Update Personal Info</h2>
          <form className="space-y-4" onSubmit={handlePersonalInfoSubmit}>
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
          </form>
        </Card>

        {/* Email Update Form */}
        <Card className="p-8 space-y-6 dark:bg-slate-800 dark:border-slate-700">
          <h2 className="text-2xl dark:text-white">Update Email</h2>
          <form className="space-y-4" onSubmit={handleEmailSubmit}>
            <div>
              <Label htmlFor="email">Email</Label>
              <Input name="email" type="email" value={emailInfo.email} onChange={handleEmailChange} />
            </div>
            <Button type="submit">Save Email</Button>
          </form>
        </Card>

        {/* Password Update Form */}
        <Card className="p-8 space-y-6 dark:bg-slate-800 dark:border-slate-700">
          <h2 className="text-2xl dark:text-white">Update Password</h2>
          <form className="space-y-4" onSubmit={handlePasswordSubmit}>
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
          </form>
        </Card>

      </div>
    </div>
  );
}
