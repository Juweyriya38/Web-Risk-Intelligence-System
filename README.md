# Web-Risk-Intelligence-System
A modular, explainable web infrastructure intelligence platform that evaluates public trust signals and produces structured, defensible risk assessments for domains.


## Overview
## Architecture
## Signals Evaluated
## Risk Scoring Model
## Example Output
## Installation
## Usage
## Roadmap
## License

web-risk-intelligence-system/
│
├── collectors/
├── core/
├── config/
├── utils/
├── tests/
│
├── main.py
├── requirements.txt
├── LICENSE
└── .gitignore


# Web Risk Intelligence System

A modular, explainable web infrastructure intelligence platform that evaluates public trust signals and produces structured, defensible risk assessments for domains.

---

## 1. Overview

The Web Risk Intelligence System is a rule-based decision-support engine designed to evaluate digital trust at the infrastructure level.

Given a domain name, the system:

* Collects public infrastructure intelligence
* Translates technical signals into risk indicators
* Aggregates them using configurable weighted scoring
* Produces explainable, structured risk assessments

This is not a vulnerability scanner or malware sandbox.
It is an infrastructure-level trust evaluation engine.

---

## 2. Problem Statement

Modern phishing and impersonation attacks rely heavily on disposable infrastructure:

* Newly registered domains
* Abuse-prone TLDs
* Minimal DNS configuration
* Free SSL certificates
* Obfuscated WHOIS records

Security teams require fast, explainable risk evaluations to support defensive decisions.

This system provides deterministic, transparent scoring without relying on opaque machine learning models.

---

## 3. System Architecture

### Logic Flow

```
User Input (Domain)
        ↓
Input Validation
        ↓
Collectors Layer
    - DNS Collector
    - WHOIS Collector
    - SSL Collector
    - ASN Collector
    - Keyword/TLD Analyzer
        ↓
IntelligenceObject (Standard Data Contract)
        ↓
Risk Engine (Configurable Weighted Scoring)
        ↓
Pattern Detection Layer (Composite Risk Logic)
        ↓
Justification Mapper
        ↓
Structured Output (CLI / JSON)
```

---

## 4. Core Design Principles

1. Deterministic scoring (no hidden logic)
2. Strict data contract via IntelligenceObject
3. Separation of collection and scoring
4. Config-driven risk weights
5. Explainable output
6. Failure signals treated as intelligence
7. Modular and extensible architecture

---

## 5. Data Contract (IntelligenceObject)

All modules operate on a standardized data structure.

```python
@dataclass
class IntelligenceObject:
    domain: str

    # Infrastructure Signals
    age_days: Optional[int]
    has_mx: bool
    has_spf: bool
    ssl_valid: bool
    is_self_signed: bool
    asn_org: Optional[str]

    # Behavioral Signals
    triggered_keywords: List[str]
    risky_tld: bool

    # Failure Signals
    errors: List[str]

    # Final Output
    risk_score: int
    justifications: List[str]
```

This ensures:

* Module consistency
* Scoring reliability
* Expandability

---

## 6. Signals Evaluated

### Infrastructure Signals

* Domain age (days since registration)
* Presence of MX records
* Presence of SPF records
* SSL certificate validity
* Self-signed certificate detection
* ASN organization metadata

### Behavioral Indicators

* Suspicious keyword detection
* Risk-prone TLD usage

### Failure Signals

* WHOIS timeouts
* DNS resolution failures
* SSL handshake errors

Absence of expected infrastructure is treated as a risk signal.

---

## 7. Risk Scoring Model

The system uses rule-based weighted scoring.

Risk score = Σ(weight × triggered signal)

Characteristics:

* Configurable via `settings.yaml`
* Capped at 100
* Deterministic
* Fully explainable

Weights are externalized to configuration for tuning and transparency.

---

## 8. Pattern Detection Layer

Beyond individual signals, the engine detects composite risk patterns.

Examples:

Ghost Pattern

* Domain age < 7 days
* No MX records
  → Indicates likely automated disposable registration

Authority Pattern

* Login-related keywords
* Valid SSL certificate
  → Classic phishing landing behavior

Homograph Pattern

* Punycode (xn--) detection
  → Potential character spoofing attack

Patterns enhance justification but do not override core scoring.

---

## 9. Threat Model

The system assumes adversaries may attempt:

* Rapid domain registration cycles
* Abuse-prone TLD selection
* Infrastructure minimalism
* Brand impersonation via keyword stuffing
* WHOIS obfuscation
* Homograph spoofing

The engine is designed to evaluate these behaviors at the infrastructure level.

---

## 10. Project Structure

```
web-risk-intelligence-system/
│
├── collectors/
├── core/
├── config/
├── utils/
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 11. CLI Usage

Basic:

```
python main.py example.com
```

Verbose:

```
python main.py example.com --verbose
```

JSON Output:

```
python main.py example.com --json
```

---

## 12. Example Output

Human-readable:

```
Risk Score: 78 (HIGH)

Reasons:
- Domain age under 7 days
- No MX records detected
- Risk-prone TLD (.top)
- Suspicious keyword: login
```

JSON:

```json
{
  "domain": "secure-login.top",
  "risk_score": 78,
  "signals": {
    "age_days": 2,
    "has_mx": false,
    "risky_tld": true
  },
  "justifications": [...]
}
```

---

## 13. Configuration

Risk weights, keyword lists, and TLD risk lists are defined in:

```
config/settings.yaml
```

This enables tuning without modifying core logic.

---

## 14. Reliability & Safety Controls

* Input sanitization using domain validation
* Rate limiting between network calls
* Timeout handling
* Graceful partial-result handling
* Environment variable support for future API integrations

---

## 15. Future Expansion

Planned enhancements:

* Brand similarity scoring
* ASN reputation scoring
* Domain monitoring over time
* Government impersonation detection
* Integration with external intelligence sources
* REST API interface

---

## 16. Installation

```
pip install -r requirements.txt
```

---

## 17. License

MIT License

---

