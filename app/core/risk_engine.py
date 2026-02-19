"""
Risk Engine - Pure business logic.
No network calls, no I/O, no side effects.
Accepts IntelligenceObject, returns RiskResult.
"""

from app.core.models import (
    IntelligenceObject,
    RiskResult,
    RiskRuleResult,
    ConfigurationSchema,
)


class RiskEngine:
    """
    Deterministic risk scoring engine.
    Applies weighted rules to intelligence signals.
    """

    def __init__(self, config: ConfigurationSchema):
        """
        Initialize engine with configuration.

        Args:
            config: Validated configuration schema
        """
        self.config = config
        self.weights = config.risk_weights
        self.thresholds = config.risk_thresholds

    def evaluate(self, intelligence: IntelligenceObject) -> RiskResult:
        """
        Evaluate risk based on intelligence signals.

        Args:
            intelligence: Collected domain intelligence

        Returns:
            Complete risk assessment result
        """
        triggered_rules: list[RiskRuleResult] = []

        # Evaluate all rules
        triggered_rules.extend(self._evaluate_domain_age(intelligence))
        triggered_rules.extend(self._evaluate_dns_signals(intelligence))
        triggered_rules.extend(self._evaluate_ssl_signals(intelligence))
        triggered_rules.extend(self._evaluate_behavioral_signals(intelligence))
        triggered_rules.extend(self._evaluate_failure_signals(intelligence))

        # Calculate total score (capped at 100)
        total_score = min(sum(rule.weight for rule in triggered_rules if rule.triggered), 100)

        # Classify risk level
        classification = self._classify_risk(total_score)

        return RiskResult(
            domain=intelligence.domain,
            score=total_score,
            classification=classification,
            triggered_rules=triggered_rules,
            intelligence=intelligence,
        )

    def _evaluate_domain_age(self, intel: IntelligenceObject) -> list[RiskRuleResult]:
        """Evaluate domain age signals."""
        rules = []

        if intel.age_days is not None:
            if intel.age_days < 7:
                rules.append(
                    RiskRuleResult(
                        rule_name="domain_age_very_new",
                        triggered=True,
                        weight=self.weights.domain_age_very_new,
                        justification=f"Domain registered {intel.age_days} days ago (< 7 days)",
                    )
                )
            elif intel.age_days < 30:
                rules.append(
                    RiskRuleResult(
                        rule_name="domain_age_new",
                        triggered=True,
                        weight=self.weights.domain_age_new,
                        justification=f"Domain registered {intel.age_days} days ago (< 30 days)",
                    )
                )
            elif intel.age_days < 90:
                rules.append(
                    RiskRuleResult(
                        rule_name="domain_age_recent",
                        triggered=True,
                        weight=self.weights.domain_age_recent,
                        justification=f"Domain registered {intel.age_days} days ago (< 90 days)",
                    )
                )

        return rules

    def _evaluate_dns_signals(self, intel: IntelligenceObject) -> list[RiskRuleResult]:
        """Evaluate DNS configuration signals."""
        rules = []

        if not intel.has_mx:
            rules.append(
                RiskRuleResult(
                    rule_name="no_mx_records",
                    triggered=True,
                    weight=self.weights.no_mx_records,
                    justification="No MX records found (no email infrastructure)",
                )
            )

        if not intel.has_spf:
            rules.append(
                RiskRuleResult(
                    rule_name="no_spf_records",
                    triggered=True,
                    weight=self.weights.no_spf_records,
                    justification="No SPF records found (no email authentication)",
                )
            )

        return rules

    def _evaluate_ssl_signals(self, intel: IntelligenceObject) -> list[RiskRuleResult]:
        """Evaluate SSL certificate signals."""
        rules = []

        if not intel.ssl_valid:
            rules.append(
                RiskRuleResult(
                    rule_name="ssl_invalid",
                    triggered=True,
                    weight=self.weights.ssl_invalid,
                    justification="SSL certificate invalid or not present",
                )
            )

        if intel.is_self_signed:
            rules.append(
                RiskRuleResult(
                    rule_name="ssl_self_signed",
                    triggered=True,
                    weight=self.weights.ssl_self_signed,
                    justification="SSL certificate is self-signed",
                )
            )

        return rules

    def _evaluate_behavioral_signals(self, intel: IntelligenceObject) -> list[RiskRuleResult]:
        """Evaluate behavioral indicators."""
        rules = []

        if intel.risky_tld:
            rules.append(
                RiskRuleResult(
                    rule_name="risky_tld",
                    triggered=True,
                    weight=self.weights.risky_tld,
                    justification=f"High-risk TLD detected",
                )
            )

        # Keyword scoring (max 2 keywords to avoid over-penalization)
        keyword_count = min(len(intel.triggered_keywords), 2)
        if keyword_count > 0:
            rules.append(
                RiskRuleResult(
                    rule_name="suspicious_keyword",
                    triggered=True,
                    weight=self.weights.suspicious_keyword * keyword_count,
                    justification=f"Suspicious keywords: {', '.join(intel.triggered_keywords[:2])}",
                )
            )

        if intel.is_punycode:
            rules.append(
                RiskRuleResult(
                    rule_name="punycode_detected",
                    triggered=True,
                    weight=self.weights.punycode_detected,
                    justification="Punycode detected (potential homograph attack)",
                )
            )

        return rules

    def _evaluate_failure_signals(self, intel: IntelligenceObject) -> list[RiskRuleResult]:
        """Evaluate failure signals as risk indicators."""
        rules = []

        for error in intel.errors:
            if "whois" in error.lower():
                rules.append(
                    RiskRuleResult(
                        rule_name="whois_lookup_failed",
                        triggered=True,
                        weight=self.weights.whois_lookup_failed,
                        justification="WHOIS lookup failed or timed out",
                    )
                )
            elif "dns" in error.lower():
                rules.append(
                    RiskRuleResult(
                        rule_name="dns_resolution_failed",
                        triggered=True,
                        weight=self.weights.dns_resolution_failed,
                        justification="DNS resolution failed",
                    )
                )

        return rules

    def _classify_risk(self, score: int) -> str:
        """Classify risk level based on score."""
        if score >= self.thresholds.critical:
            return "Critical"
        elif score >= self.thresholds.high:
            return "High"
        elif score >= self.thresholds.medium:
            return "Medium"
        else:
            return "Low"
