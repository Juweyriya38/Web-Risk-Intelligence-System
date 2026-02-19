"""
WHOIS Collector - Gathers domain registration intelligence.
Handles timeouts and parsing failures gracefully.
"""

import whois
import logging
from datetime import datetime
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


class WHOISCollector:
    """Collects WHOIS registration data."""

    def __init__(self, timeout: int = 10):
        """
        Initialize WHOIS collector.

        Args:
            timeout: WHOIS query timeout in seconds
        """
        self.timeout = timeout

    def collect(self, domain: str) -> Tuple[Optional[int], list[str]]:
        """
        Collect WHOIS data for domain.

        Args:
            domain: Validated domain name

        Returns:
            Tuple of (age_days, errors)
        """
        age_days = None
        errors = []

        try:
            w = whois.whois(domain)

            # Extract creation date
            creation_date = w.creation_date

            # Handle list of dates (some registrars return multiple)
            if isinstance(creation_date, list):
                creation_date = creation_date[0] if creation_date else None

            if creation_date:
                if isinstance(creation_date, datetime):
                    age_days = (datetime.now() - creation_date).days
                    logger.debug(f"Domain {domain} is {age_days} days old")
                else:
                    logger.warning(f"Unexpected creation_date type for {domain}: {type(creation_date)}")
            else:
                logger.warning(f"No creation date found for {domain}")

        except whois.parser.PywhoisError as e:
            errors.append(f"WHOIS: Parsing error")
            logger.warning(f"WHOIS parsing error for {domain}: {e}")
        except Exception as e:
            errors.append(f"WHOIS: Lookup failed")
            logger.error(f"WHOIS error for {domain}: {e}")

        return age_days, errors
