# GrantGuru User Manual - Applications Section
Abdullahi Abdullahi: abdullahi204

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Managing Applications](#managing-applications)
4. [Working with Tasks & Deadlines](#working-with-tasks--deadlines)
5. [Document Management](#document-management)
6. [Application Status Tracking](#application-status-tracking)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

The GrantGuru Applications section is your central hub for managing grant applications throughout their entire lifecycle. From creating initial applications to tracking deadlines, uploading documents, and monitoring submission status, this comprehensive interface helps you stay organized and meet critical grant deadlines.

### Key Features
- Create and manage grant applications
- Track submission status and application state
- Set internal deadlines and task reminders
- Upload and organize supporting documents
- Monitor application progress at a glance

---

## Getting Started

### Accessing the Applications Section

1. **Login** to your GrantGuru account at `http://localhost:5173/`
2. From the homepage, click **"My Applications"** in the navigation menu
3. You'll see your Applications Dashboard

### Applications Dashboard Overview

The dashboard displays:
- **Your Applications List:** All your grant applications in a searchable table
- **Create Application Button:** Start a new grant application
- **Search Bar:** Filter applications by ID, grant, status, or date
- **Navigation Menu:** Quick access to Home, User Settings, and Logout

---

## Managing Applications

### Creating a New Application

1. Click the **"+ Create Application"** button (top right of the dashboard)
2. A modal window will appear with available grants
3. Select a grant from the dropdown menu
4. Click **"Create"** to initialize your application
5. The new application appears in your list with "pending" status

**Note:** You cannot create duplicate applications for the same grant. The system prevents this automatically.

### Viewing Application Details

1. Navigate to your applications list
2. Click on any application row to view details
3. The application detail page shows:
   - Grant information (title, provider, deadlines)
   - Current submission status
   - Application status
   - Internal deadline
   - Notes section
   - Associated tasks
   - Uploaded documents

### Editing Application Information

From the application detail page, you can update:

**Status** (Application State)
- Options: `pending`, `approved`, `rejected`, `withdrawn`
- Use the status dropdown and click "Update Status"

**Internal Deadline**
- Set your own deadline (independent of grant deadline)
- Useful for institutional review deadlines
- Update using the date picker

**Notes**
- Add personal notes, reminders, or details
- Free-text field for any application-specific information
- Automatically saved when updated

**Submission Status**
- Toggle between `started` and `submitted`
- Tracks whether you've officially submitted to the grant provider
- Cannot be reversed once marked as submitted

### Searching Applications

Use the search bar to filter applications by:
- Application ID
- Grant ID
- Status (pending, approved, rejected, withdrawn)
- Application date

**Example Searches:**
- "pending" - Shows all pending applications
- "2024-03-15" - Shows applications from March 15, 2024
- Grant UUID - Shows specific grant application

### Deleting Applications

1. Navigate to the application detail page
2. Click the **"Delete Application"** button
3. Confirm the deletion
4. **Warning:** This action is permanent and will delete all associated documents and tasks

---

## Working with Tasks & Deadlines

### What are Internal Deadlines?

Internal deadlines (also called "Application Tasks") are personal milestones and to-do items you set for each application. They help you break down the application process into manageable steps.

### Creating a Task

1. Open an application detail page
2. Scroll to the **"Tasks"** section
3. Click **"Add Task"** or **"Create New Task"**
4. Fill in the task form:
   - **Task Name:** Brief description (e.g., "Submit budget proposal")
   - **Deadline Date:** When this task should be completed
   - **Description:** Optional detailed notes about the task
5. Click **"Save"** or **"Create"**

### Viewing Tasks

Tasks are displayed in the application detail view:
- Ordered by deadline date (nearest deadline first)
- Shows task name, deadline, completion status
- Color-coded indicators for overdue tasks

### Completing Tasks

1. Find the task in the tasks list
2. Click the checkbox or **"Mark Complete"** button
3. The task is marked as completed with a timestamp
4. Completed tasks can be toggled back to incomplete if needed

### Editing Tasks

1. Click the task or the **"Edit"** button
2. Modify the task name, deadline, or description
3. Click **"Save"** to update

### Deleting Tasks

1. Click the **"Delete"** button next to the task
2. Confirm the deletion
3. The task is permanently removed

### Task Best Practices

- **Break down large applications** into smaller tasks
- **Set realistic deadlines** with buffer time
- **Include all steps:** draft writing, review, document gathering, submission
- **Use descriptions** for detailed notes or checklists
- **Review tasks weekly** to stay on track

---

## Document Management

### Uploading Documents

1. Navigate to the application detail page
2. Find the **"Documents"** section
3. Click **"Upload Document"** or **"Add Document"**
4. Select a file from your computer
5. The document is uploaded and appears in the documents list

**Supported File Types:**
- PDF (.pdf)
- Word Documents (.doc, .docx)
- Excel Spreadsheets (.xls, .xlsx)
- Images (.jpg, .png)
- Text files (.txt)

**File Size Limit:** Check with your system administrator for maximum file size (typically 10-50 MB)

### Viewing Documents

Documents are listed in the application detail view:
- Ordered by upload date (most recent first)
- Shows: Document name, file type, size, upload date
- Click the document name or **"View"** button to preview

### Downloading Documents

1. Find the document in the documents list
2. Click the **"Download"** button or download icon
3. The file downloads to your default downloads folder

### Deleting Documents

1. Click the **"Delete"** button next to the document
2. Confirm the deletion
3. **Warning:** This action is permanent and cannot be undone

### Document Organization Tips

- **Use descriptive filenames** before uploading (e.g., "Budget_2024_v2.pdf")
- **Upload all versions** for your records
- **Keep a local backup** of critical documents
- **Upload early** to avoid last-minute technical issues

---

## Application Status Tracking

### Understanding Application States

**Submission Status** (Process State)
- `started` - Application is in progress, not yet submitted
- `submitted` - Application has been submitted to grant provider

**Application Status** (Outcome State)
- `pending` - Awaiting decision from grant provider
- `approved` - Application has been approved/funded
- `rejected` - Application was not approved
- `withdrawn` - You withdrew the application

### Typical Application Workflow

1. **Create Application** → Status: `pending`, Submission: `started`
2. **Work on Application** → Add tasks, upload documents
3. **Complete Tasks** → Mark internal deadlines complete
4. **Submit Application** → Change submission status to `submitted`
5. **Await Decision** → Status remains `pending`
6. **Receive Decision** → Update status to `approved` or `rejected`

### Tracking Multiple Applications

Use the applications list to:
- **Sort by date** to see newest applications
- **Filter by status** to focus on pending submissions
- **Search by grant** to find specific opportunities
- **Monitor submission status** to see what's in progress

---

## Tips & Best Practices

### Application Management
- **Start early:** Create applications well before deadlines
- **Set internal deadlines 1-2 weeks before official deadline** for buffer time
- **Use the notes field** for grant-specific requirements or contact information
- **Review weekly:** Check your applications dashboard at least once per week

### Task Management
- **Break down work:** Create tasks for each major section (budget, narrative, etc.)
- **Include review time:** Add tasks for peer review, institutional review
- **Buffer deadlines:** Set task deadlines a few days before you actually need them
- **Track external dependencies:** Note when you're waiting on letters of recommendation

### Document Management
- **Upload as you go:** Don't wait until the last minute
- **Version control:** Include version numbers in filenames (v1, v2, final)
- **Organize by category:** Group similar documents (budgets, CVs, letters)
- **Test downloads:** Verify files are accessible before the deadline

### Staying Organized
- **Use consistent naming:** Develop a naming convention for documents
- **Regular cleanup:** Archive or delete old draft versions
- **Calendar integration:** Export deadlines to your calendar app
- **Collaboration:** Share grant IDs with team members if coordinating

---

## Troubleshooting

### Cannot Create Application

**Problem:** "Create Application" button doesn't work or shows error

**Solutions:**
1. Verify you're logged in (check for user ID in navigation)
2. Check if you already have an application for that grant (no duplicates allowed)
3. Ensure the grant is still active and accepting applications
4. Refresh the page and try again
5. Check browser console for errors (F12 → Console tab)

### Application Not Appearing

**Problem:** Created application doesn't show in list

**Solutions:**
1. Refresh the applications page (F5)
2. Clear your search filters
3. Check if you're logged in with the correct account
4. Try logging out and back in

### Cannot Upload Document

**Problem:** Document upload fails or shows error

**Solutions:**
1. Check file size (must be under maximum limit)
2. Verify file type is supported
3. Ensure stable internet connection
4. Try a different file format (e.g., convert to PDF)
5. Check available disk space on server

### Document Won't Download

**Problem:** Downloaded file is corrupted or won't open

**Solutions:**
1. Try downloading again
2. Check file extension matches file type
3. Use a different browser
4. Verify the file was uploaded correctly (check file size)

### Tasks Not Saving

**Problem:** Task changes don't persist after saving

**Solutions:**
1. Ensure all required fields are filled
2. Check date format is valid
3. Verify internet connection
4. Try refreshing the page
5. Check browser console for error messages

### Deadline Notifications Not Working

**Problem:** Not receiving reminders about upcoming deadlines

**Note:** Email notifications may not be implemented yet. Current system requires manual checking of the applications dashboard for upcoming deadlines.

### General Issues

**Clear Browser Cache:**
1. Press `Ctrl+Shift+Delete` (Windows/Linux) or `Cmd+Shift+Delete` (Mac)
2. Select "Cached images and files"
3. Clear cache
4. Refresh the page

**Try Different Browser:**
- Chrome, Firefox, Edge, or Safari
- Ensure browser is up to date

**Contact Support:**
If issues persist, contact your system administrator with:
- Description of the problem
- Steps to reproduce
- Browser and version
- Any error messages
- Screenshots if applicable

---

## Quick Reference Guide

### Common Actions

| Action | Location | Steps |
|--------|----------|-------|
| Create Application | Applications Dashboard | Click "+ Create Application" → Select Grant → Create |
| View Details | Applications List | Click on application row |
| Update Status | Application Detail | Select status → Click "Update Status" |
| Add Task | Application Detail | Tasks section → "Add Task" → Fill form → Save |
| Upload Document | Application Detail | Documents section → "Upload" → Select file |
| Delete Application | Application Detail | "Delete Application" button → Confirm |
| Search Applications | Applications Dashboard | Type in search bar → Results filter automatically |
| Mark Task Complete | Application Detail | Tasks section → Check checkbox or "Mark Complete" |

### Keyboard Shortcuts

- `Ctrl+F` or `Cmd+F` - Search on page
- `F5` - Refresh page
- `Esc` - Close modal windows
- `Tab` - Navigate between form fields

---

## Glossary

- **Application:** Your submission for a specific grant opportunity
- **Grant:** Funding opportunity from a provider
- **Submission Status:** Whether your application is in progress or submitted
- **Application Status:** The decision state (pending, approved, rejected)
- **Internal Deadline:** Personal deadline you set for tasks or milestones
- **Task:** A to-do item or milestone within an application
- **Document:** Files uploaded and associated with an application
- **UUID:** Universal Unique Identifier - the ID format used for applications and grants

---

