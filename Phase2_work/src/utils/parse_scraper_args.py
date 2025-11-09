"""

File: parse_scraper_args.py

Version: 1 November 2025

Author: Colby Wirth

Description:
    Helper module for argument parsing for make_scrapes.py

"""

import argparse

def parse_args(args=None):
    """
    Parse command-line arguments for make_scrapes.py.
    Returns an argparse.Namespace object.
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
        default="runtime/grant_details.json",
        help="Output JSON file for grant details (default: runtime/grant_details.json).",
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
  
    return parser.parse_args(args)
