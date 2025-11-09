"""

    File: dates_parser.py

    Version: 1 November 2025

    Author: Colby Wirth
 
    Description:
        - Utility functions for parsing the dates in a dirty grant scrapped from Grants.gov
        - Generated with the help of AI tools

    Usage:
        there are two main helpers called by src.scraper.clean_scrapes.py:
            get_dates() attempts to clean dates - looking at two different points in the dirty grant dictionary
            to_non_negative_int() attempts to convert any integer to an non-negative int

"""



from datetime import datetime
from typing import Optional, Dict, Any

def _parse_human_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse human-readable date like 'Nov 17, 2025 12:00:00 AM EST'."""
    if not date_str:
        return None
    try:
        parts = date_str.split()
        # Remove timezone if present
        date_clean = " ".join(parts[:-1]) if len(parts) >= 6 else date_str
        dt = datetime.strptime(date_clean, "%b %d, %Y %I:%M:%S %p")
        return dt
    except Exception:
        return None

def _parse_backup_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse backup date string like '2025-11-17-00-00-00'."""
    if not date_str:
        return None
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d-%H-%M-%S")
        return dt
    except Exception:
        return None

def get_dates(dirty_grant: Dict) -> Dict[str, Optional[str]]:
    """
    main logic to get dates - used in the clean_scrapes.py

    Extract dates from a grant dictionary.
    Returns a dictionary suitable for MySQL DATETIME columns.
    """
    synopsis = dirty_grant.get("synopsis", {})
    dates: Dict[str, Optional[str]] = {}

    # Response date: primary then backup
    response_date = _parse_human_date(synopsis.get("responseDate")) \
                    or _parse_backup_date(synopsis.get("responseDateStr"))

    posting_date = _parse_human_date(synopsis.get("postingDate")) \
                   or _parse_backup_date(synopsis.get("postingDateStr"))

    archive_date = _parse_human_date(synopsis.get("archiveDate")) \
                   or _parse_backup_date(synopsis.get("archiveDateStr"))

    last_updated_date = _parse_human_date(synopsis.get("lastUpdatedDate"))

    # Format for MySQL DATETIME or None
    dates["response_date"] = response_date.strftime("%Y-%m-%d %H:%M:%S") if response_date else None
    dates["posting_date"] = posting_date.strftime("%Y-%m-%d %H:%M:%S") if posting_date else None
    dates["archive_date"] = archive_date.strftime("%Y-%m-%d %H:%M:%S") if archive_date else None
    dates["last_updated_date"] = last_updated_date.strftime("%Y-%m-%d %H:%M:%S") if last_updated_date else None

    return dates


def to_non_negative_int(value: Any) -> Optional[int]:
    """
    helper function for clean_a_grant
    """
    try:
        num = int(value)
        return num if num >= 0 else None
    except (TypeError, ValueError):
        return None
