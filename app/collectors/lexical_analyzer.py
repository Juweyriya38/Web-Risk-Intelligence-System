"""
Lexical Analyzer - Detects suspicious keywords and risky TLDs.
Pure logic, no external calls.
"""

import logging
from typing import Tuple
from app.core.validators import DomainValidator

logger = logging.getLogger(__name__)


class LexicalAnalyzer:
    """Analyzes domain lexical patterns."""

    def __init__(self, suspicious_keywords: list[str], risky_tlds: list[str]):
        """
        Initialize analyzer with keyword and TLD lists.

        Args:
            suspicious_keywords: List of suspicious keywords
            risky_tlds: List of high-risk TLDs
        """
        self.suspicious_keywords = [kw.lower() for kw in suspicious_keywords]
        self.risky_tlds = [tld.lower() for tld in risky_tlds]

    def analyze(self, domain: str) -> Tuple[list[str], bool, bool]:
        """
        Analyze domain for lexical risk indicators.

        Args:
            domain: Validated domain name

        Returns:
            Tuple of (triggered_keywords, risky_tld, is_punycode)
        """
        domain_lower = domain.lower()

        # Detect triggered keywords
        triggered_keywords = [
            kw for kw in self.suspicious_keywords if kw in domain_lower
        ]

        if triggered_keywords:
            logger.debug(f"Triggered keywords in {domain}: {triggered_keywords}")

        # Check TLD
        tld = DomainValidator.extract_tld(domain)
        risky_tld = tld in self.risky_tlds if tld else False

        if risky_tld:
            logger.debug(f"Risky TLD detected: {tld}")

        # Check punycode
        is_punycode = DomainValidator.is_punycode(domain)

        if is_punycode:
            logger.debug(f"Punycode detected in {domain}")

        return triggered_keywords, risky_tld, is_punycode
