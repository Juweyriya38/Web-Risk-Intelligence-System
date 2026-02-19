"""
DNS Collector - Gathers DNS intelligence signals.
Handles timeouts gracefully, returns partial results.
"""

import dns.resolver
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class DNSCollector:
    """Collects DNS-related intelligence signals."""

    def __init__(self, timeout: int = 5):
        """
        Initialize DNS collector.

        Args:
            timeout: DNS query timeout in seconds
        """
        self.timeout = timeout
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout

    def collect(self, domain: str) -> Tuple[bool, bool, list[str]]:
        """
        Collect DNS signals for domain.

        Args:
            domain: Validated domain name

        Returns:
            Tuple of (has_mx, has_spf, errors)
        """
        has_mx = False
        has_spf = False
        errors = []

        # Check MX records
        try:
            mx_records = self.resolver.resolve(domain, "MX")
            has_mx = len(mx_records) > 0
            logger.debug(f"Found {len(mx_records)} MX records for {domain}")
        except dns.resolver.NoAnswer:
            logger.debug(f"No MX records for {domain}")
        except dns.resolver.NXDOMAIN:
            errors.append(f"DNS: Domain does not exist")
            logger.warning(f"NXDOMAIN for {domain}")
        except dns.exception.Timeout:
            errors.append(f"DNS: Query timeout")
            logger.warning(f"DNS timeout for {domain}")
        except Exception as e:
            errors.append(f"DNS: {str(e)}")
            logger.error(f"DNS error for {domain}: {e}")

        # Check SPF records (TXT)
        try:
            txt_records = self.resolver.resolve(domain, "TXT")
            for record in txt_records:
                txt_value = record.to_text()
                if "v=spf1" in txt_value.lower():
                    has_spf = True
                    logger.debug(f"Found SPF record for {domain}")
                    break
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            logger.debug(f"No SPF records for {domain}")
        except dns.exception.Timeout:
            logger.warning(f"SPF lookup timeout for {domain}")
        except Exception as e:
            logger.error(f"SPF lookup error for {domain}: {e}")

        return has_mx, has_spf, errors
