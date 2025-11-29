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
            1. Runs deletion_script() to remove unreferenced Grants that are past "archieved date" from the Database
            2. Runs scraper_script() function which scrapes all new grants from Grants.gv
            3. Runs cleaner_script() to filter and clean grants that have been posted in the last SCRAPE_PERIOD_DAYS
            4. Runs insert_script() to insert all new Grants to DB
'''

SCRAPE_PERIOD_DAYS = 365
from src.utils.logging_utils import log_info


def daily_operations():

    log_info("Starting daily DB cleaning...")

    deletion_script() 

    log_info("Starting daily scraper scheduler...")
    dirty_grant_dict = scraper_script([
        "--statuses", "forecasted", "posted" # we can add other filters here
        "-n", "100" # FOR TESTING ONLY

    ])

    cleaned_grants: list = cleaner_script(dirty_grant_dict, filter_on_dates=SCRAPE_PERIOD_DAYS)
    insert_script(cleaned_grants)
    

if __name__ == "__main__":
 

    schedule.every(SCRAPE_PERIOD_DAYS).days.do(daily_operations)
    while True:
        schedule.run_pending()

