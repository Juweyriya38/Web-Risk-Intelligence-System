"""
Input validation and sanitization.
Ensures only valid domains enter the system.
"""

import re
from typing import Optional


class DomainValidator:
    """Validates and sanitizes domain input."""

    # RFC-compliant domain regex (simplified)
    DOMAIN_PATTERN = re.compile(
        r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*"
        r"[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$"
    )

    @classmethod
    def validate(cls, domain: str) -> str:
        """
        Validate and sanitize domain input.

        Args:
            domain: Raw domain string

        Returns:
            Sanitized domain in lowercase

        Raises:
            ValueError: If domain is invalid
        """
        if not domain:
            raise ValueError("Domain cannot be empty")

        # Remove whitespace and convert to lowercase
        domain = domain.strip().lower()

        # Remove protocol if present
        domain = cls._strip_protocol(domain)

        # Remove path if present
        domain = cls._strip_path(domain)

        # Validate format
        if not cls.DOMAIN_PATTERN.match(domain):
            raise ValueError(f"Invalid domain format: {domain}")

        # Length checks
        if len(domain) > 253:
            raise ValueError("Domain exceeds maximum length (253 characters)")

        labels = domain.split(".")
        if any(len(label) > 63 for label in labels):
            raise ValueError("Domain label exceeds maximum length (63 characters)")

        return domain

    @staticmethod
    def _strip_protocol(domain: str) -> str:
        """Remove http(s):// prefix if present."""
        for prefix in ["https://", "http://", "//", "www."]:
            if domain.startswith(prefix):
                domain = domain[len(prefix) :]
        return domain

    @staticmethod
    def _strip_path(domain: str) -> str:
        """Remove path and query string if present."""
        return domain.split("/")[0].split("?")[0]

    @staticmethod
    def extract_tld(domain: str) -> Optional[str]:
        """Extract TLD from domain."""
        parts = domain.split(".")
        if len(parts) < 2:
            return None
        return f".{parts[-1]}"

    @staticmethod
    def is_punycode(domain: str) -> bool:
        """Check if domain contains punycode (potential homograph attack)."""
        return "xn--" in domain
