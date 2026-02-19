"""
SSL Collector - Gathers SSL/TLS certificate intelligence.
Validates certificates and detects self-signed certs.
"""

import ssl
import socket
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class SSLCollector:
    """Collects SSL certificate data."""

    def __init__(self, timeout: int = 10):
        """
        Initialize SSL collector.

        Args:
            timeout: SSL connection timeout in seconds
        """
        self.timeout = timeout

    def collect(self, domain: str) -> Tuple[bool, bool, list[str]]:
        """
        Collect SSL certificate data for domain.

        Args:
            domain: Validated domain name

        Returns:
            Tuple of (ssl_valid, is_self_signed, errors)
        """
        ssl_valid = False
        is_self_signed = False
        errors = []

        context = ssl.create_default_context()

        try:
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    ssl_valid = True
                    logger.debug(f"Valid SSL certificate for {domain}")

                    # Check if self-signed (issuer == subject)
                    issuer = dict(x[0] for x in cert.get("issuer", []))
                    subject = dict(x[0] for x in cert.get("subject", []))

                    if issuer == subject:
                        is_self_signed = True
                        logger.debug(f"Self-signed certificate detected for {domain}")

        except ssl.SSLError as e:
            logger.warning(f"SSL error for {domain}: {e}")
            # Check if self-signed by attempting unverified connection
            is_self_signed = self._check_self_signed_unverified(domain)
        except socket.timeout:
            errors.append("SSL: Connection timeout")
            logger.warning(f"SSL timeout for {domain}")
        except socket.gaierror:
            errors.append("SSL: DNS resolution failed")
            logger.warning(f"SSL DNS error for {domain}")
        except ConnectionRefusedError:
            errors.append("SSL: Connection refused (no HTTPS)")
            logger.debug(f"No HTTPS service on {domain}")
        except Exception as e:
            errors.append(f"SSL: {str(e)}")
            logger.error(f"SSL error for {domain}: {e}")

        return ssl_valid, is_self_signed, errors

    def _check_self_signed_unverified(self, domain: str) -> bool:
        """Check if certificate is self-signed using unverified context."""
        try:
            context = ssl._create_unverified_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get("issuer", []))
                    subject = dict(x[0] for x in cert.get("subject", []))
                    return issuer == subject
        except Exception:
            return False
