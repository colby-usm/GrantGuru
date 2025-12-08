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
from src.utils.logging_utils import log_info, log_error, log_warning


def daily_operations():

    log_info("Starting daily DB cleaning...")

    deletion_script() 

    log_info("Starting daily scraper scheduler...")
    dirty_grant_dict = scraper_script([
        "--statuses", "posted",  # we can add other filters here
        "-n", "20"  # Limit to 20 grants for testing
    ])

    # scraper_script returns None when no IDs are found or an error occurred
    if not dirty_grant_dict:
        log_warning("Scraper returned no data; skipping cleaning and insertion.")
        return

    cleaned_grants: list = cleaner_script(dirty_grant_dict)
    insert_script(cleaned_grants)
    

if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser(description="Daily grants maintenance scheduler")
    parser.add_argument("--once", action="store_true", help="Run the maintenance once and exit")
    parser.add_argument("--at", type=str, default="00:00", help="Time to run daily in HH:MM (24h) format, default 00:00")
    args = parser.parse_args()

    if args.once:
        try:
            daily_operations()
        except Exception as e:
            log_error(f"Error during one-time daily operations: {e}")
        raise SystemExit(0)

    # Schedule daily run at the specified time (local system time)
    run_time = args.at
    schedule.every().day.at(run_time).do(daily_operations)
    log_info(f"Scheduled daily maintenance at {run_time} local time. Running schedule loop...")

    try:
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        log_info("Daily maintenance scheduler stopped by user.")

