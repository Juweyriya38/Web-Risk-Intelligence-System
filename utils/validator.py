# utils/validator.py

import re
import idna  # for punycode / IDN handling
from models import IntelligenceObject

def clean_domain(domain: str) -> str:
    """
    Strip protocol, whitespace, and lowercase.
    """
    domain = domain.strip().lower()
    domain = re.sub(r"^https?://", "", domain)
    domain = re.sub(r"/.*$", "", domain)  # remove paths
    return domain

def is_punycode(domain: str) -> bool:
    """
    Detect if domain uses punycode (xn-- prefix)
    """
    try:
        return domain.startswith("xn--") or "xn--" in idna.encode(domain).decode()
    except Exception:
        return False

def detect_keywords(domain: str, brand_keywords: list, trust_keywords: list) -> tuple:
    """
    Check for brand + trust keyword collision
    """
    brand_found = any(kw in domain for kw in brand_keywords)
    trust_found = any(kw in domain for kw in trust_keywords)
    return brand_found, trust_found

def validate_domain(domain: str, lists: dict) -> IntelligenceObject:
    """
    Returns a fully-prepped IntelligenceObject for RiskEngine
    """
    clean = clean_domain(domain)
    io = IntelligenceObject(domain=clean)

    # Punycode
    io.is_punycode = is_punycode(clean)

    # Brand / trust keywords
    io.brand_keyword_found, io.trust_keyword_found = detect_keywords(
        clean, lists.get("brand_keywords", []), lists.get("trust_keywords", [])
    )

    # Free / risky TLDs
    io.tld_score = 0
    io.tld_flagged = any(clean.endswith(tld) for tld in lists.get("risky_tlds", []))

    return io

# -----------------------------
# MOCK TEST LAB
# -----------------------------
if __name__ == "__main__":
    from config.settings import SETTINGS  # or import YAML if needed
    lists = SETTINGS["lists"]

    test_domains = [
        "https://xn--chase-vrif-i5a.top/path",
        "http://paypal-secure.xyz",
        "https://good.com"
    ]

    for d in test_domains:
        io = validate_domain(d, lists)
        print(f"Domain: {io.domain}")
        print(f"  Punycode: {io.is_punycode}")
        print(f"  Brand Keyword: {io.brand_keyword_found}")
        print(f"  Trust Keyword: {io.trust_keyword_found}")
        print(f"  Risky TLD: {io.tld_flagged}")
        print("-" * 40)
