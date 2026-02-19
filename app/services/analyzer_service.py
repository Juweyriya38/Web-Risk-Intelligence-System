"""
Analyzer Service - Orchestrates collection and risk assessment.
This is the main entry point for both CLI and API.
"""

import logging
from app.core.models import IntelligenceObject, RiskResult, ConfigurationSchema
from app.core.validators import DomainValidator
from app.core.risk_engine import RiskEngine
from app.collectors.dns_collector import DNSCollector
from app.collectors.whois_collector import WHOISCollector
from app.collectors.ssl_collector import SSLCollector
from app.collectors.lexical_analyzer import LexicalAnalyzer

logger = logging.getLogger(__name__)


class AnalyzerService:
    """
    Domain risk analysis service.
    Coordinates collectors and risk engine.
    """

    def __init__(self, config: ConfigurationSchema):
        """
        Initialize service with configuration.

        Args:
            config: Validated configuration schema
        """
        self.config = config
        self.risk_engine = RiskEngine(config)

        # Initialize collectors
        self.dns_collector = DNSCollector(timeout=config.timeouts.dns)
        self.whois_collector = WHOISCollector(timeout=config.timeouts.whois)
        self.ssl_collector = SSLCollector(timeout=config.timeouts.ssl)
        self.lexical_analyzer = LexicalAnalyzer(
            suspicious_keywords=config.suspicious_keywords,
            risky_tlds=config.risky_tlds,
        )

    def analyze_domain(self, domain: str) -> RiskResult:
        """
        Perform complete risk analysis on domain.

        Args:
            domain: Raw domain input

        Returns:
            Complete risk assessment result

        Raises:
            ValueError: If domain is invalid
        """
        # Validate and sanitize input
        validated_domain = DomainValidator.validate(domain)
        logger.info(f"Analyzing domain: {validated_domain}")

        # Collect intelligence
        intelligence = self._collect_intelligence(validated_domain)

        # Evaluate risk
        result = self.risk_engine.evaluate(intelligence)

        logger.info(
            f"Analysis complete: {validated_domain} - "
            f"Score: {result.score}, Classification: {result.classification}"
        )

        return result

    def _collect_intelligence(self, domain: str) -> IntelligenceObject:
        """
        Collect all intelligence signals for domain.

        Args:
            domain: Validated domain name

        Returns:
            Populated intelligence object
        """
        errors = []

        # DNS collection
        has_mx, has_spf, dns_errors = self.dns_collector.collect(domain)
        errors.extend(dns_errors)

        # WHOIS collection
        age_days, whois_errors = self.whois_collector.collect(domain)
        errors.extend(whois_errors)

        # SSL collection
        ssl_valid, is_self_signed, ssl_errors = self.ssl_collector.collect(domain)
        errors.extend(ssl_errors)

        # Lexical analysis
        triggered_keywords, risky_tld, is_punycode = self.lexical_analyzer.analyze(domain)

        # Build intelligence object
        intelligence = IntelligenceObject(
            domain=domain,
            age_days=age_days,
            has_mx=has_mx,
            has_spf=has_spf,
            ssl_valid=ssl_valid,
            is_self_signed=is_self_signed,
            triggered_keywords=triggered_keywords,
            risky_tld=risky_tld,
            is_punycode=is_punycode,
            errors=errors,
        )

        logger.debug(f"Intelligence collected: {intelligence}")

        return intelligence
