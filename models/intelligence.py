from dataclasses import dataclass, field
from typing import Optional, Dict

@dataclass
class IntelligenceObject:
    domain: str
    age_days: Optional[int] = None
    has_mx: Optional[bool] = None
    spf_valid: Optional[bool] = None
    ssl_issuer: Optional[str] = None
    asn: Optional[int] = None
    keywords_score: Optional[int] = None
    tld_score: Optional[int] = None
    raw_data: Dict = field(default_factory=dict)
    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
