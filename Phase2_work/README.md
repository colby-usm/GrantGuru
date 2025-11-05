## Members:

Abdullahi Abdullahi: abdullahi204

Mathieu Poulin: MPoulin42

James Tedder: James-Tedder

Colby Wirth: colby-usm


# Project Tasks and Coding Style Standards

## Coding Style Standards
- Adhere to [PEP 8](https://peps.python.org/pep-0008) guidelines for Python code formatting and style.

## ~~Repository Setup~~
- **Tasks**:
  -  All team members have copied the contents of the main branch to their own branch.
  - Confirm that each team member has cloned their respective branch from the GitHub repository.
- **Assigned**: Team
- **Deadline**: October 26, 2025

## Team Member Contributions
- **Tasks**:
  - Record your progress throughout Phase 2  
  - Each member is responsible for recording their own tasks, and submitting them to the team leader. 
- **Assigned**: Entire Team
- **Deadline**: November 14, 2025

## Data Scraping

### ~~Grants.gov Scraper~~
- **Tasks**:
  - Develop a script using the **Beautiful Soup** library to perform multiple searches in the Grants.gov database based on a user’s research files.
    - Assume a list of strings is passed as a parameter.
    - Example function header: `def db_scraper(fields: List)`
- **Assigned**: Mathieu, Abdullahi
- **Deadline**: October 30, 2025

### ~~Grant Cleaner~~
- **Tasks**:
  - Implement a grant cleaner to parse and normalize data from the scraper function.
    - Note: Only the Grants.gov database is scraped in this project version, so cleaning should be straightforward.
- **Assigned**: James, Colby
- **Deadline**: November 2, 2025

## Database Development

### Database Schema Creation
~~- **User Entity Script**:~~
  - **Assigned**: Colby
  - **Deadline**: October 30, 2025
~~- **Application Entity Script**:~~
  - **Assigned**: Abdullahi
  - **Deadline**: November 2, 2025
~~- **Deadline Entity Script**:~~
  - **Assigned**: Mathieu
  - **Deadline**: November 2, 2025
~~- **Document Entity Script**:~~
  - **Assigned**: Mathieu
  - **Deadline**: November 2, 2025
~~- **Grant Entity Script**:~~
  - **Assigned**: James
  - **Deadline**: October 30, 2025
~~- **Dispatcher Script**:~~
  - Create a script to run all build scripts in sequence.
  - **Assigned**: Colby
  - **Deadline**: November 5, 2025
- **Index Creation**:
  - **Assigned**: Mathieu
  - **Deadline**: November 5, 2025

## System Functionalities
- **Periodic Scraper Timer**:
  - Implement a timer to spawn periodic scraping tasks.  This is hardcoded at 3 days in the current version - this is subject to change.
  - **Assigned**: Colby
  - **Deadline**: November 8, 2025
- **Daily Deletion Timer**:
  - Implement a timer to spawn daily deletion tasks.
  - **Assigned**: James
  - **Deadline**: November 5, 2025
- **User-Triggered Scraping**:
  - Create a trigger for user-initiated scraping, defaulting to the user’s `research_field` attribute for keywords.
  - **Assigned**: Abdullahi
  - **Deadline**: November 5, 2025
- **Role-Based Permissions (RBP) Infrastructure**:
  - Develop infrastructure for role-based permissions, including:
    - Administrator view
    - User view
  - **Assigned**: Colby
  - **Deadline**: November 8, 2025

## CRUD Operations
- **Overview**:
  - Each entity will have a dedicated Python script to trigger SQL logic (e.g., `user_crud.py`, `application_crud.py`).
  - All SQL logic will reside in a single file (e.g., `db_operations.mysql`).

### User Entity CRUD
- **Tasks**:
  - Create a script to generate sample data.
  - Implement Create, Read, Update, Delete operations.
  - Include authorization via email.
- **Assigned**: Colby
- **Deadline**: November 11, 2025

### Application Entity CRUD
- **Tasks**:
  - Create a script to generate sample data.
  - Implement Create, Read, Update, Delete operations.
- **Assigned**: Abdullahi
- **Deadline**: November 8, 2025

### Document Entity CRUD
- **Tasks**:
  - Create a script to generate sample data.
  - Implement Create, Read, Update, Delete operations.
- **Assigned**: Mathieu
- **Deadline**: November 8, 2025

### Internal Deadlines Entity CRUD
- **Tasks**:
  - Create a script to generate sample data.
  - Implement Create, Read, Update, Delete operations.
- **Assigned**: Mathieu
- **Deadline**: November 8, 2025

### Grant Entity CRUD
- **Tasks**:
  - Create a script for sample data.
  - Implement Create, Read, Update, Delete operations.
- **Assigned**: James
- **Deadline**: November 8, 2025

## Query Optimization Analysis
- **Tasks**:
  - Analyze and present before/after query performance results for at least two queries.
- **Assigned**: James, Abdullahi, Mathieu
- **Deadline**: November 11, 2025

## Video Presentation
- **Tasks**:
  - Record a project demonstration video.
- **Assigned**: Entire Team
- **Deadline**: November 14, 2025



