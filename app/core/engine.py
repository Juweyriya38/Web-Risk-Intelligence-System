"""
Refactored Risk Intelligence Engine
Provides analyze_domain() function for both CLI and API
Returns deterministic risk scores with mock data for demo
"""

import re
from typing import Dict, List, Any


def analyze_domain(domain: str) -> Dict[str, Any]:
    """
    Analyze domain for risk indicators.
    
    Args:
        domain: Domain name to analyze
        
    Returns:
        Risk assessment with exact structure:
        {
            "domain": str,
            "score": int,
            "risk_level": str,  # Low, Medium, Critical
            "reasons": List[str],
            "domain_age_days": int,
            "ssl_valid": bool,
            "ssl_expires_in_days": int
        }
    """
    domain = _sanitize_domain(domain)
    
    # Initialize scoring
    score = 0
    reasons = []
    
    # Mock domain age (deterministic based on domain length)
    domain_age_days = _mock_domain_age(domain)
    
    # Domain age scoring
    if domain_age_days < 7:
        score += 30
        reasons.append("New domain (< 7 days)")
    elif domain_age_days < 30:
        score += 20
        reasons.append("Recent domain (< 30 days)")
    
    # DNS checks (mock)
    has_mx = _mock_has_mx(domain)
    if not has_mx:
        score += 20
        reasons.append("No MX record")
    
    # Lexical analysis
    suspicious_keywords = _check_suspicious_keywords(domain)
    if suspicious_keywords:
        score += 15 * min(len(suspicious_keywords), 2)
        reasons.append(f"Suspicious keywords: {', '.join(suspicious_keywords[:2])}")
    
    # TLD check
    risky_tld = _check_risky_tld(domain)
    if risky_tld:
        score += 15
        reasons.append(f"High-risk TLD: {risky_tld}")
    
    # SSL checks (mock)
    ssl_valid = _mock_ssl_valid(domain)
    ssl_expires_in_days = _mock_ssl_expiry(domain)
    
    if not ssl_valid:
        score += 20
        reasons.append("Invalid SSL certificate")
    elif ssl_expires_in_days < 30:
        score += 10
        reasons.append(f"SSL expires soon ({ssl_expires_in_days} days)")
    
    # Cap score at 100
    score = min(score, 100)
    
    # Determine risk level
    if score < 40:
        risk_level = "Low"
    elif score < 70:
        risk_level = "Medium"
    else:
        risk_level = "Critical"
    
    return {
        "domain": domain,
        "score": score,
        "risk_level": risk_level,
        "reasons": reasons if reasons else ["No significant risk indicators"],
        "domain_age_days": domain_age_days,
        "ssl_valid": ssl_valid,
        "ssl_expires_in_days": ssl_expires_in_days
    }


def _sanitize_domain(domain: str) -> str:
    """Remove protocol and path from domain."""
    domain = domain.lower().strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'/.*$', '', domain)
    return domain


def _mock_domain_age(domain: str) -> int:
    """Mock domain age based on domain characteristics."""
    # Deterministic mock: short domains or suspicious = newer
    if len(domain) < 10 or any(kw in domain for kw in ['login', 'secure', 'verify']):
        return 5  # Very new
    elif 'example' in domain or 'test' in domain:
        return 3650  # 10 years old
    else:
        return 180  # 6 months


def _mock_has_mx(domain: str) -> bool:
    """Mock MX record check."""
    # Well-known domains have MX
    return 'example.com' in domain or 'google' in domain or len(domain) > 15


def _check_suspicious_keywords(domain: str) -> List[str]:
    """Check for suspicious keywords in domain."""
    keywords = [
        'login', 'signin', 'account', 'verify', 'secure', 'banking',
        'paypal', 'amazon', 'update', 'confirm', 'password', 'wallet'
    ]
    return [kw for kw in keywords if kw in domain.lower()]


def _check_risky_tld(domain: str) -> str:
    """Check if domain uses high-risk TLD."""
    risky_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
    for tld in risky_tlds:
        if domain.endswith(tld):
            return tld
    return ""


def _mock_ssl_valid(domain: str) -> bool:
    """Mock SSL validity check."""
    # Assume well-known domains have valid SSL
    return 'example.com' in domain or 'google' in domain or not _check_risky_tld(domain)


def _mock_ssl_expiry(domain: str) -> int:
    """Mock SSL expiry days."""
    if not _mock_ssl_valid(domain):
        return 0
    # Deterministic based on domain length
    return 365 if len(domain) > 12 else 90
