"""

    File: clean_scrapes.py

    Version: 1 November 2025

    Author: Colby Wirth
    
    Description:
        use the clean_a_grant function to clean a single grant (put it in a format normalized for the DB)

    Usage:
        pass a SINGLE dictionary for an uncleaned grant to clean_a_grant() to clean the grant and normalize it for the DB
"""

import json
from typing import Dict, Any
from src.utils.grant_cleaner_helpers import get_dates, to_non_negative_int
from src.utils.logging_utils import log_debug, log_default, log_info, log_warning


def clean_a_grant(dirty_grant: Dict[str, Any]) -> Dict[str, Any]:
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


def main():

    log_debug("Running test script for clean_scrapes.py")

    with open("runtime/grant_details_1.json", "r") as f:
        data: Dict[str, Any] = json.load(f)

    grants = data.get("grants", [])
    if not grants:
        log_warning("No grants found.")
        return

    # Process the first grant (or loop over all grants if needed)
    first_grant = grants[0]
    cleaned_grant = clean_a_grant(first_grant)

    log_info("Cleaned Grant:")
    log_default(json.dumps(cleaned_grant, indent=2))

if __name__ == "__main__":
    main()
