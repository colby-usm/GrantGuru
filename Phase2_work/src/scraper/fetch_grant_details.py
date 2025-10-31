"""
Fetch detailed grant information from Grants.gov API.

This script searches for grants using the grant_id_search module and fetches
detailed information for each grant found.

Usage:
    python fetch_grant_details.py -c HEALTH -n 10
    python fetch_grant_details.py -k "climate change" -c ENVIRONMENT -v
"""
import requests
import json
import argparse
import time
from typing import List, Optional
from grant_id_search import get_grant_ids, FundingCategory, OpportunityStatus


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
            print(f"  Warning: Empty response for ID {grant_id}")
            return None
        
        if verbose:
            print(f"  Response status: {response.status_code}")
            print(f"  Response length: {len(response.text)} characters")
        
        response_json = response.json()
        
        # Return the entire data object for complete grant details
        data = response_json.get('data', {})
        
        if data:
            # Add the ID to the data for reference
            data['id'] = grant_id
            return data
        else:
            print(f"  Warning: No data found for ID {grant_id}")
            if verbose:
                print(f"  Full response: {response_json}")
            return None

    except requests.HTTPError as e:
        print(f"  HTTP Error for ID {grant_id}: {e}")
        if verbose and hasattr(e.response, 'text'):
            print(f"  Response text: {e.response.text[:200]}")
        return None
    except requests.RequestException as e:
        print(f"  Request error for ID {grant_id}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON decode error for ID {grant_id}: {e}")
        if verbose:
            print(f"  Response text: {response.text[:200]}")
        return None


def main():
    """
    Main function to search for grant IDs, fetch their details, and save to a JSON file.
    """
    parser = argparse.ArgumentParser(
        description="Search for grants and fetch their details from Grants.gov API."
    )
    parser.add_argument(
        "-c",
        "--categories",
        type=str,
        nargs="+",
        help="Funding categories (e.g., HL ED or HEALTH EDUCATION).",
    )
    parser.add_argument(
        "-k",
        "--keywords",
        type=str,
        help="Search keywords (e.g., 'climate change').",
    )
    parser.add_argument(
        "-s",
        "--statuses",
        type=str,
        nargs="+",
        default=["posted"],
        help="Opportunity statuses (e.g., posted closed archived forecasted). Default: posted",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="grant_details.json",
        help="Output JSON file for grant details (default: grant_details.json).",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=None,
        help="Number of grants to fetch details for (default: all grants).",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output for debugging.",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0.5,
        help="Delay between requests in seconds (default: 0.5).",
    )
    
    args = parser.parse_args()

    # Search for grant IDs using grant_id_search module
    print("Searching for grants...")
    try:
        grant_ids = get_grant_ids(
            funding_categories=args.categories,
            keywords=args.keywords,
            statuses=args.statuses
        )
    except Exception as e:
        print(f"Error searching for grants: {e}")
        return

    if not grant_ids:
        print("No grants found matching the search criteria.")
        return

    # Determine how many grants to fetch
    num_to_fetch = args.num if args.num is not None else len(grant_ids)
    ids_to_fetch = grant_ids[:num_to_fetch]
    
    print(f"Found {len(grant_ids)} IDs. Fetching details for {len(ids_to_fetch)} grants...")

    fetched_details = []
    failed_ids = []

    for i, grant_id in enumerate(ids_to_fetch, 1):
        print(f"\n[{i}/{len(ids_to_fetch)}] Fetching details for ID: {grant_id}")
        details = fetch_details(grant_id, verbose=args.verbose)
        
        if details:
            # Display basic info
            title = details.get('opportunityTitle', 'N/A')
            synopsis = details.get('synopsis', {})
            agency = synopsis.get('agencyName', 'N/A')
            
            print(f"  Title: {title}")
            print(f"  Agency: {agency}")
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
        print(f"\n---\nSuccessfully fetched and saved details for {len(fetched_details)} grants.")
        if failed_ids:
            print(f"Failed to fetch {len(failed_ids)} grants (IDs saved in metadata).")
        print(f"Output saved to: {args.output}")
    except IOError as e:
        print(f"\nError: Could not write to output file {args.output}: {e}")


if __name__ == "__main__":
    main()