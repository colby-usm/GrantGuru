# Project Tasks and Coding Style Standards

## Coding Style Standards
- Follow [PEP 8](https://peps.python.org/pep-0008) for Python code formatting and style.


## Potential tree hiearchy:



### Repository Setup (Completed by Oct 26)
- Ensure everyone has copied the contents of main branch into their own
- Ensure everyone has cloned THEIR branch of GitHub repository.

## Scraping

### Grants.gov Scraper
- 1. Use **Beautiful Soup** library for scraping. Mathieu and Abdullahi (Deadline: October 30th) 
- Create a script to perform multiple searches in Grants.gov database based on a user’s research files.
  - For now, assume a list of strings is passed as a parameter.
  - Function header example: `def db_scraper(fields: List)`
- Implement a **grant normalizer** to parse and normalize data from the scraper function. James and Colby (Deadline Nov 2nd)
  - Note that only one database (Grants.gov) is being scraped in this verison of the project - normalization should be a simple task.


## DB 

### Database Schema Creation
- Script for User Entity Colby (Deadline: October 30th)
- Script for Application Entity Abdullahi (Deadline Nov 2nd)
- Script for Deadline Entity Mathieu (Deadline Nov 2nd)
- Script for Document Entity Mathieu (Deadline Nov 2nd)
- Script for Grant Entity James (Deadline: October 30th)
- Dispatcher script to run all build scripts in sequence Colby (Deadline: Nov 5th)
- Index Creation Mathieu (Deadline: November 5th)
- 

## System Functionalities
  - 1. Timer that spawns periodic scraper Colby (Deadline: November 8)
  - 2. Timer that spawns daily deletion James (Deadline: November 5)
  - 3. Trigger for User spawned scraping (with keywords defaulting to their own research_field attr) Abdullahi (November 5)
  - 4. Infrastructure for Role-Based Permissions (RBP) - some python scripts? Colby (Deadline: November 8)
      - Administrator view.
      - User view.



### CRUD Operations
- Each of these will have their own Python script that triggers the SQL logic (e.g. user_crud.py, application_crud.py)
- The SQL logic is all under 1 file (e.g. db_operations.mysql)

- **User Entity CRUD**:
  - Add a script for sample data
  - Implement Create, Read, Update, Delete operations. Colby (Deadline November 11)
  - Consider authorization via email.
    
- **Application Entity CRUD**: )
  - Add a script for sample data
  - Implement Create, Read, Update, Delete operations. Abdullahi (Deadline November 8)
    
- **Document Entity CRUD**: Mathieu (Deadline: November 8)
  - Add a script for sample data
  - Implement Create, Read, Update, Delete operations.
    
- **Internal Deadlines Entity CRUD**: Mathieu: (Deadline: November 8)
  - Add a script for sample data
  - Implement Create, Read, Update, Delete operations.
 
- **Grant Entity CRUD**: James: (Deadline: November 8)
  - Add a script for sample data
  - Implement Create, Read, Update, Delete operations.

## Query Optimization Analysis
  - Show before/after query performance results for at least two queries. James, Abdullahi, Mathieu (Deadline: November 11)
    

## Record Video (Everybody) (Deadline: November 14)
