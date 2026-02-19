"""
Core data models for the risk intelligence system.
All modules operate on these standardized structures.
"""

from typing import Optional
from pydantic import BaseModel, Field


class IntelligenceObject(BaseModel):
    """
    Standard data contract for domain intelligence.
    Populated by collectors, consumed by risk engine.
    """

    domain: str

    # Infrastructure signals
    age_days: Optional[int] = None
    has_mx: bool = False
    has_spf: bool = False
    ssl_valid: bool = False
    is_self_signed: bool = False
    asn_org: Optional[str] = None

    # Behavioral signals
    triggered_keywords: list[str] = Field(default_factory=list)
    risky_tld: bool = False
    is_punycode: bool = False

    # Failure signals
    errors: list[str] = Field(default_factory=list)


class RiskRuleResult(BaseModel):
    """Individual risk rule evaluation result."""

    rule_name: str
    triggered: bool
    weight: int
    justification: str


class RiskResult(BaseModel):
    """Final risk assessment output."""

    domain: str
    score: int = Field(ge=0, le=100)
    classification: str  # Low, Medium, High, Critical
    triggered_rules: list[RiskRuleResult]
    intelligence: IntelligenceObject


class RiskWeights(BaseModel):
    """Risk scoring weights from configuration."""

    domain_age_very_new: int
    domain_age_new: int
    domain_age_recent: int
    no_mx_records: int
    no_spf_records: int
    ssl_invalid: int
    ssl_self_signed: int
    risky_tld: int
    suspicious_keyword: int
    punycode_detected: int
    whois_lookup_failed: int
    dns_resolution_failed: int


class RiskThresholds(BaseModel):
    """Risk classification thresholds."""

    low: int
    medium: int
    high: int
    critical: int


class Timeouts(BaseModel):
    """Collector timeout configuration."""

    dns: int
    whois: int
    ssl: int


class ConfigurationSchema(BaseModel):
    """Complete configuration schema with validation."""

    risk_weights: RiskWeights
    risk_thresholds: RiskThresholds
    risky_tlds: list[str]
    suspicious_keywords: list[str]
    trusted_keywords: list[str]
    timeouts: Timeouts

    def validate_config(self) -> None:
        """Validate configuration logic."""
        # Ensure no negative weights
        for field, value in self.risk_weights.model_dump().items():
            if value < 0:
                raise ValueError(f"Weight {field} cannot be negative: {value}")

        # Ensure thresholds are logical
        thresholds = self.risk_thresholds
        if not (thresholds.low < thresholds.medium < thresholds.high < thresholds.critical):
            raise ValueError("Risk thresholds must be in ascending order")

        if thresholds.critical > 100:
            raise ValueError("Critical threshold cannot exceed 100")
