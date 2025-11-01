"""

    File: fetch_grant_details.py

    Version: 1 November 2025

    Author: Abdullahi Abdullahi
    
    Description:
        Fetches detailed grant information from Grants.gov API.
        Based upon a json file generated from grant_id_search.py

    Usage:
         Example:
         python3  -m src.scraper.fetch_grant_details <args>
         **see src.utils.parse_scraper_args.py to see appropiate args**

"""

import requests
import json
import time
from typing import Optional


from src.utils.grant_id_search import get_grant_ids, FundingCategory, OpportunityStatus
from src.utils.logging_utils import log_warning, log_info, log_error, log_debug, log_default
from src.utils.parse_scraper_args import parse_args


def fetch_details(grant_id: str, verbose: bool = False) -> Optional[dict]:
    """
    Fetches the full details for a single grant ID from the fetchOpportunity API.
    
    Args:
        grant_id: The opportunity ID to fetch.
        verbose: If True, print detailed error information.

    Returns:
        A dictionary containing the full grant details, or None if an error occurs.
    """
    # The API endpoint for fetching details
    url = "https://api.grants.gov/v1/api/fetchOpportunity"
 
    headers = {
        "User-Agent": "Python Grant Fetcher",
        "Content-Type": "application/json",
    }
 
    # The payload requires the opportunity ID
    payload = json.dumps({"opportunityId": grant_id})

    try:
        response = requests.post(url, headers=headers, data=payload, timeout=10)
 
        # Check for HTTP errors (e.g., 404, 500)
        response.raise_for_status()
 
        # Check if response has content
        if not response.text or response.text.strip() == "":
            log_warning(f"Empty response for ID {grant_id}")
            return None
 
        if verbose:
            log_debug(f"  Response status: {response.status_code}")
            log_debug(f"  Response length: {len(response.text)} characters")
 
        response_json = response.json()
 
        # Return the entire data object for complete grant details
        data = response_json.get('data', {})

        if data:
            # Add the ID to the data for reference
            data['id'] = grant_id
            return data
        else:
            log_warning(f"No data found for ID {grant_id}")
            if verbose:
                log_debug(f"Full response: {response_json}")
            return None

    except requests.HTTPError as e:
        log_error(f"  HTTP Error for ID {grant_id}: {e}")
        if verbose and hasattr(e.response, 'text'):
            log_error(f"  Response text: {e.response.text[:200]}")
        return None
    except requests.RequestException as e:
        log_error(f"  Request error for ID {grant_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        log_error(f"  JSON decode error for ID {grant_id}: {e}")
        if verbose:
            log_error(f"  Response text: {response.text[:200]}")
        return None


def main():
    """
    Main function to search for grant IDs, fetch their details, and save to a JSON file.
    """
 
    args = parse_args()

    # Search for grant IDs using grant_id_search module
    log_info("Searching for grants...")
    try:
        grant_ids = get_grant_ids(
            funding_categories=args.categories,
            keywords=args.keywords,
            statuses=args.statuses
        )
    except Exception as e:
        log_error(f"Error searching for grants: {e}")
        return

    if not grant_ids:
        log_warning("No grants found matching the search criteria.")
        return

    # Determine how many grants to fetch
    num_to_fetch = args.num if args.num is not None else len(grant_ids)
    ids_to_fetch = grant_ids[:num_to_fetch]
 
    log_info(f"Found {len(grant_ids)} IDs. Fetching details for {len(ids_to_fetch)} grants...")

    fetched_details = []
    failed_ids = []

    for i, grant_id in enumerate(ids_to_fetch, 1):
        log_info(f"\n[{i}/{len(ids_to_fetch)}] Fetching details for ID: {grant_id}")
        details = fetch_details(grant_id, verbose=args.verbose)
        
        if details:
            # Display basic info
            title = details.get('opportunityTitle', 'N/A')
            synopsis = details.get('synopsis', {})
            agency = synopsis.get('agencyName', 'N/A')
            
            log_default(f"  Title: {title}")
            log_default(f"  Agency: {agency}")
            fetched_details.append(details)
        else:
            failed_ids.append(grant_id)
        
        # Add delay to avoid rate limiting
        if i < len(ids_to_fetch):
            time.sleep(args.delay)

    # Save all details to a JSON file
    output_data = {
        "metadata": {
            "total_grants_fetched": len(fetched_details),
            "total_grants_failed": len(failed_ids),
            "search_criteria": {
                "categories": args.categories,
                "keywords": args.keywords,
                "statuses": args.statuses
            },
            "total_ids_found": len(grant_ids),
            "failed_ids": failed_ids
        },
        "grants": fetched_details
    }
    
    try:
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        log_info(f"Successfully fetched and saved details for {len(fetched_details)} grants.")
        if failed_ids:
            log_warning(f"Failed to fetch {len(failed_ids)} grants (IDs saved in metadata).")
        log_info(f"Output saved to: {args.output}")
    except IOError as e:
        log_error(f"Error: Could not write to output file {args.output}: {e}")


if __name__ == "__main__":
    main()
