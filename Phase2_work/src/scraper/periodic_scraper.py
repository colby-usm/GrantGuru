'''
    File: periodic_scraper.py

    Version: 8 November 2025

    Author: Colby Wirth
    
    Description:
        Using the python schedule api to execute a full scrape of Grants.Gov every SCRAPE_PERIOD_DAYS days
        Note, the Grants.gov scraping APIs are poorly designed where we cannot query based on dates.  Therefore, to get all recent updates, we have to scrape the entire DB for "forecasted" and "posted" then we filter all grants on our side.

    Usage:
         Example:
         python3 -m src.scraper.periodic_scraper

'''
import schedule

from src.utils.logging_utils import log_info
from src.scraper.make_scrapes import main as scraper_script
from src.scraper.clean_scrapes import main as cleaner_script

SCRAPE_PERIOD_DAYS = 7

def periodic_scraper():
    """
    Core logic:
        - Scrape newly posted or forecasted grants
        - Clean and normalize them
        - Insert into the database
    """

    dirty_grant_dict = scraper_script([
        "--statuses", "forecasted", "posted"
    ])
    cleaned_grants = cleaner_script(dirty_grant_dict, filter_on_dates=SCRAPE_PERIOD_DAYS)

    #TODO: implement a helper function that calls the correct sql insertion logic for grant entities for every value in the cleaned_grants list
    #insert_grants(cleaned)
    #log_info(f"Periodic scrape complete. Inserted {len(cleaned)} grants.")
 

if __name__ == "__main__":
    schedule.every(SCRAPE_PERIOD_DAYS ).days.do(periodic_scraper)
    log_info("Starting periodic scraper scheduler...")
    while True:
        schedule.run_pending()

