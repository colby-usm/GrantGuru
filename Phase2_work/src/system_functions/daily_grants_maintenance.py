import schedule
from src.scraper.make_scrapes import main as scraper_script
from src.scraper.clean_scrapes import main as cleaner_script
from src.system_functions.delete_old_grants import main as deletion_script
from src.system_functions.insert_cleaned_grant import main as insert_script

'''
    File: daily_grants_maintenance.py
    Version: 14 November 2025
    Author: Colby Wirth and James Tedder

    Description:
        - Runs on daily intervals:
            1. Clean unreferenced Grants that are past "archieved date" from the Database
            2. Runs the daily_scraper() function which scrapes all new grants from Grants.gv
            3. Cleans the retrieved Grants
            4. Insert new Grants to DB
'''

SCRAPE_PERIOD_DAYS = 7
from src.utils.logging_utils import log_info


def daily_operations():

    # 1 James' deletion logic here
    log_info("Starting daily DB cleaning...")
    deletion_script()


    # 2 scraping logic

    log_info("Starting daily scraper scheduler...")
    dirty_grant_dict = scraper_script([
        "--statuses", "forecasted", "posted", "-n", "5"
    ])

    # 3 cleaning logic
    cleaned_grants: list = cleaner_script(dirty_grant_dict, filter_on_dates=100000)
    
    # James, cleaned_grants is a list of grants that contain the dictionary, use "opportunity_number" to get the UUID that Grants.gov genreates
    # print(cleaned_grants[1]) <- use this to see an example
    # 4 James' DB insertion logic here
    insert_script(cleaned_grants)
    

if __name__ == "__main__":
 

    schedule.every(SCRAPE_PERIOD_DAYS).days.do(daily_operations)
    while True:
        schedule.run_pending()

