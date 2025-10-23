# Project Tasks and Coding Style Standards

## Coding Style Standards
- Follow [PEP 8](https://peps.python.org/pep-0008) for Python code formatting and style.

## Tasks

### Repository Setup (Completed by Oct 26)
- Ensure everyone has copied the contents of main branch into their own
- Ensure everyone has cloned THEIR branch of GitHub repository.

### Grants.gov Scraper
- Use **Beautiful Soup** library for scraping.
- Create a script to perform multiple searches in Grants.gov database based on a user’s research files.
  - For now, assume a list of strings is passed as a parameter.
  - Function header example: `def db_scraper(fields: List)`
- Implement a **grant normalizer** to parse and normalize data from the scraper function.
  - Note that only one database (Grants.gov) is being scraped in this verison of the project - normalization should be a simple task.

### Database Schema Creation
- Write scripts to create the database schema from scratch (runs one time to initialize).
- Ensure constraints are enforced (e.g., Primary Key, NOT NULL).

### Periodic External DB (Grants.gov) Scraper
- Develop code for periodic scraping of Grants.gov.
- Details to be finalized:
  - Frequency of scraping.
  - Conditions for scraping.

### CRUD Operations
- **User Entity CRUD**:
  - Implement Create, Read, Update, Delete operations.
  - Consider authorization via email.
- **Application Entity CRUD**:
  - Implement Create, Read, Update, Delete operations.
- **Document Entity CRUD**:
  - Implement Create, Read, Update, Delete operations.
- **Internal Deadlines Entity CRUD**:
  - Implement Create, Read, Update, Delete operations.

### Notifications
- Create scripts for generating periodic notifications (details to be specified).

### Infrastructure for Role-Based Permissions (RBP)
- Develop infrastructure to support:
  - Administrator view.
  - User view.
