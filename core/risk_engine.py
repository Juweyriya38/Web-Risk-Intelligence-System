from models import IntelligenceObject
import yaml

class RiskEngine:
    def __init__(self, config_path="config/settings.yaml"):
        # Load the YAML configuration
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
        self.weights = self.config["weights"]
        self.lists = self.config.get("lists", {})
        self.thresholds = self.config.get("thresholds", {})

    def evaluate(self, io: IntelligenceObject) -> IntelligenceObject:
        """
        Calculates risk score based on the IntelligenceObject signals.
        """
        score = 0
        io.justifications = []  # Ensure we have a clean slate

        # Temporal Signals
        if io.age_days is not None:
            if io.age_days < 7:
                score += self.weights["age_under_7"]
                io.justifications.append(f"Critical: Domain is extremely new ({io.age_days} days).")
            elif io.age_days < 30:
                score += self.weights["age_under_30"]
                io.justifications.append(f"Warning: Domain is less than 30 days old.")

        # Infrastructure Signals
        if io.has_mx is False:
            score += self.weights["missing_mx"]
            io.justifications.append("Infrastructure: No MX records detected.")
        if io.spf_valid is False:
            score += self.weights["missing_spf"]
            io.justifications.append("Infrastructure: SPF missing.")

        # Network Identity
        if io.asn in self.lists.get("disposable_asns", []):
            score += self.weights.get("disposable_asn", 0)
            io.justifications.append(f"Network: Hosted on disposable ASN ({io.asn}).")
        if any(io.domain.endswith(tld) for tld in self.lists.get("free_tlds", [])):
            score += self.weights.get("free_tld", 0)
            io.justifications.append(f"Network: Uses free TLD ({io.domain.split('.')[-1]}).")

        # Behavioral / Lexical Signals
        if getattr(io, "is_punycode", False):
            score += self.weights.get("punycode_detected", 0)
            io.justifications.append("Evasion: Punycode/IDN detected.")
        if getattr(io, "brand_keyword_found", False) and getattr(io, "trust_keyword_found", False):
            score += self.weights.get("brand_trust_collision", 0)
            io.justifications.append("Behavioral: Brand-trust keyword collision detected.")

        # Final Score
        io.risk_score = min(score, 100)
        # Risk Level based on thresholds
        if io.risk_score <= self.thresholds.get("low_max", 39):
            io.risk_level = "Low"
        elif io.risk_score <= self.thresholds.get("medium_max", 69):
            io.risk_level = "Medium"
        else:
            io.risk_level = "High/Critical"

        return io

# -----------------------------
# MOCK TEST LAB
# -----------------------------
if __name__ == "__main__":
    engine = RiskEngine()

    mock_phish = IntelligenceObject(
        domain="xn--chase-vrif-i5a.top",
        age_days=2,
        has_mx=False,
        spf_valid=False,
        asn=12345,
        is_punycode=True,
        brand_keyword_found=True,
        trust_keyword_found=True
    )

    result = engine.evaluate(mock_phish)
    print(f"\n[!] ANALYSIS COMPLETE: {result.domain}")
    print(f"SCORE: {result.risk_score}/100")
    print(f"RISK LEVEL: {result.risk_level}")
    print("JUSTIFICATIONS:")
    for line in result.justifications:
        print(f" - {line}")
