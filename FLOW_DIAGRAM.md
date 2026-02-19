# System Flow Diagram

## Complete Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│                                                                 │
│  CLI: python main_cli.py analyze example.com                   │
│  API: POST /api/v1/analyze {"domain": "example.com"}           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT VALIDATION                             │
│                                                                 │
│  DomainValidator.validate()                                     │
│  • Strip protocol (https://)                                    │
│  • Strip path (/page)                                           │
│  • Lowercase                                                    │
│  • RFC compliance check                                         │
│  • Length validation                                            │
│                                                                 │
│  ✓ Valid: "example.com"                                         │
│  ✗ Invalid: ValueError raised                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                   ANALYZER SERVICE                              │
│                                                                 │
│  AnalyzerService.analyze_domain()                               │
│  • Orchestrates all collectors                                  │
│  • Builds IntelligenceObject                                    │
│  • Invokes Risk Engine                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  PARALLEL COLLECTION                            │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ DNS          │  │ WHOIS        │  │ SSL          │         │
│  │ Collector    │  │ Collector    │  │ Collector    │         │
│  │              │  │              │  │              │         │
│  │ • MX records │  │ • Domain age │  │ • Cert valid │         │
│  │ • SPF records│  │ • Creation   │  │ • Self-signed│         │
│  │              │  │   date       │  │              │         │
│  │ Timeout: 5s  │  │ Timeout: 10s │  │ Timeout: 10s │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                 │                 │                  │
│         └─────────────────┴─────────────────┘                  │
│                           │                                     │
│                           ↓                                     │
│                  ┌──────────────────┐                          │
│                  │ Lexical Analyzer │                          │
│                  │                  │                          │
│                  │ • Keywords       │                          │
│                  │ • TLD check      │                          │
│                  │ • Punycode       │                          │
│                  │                  │                          │
│                  │ (Pure logic)     │                          │
│                  └──────────────────┘                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE OBJECT                            │
│                                                                 │
│  IntelligenceObject {                                           │
│    domain: "example.com"                                        │
│    age_days: 9000                                               │
│    has_mx: true                                                 │
│    has_spf: true                                                │
│    ssl_valid: true                                              │
│    is_self_signed: false                                        │
│    triggered_keywords: []                                       │
│    risky_tld: false                                             │
│    is_punycode: false                                           │
│    errors: []                                                   │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RISK ENGINE (PURE)                           │
│                                                                 │
│  RiskEngine.evaluate()                                          │
│                                                                 │
│  1. Evaluate domain age                                         │
│     ✗ Not triggered (9000 days old)                            │
│                                                                 │
│  2. Evaluate DNS signals                                        │
│     ✗ Has MX records                                           │
│     ✗ Has SPF records                                          │
│                                                                 │
│  3. Evaluate SSL signals                                        │
│     ✗ SSL is valid                                             │
│                                                                 │
│  4. Evaluate behavioral signals                                 │
│     ✗ No suspicious keywords                                   │
│     ✗ Not risky TLD                                            │
│     ✗ Not punycode                                             │
│                                                                 │
│  5. Evaluate failure signals                                    │
│     ✗ No errors                                                │
│                                                                 │
│  Total Score: 0                                                 │
│  Classification: Low                                            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      RISK RESULT                                │
│                                                                 │
│  RiskResult {                                                   │
│    domain: "example.com"                                        │
│    score: 0                                                     │
│    classification: "Low"                                        │
│    triggered_rules: []                                          │
│    intelligence: { ... }                                        │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    OUTPUT FORMATTING                            │
│                                                                 │
│  CLI: Human-readable with colors                                │
│  API: JSON response                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## High-Risk Domain Example

```
Input: "secure-login.tk" (3 days old)

┌─────────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE OBJECT                            │
│                                                                 │
│  domain: "secure-login.tk"                                      │
│  age_days: 3                          ← ⚠️ Very new            │
│  has_mx: false                        ← ⚠️ No email            │
│  has_spf: false                       ← ⚠️ No SPF              │
│  ssl_valid: false                     ← ⚠️ No SSL              │
│  triggered_keywords: ["secure","login"] ← ⚠️ Suspicious        │
│  risky_tld: true                      ← ⚠️ .tk TLD             │
│  is_punycode: false                                             │
│  errors: []                                                     │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RISK ENGINE                                  │
│                                                                 │
│  ✓ Domain age < 7 days          → +25                          │
│  ✓ No MX records                → +15                          │
│  ✓ No SPF records               → +10                          │
│  ✓ SSL invalid                  → +20                          │
│  ✓ Risky TLD (.tk)              → +20                          │
│  ✓ Keywords (2): secure, login  → +30 (15×2)                   │
│                                                                 │
│  Total: 120 → Capped at 100                                     │
│  Classification: CRITICAL                                       │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT                                     │
│                                                                 │
│  Risk Score: 100/100 (CRITICAL)                                 │
│                                                                 │
│  Risk Indicators:                                               │
│  • Domain registered 3 days ago (< 7 days) (+25)                │
│  • No MX records found (no email infrastructure) (+15)          │
│  • No SPF records found (no email authentication) (+10)         │
│  • SSL certificate invalid or not present (+20)                 │
│  • High-risk TLD detected (+20)                                 │
│  • Suspicious keywords: secure, login (+30)                     │
│                                                                 │
│  ⚠️  IMMEDIATE ACTION REQUIRED                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    COLLECTOR TIMEOUT                            │
│                                                                 │
│  WHOIS Collector                                                │
│  • Query sent                                                   │
│  • Timeout after 10s                                            │
│  • Exception caught                                             │
│  • Return: (age_days=None, errors=["WHOIS: timeout"])          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE OBJECT                            │
│                                                                 │
│  age_days: None                       ← No data                │
│  errors: ["WHOIS: timeout"]           ← Failure recorded       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RISK ENGINE                                  │
│                                                                 │
│  • Age rules not triggered (age_days is None)                   │
│  • Failure signal triggered:                                    │
│    ✓ WHOIS lookup failed → +10                                 │
│                                                                 │
│  Failure treated as risk indicator!                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    STARTUP                                      │
│                                                                 │
│  1. Load config/settings.yaml                                   │
│  2. Parse YAML                                                  │
│  3. Validate with Pydantic (ConfigurationSchema)                │
│  4. Check business rules:                                       │
│     • No negative weights                                       │
│     • Thresholds in order                                       │
│     • Critical ≤ 100                                            │
│  5. Cache configuration                                         │
│                                                                 │
│  ✓ Success: Application starts                                  │
│  ✗ Failure: Application exits (fail-fast)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Dependency Injection Flow (API)

```
┌─────────────────────────────────────────────────────────────────┐
│                    API REQUEST                                  │
│                                                                 │
│  POST /api/v1/analyze                                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                  DEPENDENCY INJECTION                           │
│                                                                 │
│  get_config() → ConfigurationSchema                             │
│       ↓                                                         │
│  get_analyzer_service(config) → AnalyzerService                 │
│       ↓                                                         │
│  analyze_domain(request, service)                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    ROUTE HANDLER                                │
│                                                                 │
│  • Validate request (Pydantic)                                  │
│  • Call service.analyze_domain()                                │
│  • Format response                                              │
│  • Return JSON                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Principles Illustrated

1. **Unidirectional Flow**: Data flows in one direction
2. **Pure Core**: Risk Engine has no side effects
3. **Fail-Safe**: Errors don't crash, they inform
4. **Type Safety**: Pydantic validates at boundaries
5. **Separation**: Each layer has single responsibility

---

**This flow ensures predictable, testable, maintainable behavior.**
