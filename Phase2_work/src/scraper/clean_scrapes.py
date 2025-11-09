"""

    File: clean_scrapes.py

    Version: 1 November 2025

    Author: Colby Wirth
    
    Description:
        use the clean_a_grant function to clean a single grant (put it in a format normalized for the DB)

    Usage:
        pass a SINGLE dictionary for an uncleaned grant to clean_a_grant() to clean the grant and normalize it for the DB

"""
from datetime import datetime
from typing import Dict, Any, Optional
from src.utils.grant_cleaner_helpers import get_dates, to_non_negative_int
from src.utils.logging_utils import log_debug, log_warning


def check_date_in_range(dirty_grant: dict, filter_on_date: int) -> bool:
    """
    Check if a grant's lastUpdatedDate falls within the last `filter_on_date` days.

    Args:
        dirty_grant: The raw grant dictionary.
        filter_on_date: Number of days. Only grants updated in the last `filter_on_date` days will return True.

    Returns:
        True if the grant's lastUpdatedDate is within the last `filter_on_date` days, False otherwise.
        If the lastUpdatedDate is missing or cannot be parsed, returns False.
    """
    last_updated_str = dirty_grant.get("synopsis", {}).get("lastUpdatedDate")


    log_warning(f"last updated string: {last_updated_str}")

    if last_updated_str:
        # Example format: 'Jun 02, 2010 10:53:01 AM EDT'
        try:
            last_updated_dt = datetime.strptime(last_updated_str[:-4], "%b %d, %Y %I:%M:%S %p")
            log_warning(f"last updated converted: {last_updated_dt }")
        except ValueError:
            # Could not parse date
            return False

        if filter_on_date is not None:
            today_ordinal = datetime.today().toordinal()
            last_updated_ordinal = last_updated_dt.toordinal()
            # Return True if within the last `filter_on_date` days
            return (today_ordinal - last_updated_ordinal) <= filter_on_date

    return False


def clean_a_grant(dirty_grant: Dict[str, Any], filter_on_date: Optional[int] = None) -> Optional[Dict[str, Any]]:

    if filter_on_date:
        if check_date_in_range(dirty_grant, filter_on_date) == False:
            return None

    g: Dict[str, Any] = {}

    g["grant_id"] = None

    # TODO - note that opportunity_number is not in the original ER diagram
    g["opportunity_number"] = dirty_grant.get("opportunityNumber", None)
    g["grant_title"] = dirty_grant.get("opportunityTitle", "No title")[:255]

    synopsis = dirty_grant.get("synopsis") or {}
    g["description"] = synopsis.get("synopsisDesc", "No description")[:18000]

    categories = dirty_grant.get("fundingActivityCategories", synopsis.get("fundingActivityCategories", []))
    if isinstance(categories, list) and categories:
        g["research_field"] = categories[0].get("description", "No Research Field")[:250]
    else:
        g["research_field"] = "No Research Field"

    g["expected_award_count"] = synopsis.get("numberOfAwards", None)
    g["eligibility"] = synopsis.get("applicantEligibilityDesc", None)
    g["provider"] = synopsis.get("agencyName", None)
    g["link_to_source"] = synopsis.get("fundingDescLinkUrl", "https://www.grants.gov/")[:2048]

    g["award_max_amount"] = to_non_negative_int(synopsis.get("awardCeiling"))
    g["award_min_amount"] = to_non_negative_int(synopsis.get("awardFloor"))
    g["program_funding"] = to_non_negative_int(synopsis.get("estimatedFunding"))

    # TODO Agency contact info as a nested dictionary - THIS NEEDS TO BE UPDATED IN THE ER DIAGRAM
    g["point_of_contact"] = {
        "phone": synopsis.get("agencyContactPhone"),
        "name": synopsis.get("agencyContactName"),
        "desc": synopsis.get("agencyContactDesc"),
        "email": synopsis.get("agencyContactEmail"),
        "email_desc": synopsis.get("agencyContactEmailDesc"),
    }

    g["dates"] = get_dates(dirty_grant)

    return g


def main(scrape_dict, filter_on_dates=None):

    #dirty_grant_list = args[0]["grants"]


    cleaned_grants = []
    dirty_grant_list = scrape_dict["grants"]

    for g in dirty_grant_list:
        log_debug(f"Cleaning a grant")
        cleaned_grant = clean_a_grant(g, filter_on_dates)
        if cleaned_grant is not None:
            cleaned_grants.append(cleaned_grant)


    return cleaned_grants


    #log_debug("Running test script for clean_scrapes.py")

    #with open("runtime/grant_details_1.json", "r") as f:
    #    data: Dict[str, Any] = json.load(f)

    #grants = data.get("grants", [])
    #if not grants:
    #    log_warning("No grants found.")
    #    return

    ## Process the first grant (or loop over all grants if needed)
    #first_grant = grants[0]
    #cleaned_grant = clean_a_grant(first_grant)

    #log_info("Cleaned Grant:")
    #log_default(json.dumps(cleaned_grant, indent=2))

#if __name__ == "__main__":
#    main()
