import requests
from typing import Iterable, List, Optional, Union
from enum import Enum

SEARCH2_URL = "https://api.grants.gov/v1/api/search2"


class FundingCategory(Enum):
    """Grants.gov funding category codes."""
    AGRICULTURE = "AG"
    ARTS = "AR"
    BUSINESS_COMMERCE = "BC"
    COMMUNITY_DEVELOPMENT = "CD"
    CONSUMER_PROTECTION = "CP"
    DISASTER_PREVENTION = "DPR"
    EDUCATION = "ED"
    EMPLOYMENT_LABOR = "ELT"
    ENERGY = "EN"
    ENVIRONMENT = "ENV"
    FOOD_NUTRITION = "FN"
    HEALTH = "HL"
    HOUSING = "HO"
    HUMANITIES = "HU"
    INCOME_SECURITY = "IS"
    INFORMATION_STATISTICS = "ISS"
    LAW_JUSTICE = "LJL"
    NATURAL_RESOURCES = "NR"
    OPPORTUNITY_ZONE_BENEFITS = "OZ"
    REGIONAL_DEVELOPMENT = "RD"
    SCIENCE_TECHNOLOGY = "ST"
    SOCIAL_SERVICES = "ISS"
    TRANSPORTATION = "T"


class OpportunityStatus(Enum):
    """Grants.gov opportunity status types."""
    POSTED = "posted"
    CLOSED = "closed"
    ARCHIVED = "archived"
    FORECASTED = "forecasted"


def get_grant_ids(
    *,
    funding_categories: Optional[Iterable[Union[FundingCategory, str]]] = None,
    keywords: Optional[str] = None,
    statuses: Optional[Iterable[Union[OpportunityStatus, str]]] = None,
    page_size: int = 500,
    timeout: float = 30.0,
) -> List[str]:
    """
    Return every Grants.gov opportunity ID matching the search criteria.
    
    Args:
        funding_categories: Iterable of FundingCategory enums, category codes (e.g., ["HL", "ED"]),
                          or full names (e.g., ["HEALTH", "EDUCATION"]).
                          Will be converted to internal Grants.gov codes.
        keywords: Search keywords (space-separated string or single phrase)
        statuses: Optional status filter using OpportunityStatus enums or strings
                 (e.g., [OpportunityStatus.POSTED] or ["posted", "closed"])
        page_size: Number of results per page (default 500, max 1000)
        timeout: Request timeout in seconds (default 30.0)
    
    Returns:
        List of grant opportunity IDs
        
    Examples:
        >>> # Using enums (recommended)
        >>> get_grant_ids(funding_categories=[FundingCategory.HEALTH, FundingCategory.EDUCATION])
        >>> get_grant_ids(statuses=[OpportunityStatus.POSTED])
        
        >>> # Using strings (also supported)
        >>> get_grant_ids(funding_categories=["HL", "ED"])
        >>> get_grant_ids(funding_categories=["HEALTH", "EDUCATION"])
        
        >>> # Combined search
        >>> get_grant_ids(
        ...     keywords="climate change",
        ...     funding_categories=[FundingCategory.ENVIRONMENT],
        ...     statuses=[OpportunityStatus.POSTED]
        ... )
    """
    # Process funding categories - convert to codes
    category_filter = ""
    if funding_categories:
        processed_codes = []
        for cat in funding_categories:
            if isinstance(cat, FundingCategory):
                # It's an enum, use its value
                processed_codes.append(cat.value)
            elif isinstance(cat, str):
                cat_upper = cat.strip().upper()
                # Try to find matching enum by name
                try:
                    enum_member = FundingCategory[cat_upper]
                    processed_codes.append(enum_member.value)
                except KeyError:
                    # Assume it's already a code
                    processed_codes.append(cat_upper)
            else:
                raise TypeError(f"Invalid category type: {type(cat)}")
        category_filter = "|".join(processed_codes)
    
    # Process statuses
    status_filter = ""
    if statuses:
        processed_statuses = []
        for status in statuses:
            if isinstance(status, OpportunityStatus):
                processed_statuses.append(status.value)
            elif isinstance(status, str):
                processed_statuses.append(status.lower().strip())
            else:
                raise TypeError(f"Invalid status type: {type(status)}")
        status_filter = "|".join(processed_statuses)
    
    grant_ids: List[str] = []
    start_record = 0

    while True:
        payload: dict = {
            "startRecordNum": start_record,
            "rows": page_size,
        }
        
        # Add optional filters
        if category_filter:
            payload["fundingCategories"] = category_filter
        if status_filter:
            payload["oppStatuses"] = status_filter
        if keywords:
            payload["keyword"] = keywords.strip()

        response = requests.post(SEARCH2_URL, json=payload, timeout=timeout)
        response.raise_for_status()
        body = response.json()

        if body.get("errorcode") != 0:
            raise RuntimeError(f"Grants.gov search2 error: {body.get('msg')}")

        data = body.get("data", {})
        hits = data.get("oppHits", []) or []
        grant_ids.extend(hit.get("id") for hit in hits if hit.get("id"))

        hit_count = data.get("hitCount", 0)
        start_record += len(hits)
        if start_record >= hit_count or not hits:
            break

    return grant_ids


# Backwards compatibility alias
def get_grant_ids_by_funding_categories(
    categories: Iterable[str],
    *,
    statuses: Iterable[str] | None = None,
    page_size: int = 500,
    timeout: float = 30.0,
) -> List[str]:
    """Legacy function - use get_grant_ids() instead."""
    return get_grant_ids(
        funding_categories=categories,
        statuses=statuses,
        page_size=page_size,
        timeout=timeout
    )