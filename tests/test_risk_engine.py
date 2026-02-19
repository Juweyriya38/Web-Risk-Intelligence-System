"""
Unit tests for Risk Engine.
Tests deterministic scoring logic.
"""

import pytest
from app.core.models import (
    IntelligenceObject,
    ConfigurationSchema,
    RiskWeights,
    RiskThresholds,
    Timeouts,
)
from app.core.risk_engine import RiskEngine


@pytest.fixture
def test_config():
    """Create test configuration."""
    return ConfigurationSchema(
        risk_weights=RiskWeights(
            domain_age_very_new=25,
            domain_age_new=15,
            domain_age_recent=8,
            no_mx_records=15,
            no_spf_records=10,
            ssl_invalid=20,
            ssl_self_signed=15,
            risky_tld=20,
            suspicious_keyword=15,
            punycode_detected=25,
            whois_lookup_failed=10,
            dns_resolution_failed=15,
        ),
        risk_thresholds=RiskThresholds(low=0, medium=30, high=60, critical=80),
        risky_tlds=[".tk", ".xyz"],
        suspicious_keywords=["login", "secure"],
        trusted_keywords=["official"],
        timeouts=Timeouts(dns=5, whois=10, ssl=10),
    )


@pytest.fixture
def risk_engine(test_config):
    """Create risk engine instance."""
    return RiskEngine(test_config)


def test_low_risk_domain(risk_engine):
    """Test legitimate domain with low risk."""
    intel = IntelligenceObject(
        domain="google.com",
        age_days=5000,
        has_mx=True,
        has_spf=True,
        ssl_valid=True,
        is_self_signed=False,
        risky_tld=False,
        is_punycode=False,
    )

    result = risk_engine.evaluate(intel)

    assert result.score == 0
    assert result.classification == "Low"


def test_high_risk_new_domain(risk_engine):
    """Test newly registered domain with minimal infrastructure."""
    intel = IntelligenceObject(
        domain="suspicious-login.tk",
        age_days=3,
        has_mx=False,
        has_spf=False,
        ssl_valid=False,
        is_self_signed=False,
        triggered_keywords=["login"],
        risky_tld=True,
        is_punycode=False,
    )

    result = risk_engine.evaluate(intel)

    # 25 (very new) + 15 (no mx) + 10 (no spf) + 20 (ssl invalid) + 20 (risky tld) + 15 (keyword)
    expected_score = 25 + 15 + 10 + 20 + 20 + 15
    assert result.score == expected_score
    assert result.classification == "Critical"


def test_domain_age_thresholds(risk_engine):
    """Test domain age threshold boundaries."""
    # Very new (< 7 days)
    intel = IntelligenceObject(domain="test.com", age_days=6)
    result = risk_engine.evaluate(intel)
    assert any(r.rule_name == "domain_age_very_new" and r.triggered for r in result.triggered_rules)

    # New (< 30 days)
    intel = IntelligenceObject(domain="test.com", age_days=20)
    result = risk_engine.evaluate(intel)
    assert any(r.rule_name == "domain_age_new" and r.triggered for r in result.triggered_rules)

    # Recent (< 90 days)
    intel = IntelligenceObject(domain="test.com", age_days=60)
    result = risk_engine.evaluate(intel)
    assert any(r.rule_name == "domain_age_recent" and r.triggered for r in result.triggered_rules)

    # Old (>= 90 days)
    intel = IntelligenceObject(domain="test.com", age_days=100)
    result = risk_engine.evaluate(intel)
    age_rules = [r for r in result.triggered_rules if "age" in r.rule_name and r.triggered]
    assert len(age_rules) == 0


def test_keyword_scoring_cap(risk_engine):
    """Test that keyword scoring is capped at 2 keywords."""
    intel = IntelligenceObject(
        domain="test.com",
        triggered_keywords=["login", "secure", "banking", "verify"],
    )

    result = risk_engine.evaluate(intel)

    # Should only count 2 keywords max
    keyword_rules = [r for r in result.triggered_rules if r.rule_name == "suspicious_keyword"]
    assert len(keyword_rules) == 1
    assert keyword_rules[0].weight == 15 * 2  # 2 keywords max


def test_score_capped_at_100(risk_engine):
    """Test that total score never exceeds 100."""
    intel = IntelligenceObject(
        domain="xn--test.tk",
        age_days=1,
        has_mx=False,
        has_spf=False,
        ssl_valid=False,
        is_self_signed=True,
        triggered_keywords=["login", "secure"],
        risky_tld=True,
        is_punycode=True,
        errors=["WHOIS: timeout", "DNS: failed"],
    )

    result = risk_engine.evaluate(intel)

    assert result.score <= 100


def test_classification_thresholds(risk_engine):
    """Test risk classification boundaries."""
    # Low
    intel = IntelligenceObject(domain="test.com", age_days=100)
    result = risk_engine.evaluate(intel)
    assert result.classification == "Low"

    # Medium
    intel = IntelligenceObject(domain="test.com", has_mx=False, has_spf=False)
    result = risk_engine.evaluate(intel)
    assert result.score >= 30
    assert result.classification == "Medium"

    # High
    intel = IntelligenceObject(
        domain="test.tk", age_days=5, has_mx=False, ssl_valid=False, risky_tld=True
    )
    result = risk_engine.evaluate(intel)
    assert result.score >= 60
    assert result.classification in ["High", "Critical"]


def test_punycode_detection(risk_engine):
    """Test punycode detection scoring."""
    intel = IntelligenceObject(domain="xn--test.com", is_punycode=True)

    result = risk_engine.evaluate(intel)

    assert any(r.rule_name == "punycode_detected" and r.triggered for r in result.triggered_rules)


def test_failure_signals(risk_engine):
    """Test that failures are treated as risk signals."""
    intel = IntelligenceObject(
        domain="test.com",
        errors=["WHOIS: lookup failed", "DNS: resolution timeout"],
    )

    result = risk_engine.evaluate(intel)

    assert result.score > 0
    assert any("whois" in r.rule_name.lower() and r.triggered for r in result.triggered_rules)
    assert any("dns" in r.rule_name.lower() and r.triggered for r in result.triggered_rules)
