# Web Risk Intelligence System

> **Production-grade domain threat assessment platform with clean architecture**

A deterministic, explainable risk scoring engine that evaluates domain infrastructure signals to identify potential phishing, impersonation, and malicious domains.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📚 Documentation Navigation

**New to the project?** Start with [QUICKSTART.md](QUICKSTART.md) for 5-minute setup.

**Complete Documentation:**
- 📖 [INDEX.md](INDEX.md) - Documentation index and navigation
- 🚀 [QUICKSTART.md](QUICKSTART.md) - 5-minute setup guide
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Design decisions and rationale
- 📁 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - File organization and layers
- 🔄 [FLOW_DIAGRAM.md](FLOW_DIAGRAM.md) - System flow and data processing
- 📊 [SUMMARY.md](SUMMARY.md) - Project overview and achievements
- ✅ [COMPLETION_CHECKLIST.md](COMPLETION_CHECKLIST.md) - Verification checklist

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Risk Scoring Model](#-risk-scoring-model)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Security](#-security)
- [Development](#-development)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🎯 Overview

### What It Does

The Web Risk Intelligence System performs **infrastructure-level threat assessment** of domains by:

1. **Collecting** public intelligence signals (DNS, WHOIS, SSL, lexical patterns)
2. **Analyzing** signals using configurable weighted heuristics
3. **Scoring** risk on a 0-100 scale with deterministic logic
4. **Classifying** domains as Low, Medium, High, or Critical risk
5. **Explaining** every score with detailed justifications

### What It Is NOT

- ❌ Not a vulnerability scanner
- ❌ Not a malware sandbox
- ❌ Not a machine learning black box
- ❌ Not a content analyzer

### Use Cases

- **Security Operations**: Rapid triage of suspicious domains
- **Threat Intelligence**: Infrastructure-based threat profiling
- **Phishing Detection**: Identify disposable/impersonation domains
- **Brand Protection**: Detect typosquatting and homograph attacks
- **Incident Response**: Fast risk assessment during investigations

---

## 🏗️ Architecture

### Clean Architecture Principles

This system strictly follows **Clean Architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    INTERFACE LAYER                          │
│  ┌──────────────────┐         ┌──────────────────┐         │
│  │   CLI (Typer)    │         │  API (FastAPI)   │         │
│  │  - Presentation  │         │  - REST Routes   │         │
│  │  - Exit codes    │         │  - HTTP handling │         │
│  └──────────────────┘         └──────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Analyzer Service                        │  │
│  │  - Coordinates collectors                            │  │
│  │  - Invokes risk engine                               │  │
│  │  - No business logic                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   COLLECTION LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   DNS    │  │  WHOIS   │  │   SSL    │  │ Lexical  │   │
│  │Collector │  │Collector │  │Collector │  │ Analyzer │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  - External I/O with timeouts                               │
│  - Graceful failure handling                                │
│  - Return partial results                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA CONTRACT LAYER                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           IntelligenceObject (Pydantic)              │  │
│  │  - Standardized data structure                       │  │
│  │  - Type-safe contract                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER (PURE)                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  Risk Engine                         │  │
│  │  ✓ Pure functions (no side effects)                 │  │
│  │  ✓ No I/O operations                                │  │
│  │  ✓ No external dependencies                         │  │
│  │  ✓ Deterministic scoring                            │  │
│  │  ✓ 100% testable                                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  CONFIGURATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              settings.yaml                           │  │
│  │  - Risk weights                                      │  │
│  │  - Thresholds                                        │  │
│  │  - Keywords & TLDs                                   │  │
│  │  - Validated at startup (fail-fast)                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
web-risk-intelligence-system/
│
├── app/                          # Application code
│   ├── core/                     # Business logic (pure)
│   │   ├── models.py             # Pydantic data models
│   │   ├── risk_engine.py        # Risk scoring engine (PURE)
│   │   ├── validators.py         # Input validation
│   │   └── config_loader.py      # Configuration management
│   │
│   ├── collectors/               # External data collection
│   │   ├── dns_collector.py      # DNS queries (MX, SPF)
│   │   ├── whois_collector.py    # Domain registration data
│   │   ├── ssl_collector.py      # SSL certificate validation
│   │   └── lexical_analyzer.py   # Keyword/TLD analysis
│   │
│   ├── services/                 # Orchestration layer
│   │   └── analyzer_service.py   # Coordinates collection + scoring
│   │
│   ├── api/                      # REST API interface
│   │   └── routes.py             # FastAPI endpoints
│   │
│   └── cli/                      # CLI interface
│       └── main.py               # Typer commands
│
├── config/                       # Configuration
│   └── settings.yaml             # Risk weights, thresholds, keywords
│
├── tests/                        # Test suite
│   ├── test_risk_engine.py       # Business logic tests
│   ├── test_validators.py        # Input validation tests
│   └── test_api.py               # API endpoint tests
│
├── main_cli.py                   # CLI entry point
├── main_api.py                   # API entry point
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Poetry configuration
├── Dockerfile                    # Container image
├── docker-compose.yml            # Container orchestration
└── Makefile                      # Development commands
```

### Key Design Decisions

#### 1. **Pure Business Logic**
The `RiskEngine` is completely isolated:
- ✅ No network calls
- ✅ No file I/O
- ✅ No logging
- ✅ No framework dependencies
- ✅ Accepts data, returns data
- ✅ 100% deterministic and testable

#### 2. **Dependency Direction**
```
CLI/API → Service → Collectors → Models ← Risk Engine
                                    ↑
                              Configuration
```
- Business logic never depends on infrastructure
- All dependencies point inward
- Easy to swap implementations

#### 3. **Fail-Safe Collectors**
- All external calls have timeouts
- Partial results are valid
- Failures treated as intelligence signals
- Never crash the system

#### 4. **Configuration-Driven**
- All weights externalized to YAML
- Validated at startup (fail-fast)
- No magic numbers in code
- Tunable without code changes

---

## ✨ Features

### Core Capabilities

- ✅ **Deterministic Scoring**: Same input always produces same output
- ✅ **Explainable Results**: Every score includes detailed justifications
- ✅ **Configurable Weights**: Tune risk scoring without code changes
- ✅ **Graceful Degradation**: Partial results on collector failures
- ✅ **Type Safety**: Pydantic models enforce data contracts
- ✅ **Dual Interface**: CLI (primary) and REST API (secondary)
- ✅ **Production Ready**: Docker, health checks, structured logging

### Intelligence Signals

| Category | Signals |
|----------|---------|
| **Infrastructure** | Domain age, MX records, SPF records, SSL validity, Self-signed certs |
| **Behavioral** | Suspicious keywords, High-risk TLDs, Punycode detection |
| **Failure** | WHOIS timeouts, DNS failures, SSL errors |

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- pip or Poetry
- Docker (optional, for containerized deployment)

### Option 1: Using pip (Recommended for Quick Start)

```bash
# Clone repository
git clone <repository-url>
cd web-risk-intelligence-system

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Using Poetry (Recommended for Development)

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Option 3: Using Docker

```bash
# Build image
docker build -t risk-intelligence:latest .

# Run with docker-compose
docker-compose up -d
```

### Verify Installation

```bash
# CLI
python main_cli.py analyze --help

# API (in separate terminal)
python main_api.py
# Visit http://localhost:8000/docs
```

---

## 💻 Usage

### CLI Interface (Primary)

The CLI is the primary interface for interactive use and scripting.

#### Basic Analysis

```bash
python main_cli.py analyze example.com
```

**Output:**
```
Domain Risk Assessment: example.com

Risk Score: 0/100 (LOW)

Intelligence Summary
┌─────────────────┬───────────┐
│ Signal          │ Value     │
├─────────────────┼───────────┤
│ Domain Age      │ 9000 days │
│ MX Records      │ ✓         │
│ SPF Records     │ ✓         │
│ Valid SSL       │ ✓         │
└─────────────────┴───────────┘
```

#### JSON Output

```bash
python main_cli.py analyze suspicious-login.tk --json
```

**Output:**
```json
{
  "domain": "suspicious-login.tk",
  "score": 85,
  "classification": "Critical",
  "triggered_rules": [
    {
      "rule": "domain_age_very_new",
      "triggered": true,
      "weight": 25,
      "justification": "Domain registered 3 days ago (< 7 days)"
    },
    {
      "rule": "no_mx_records",
      "triggered": true,
      "weight": 15,
      "justification": "No MX records found (no email infrastructure)"
    }
  ],
  "intelligence": {
    "age_days": 3,
    "has_mx": false,
    "has_spf": false,
    "ssl_valid": false,
    "risky_tld": true,
    "triggered_keywords": ["login"]
  }
}
```

#### Verbose Mode

```bash
python main_cli.py analyze example.com --verbose
```

Shows detailed logging including collector operations and timing.

#### Custom Configuration

```bash
python main_cli.py analyze example.com --config /path/to/custom-settings.yaml
```

#### Exit Codes

The CLI returns meaningful exit codes for scripting:

- **0**: Low or Medium risk (safe to proceed)
- **1**: High or Critical risk (requires attention)
- **2**: Error occurred (invalid input, system error)

**Example Script:**
```bash
#!/bin/bash
python main_cli.py analyze "$1" --json > result.json
EXIT_CODE=$?

if [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️  HIGH RISK DOMAIN DETECTED"
    # Send alert, block domain, etc.
elif [ $EXIT_CODE -eq 2 ]; then
    echo "❌ Analysis failed"
fi
```

### API Interface (Secondary)

The REST API is ideal for integration with other systems.

#### Start Server

```bash
# Development
uvicorn main_api:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main_api:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Analyze Domain

```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'
```

**Response:**
```json
{
  "domain": "example.com",
  "score": 0,
  "classification": "Low",
  "triggered_rules": [],
  "intelligence": {
    "age_days": 9000,
    "has_mx": true,
    "has_spf": true,
    "ssl_valid": true,
    "is_self_signed": false,
    "triggered_keywords": [],
    "risky_tld": false,
    "is_punycode": false,
    "errors": []
  }
}
```

#### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

**Response:**
```json
{"status": "healthy"}
```

#### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

## ⚙️ Configuration

### Configuration File: `config/settings.yaml`

All risk scoring parameters are externalized for easy tuning.

```yaml
# Risk weights (contribute to max score of 100)
risk_weights:
  domain_age_very_new: 25      # < 7 days
  domain_age_new: 15           # < 30 days
  domain_age_recent: 8         # < 90 days
  no_mx_records: 15
  no_spf_records: 10
  ssl_invalid: 20
  ssl_self_signed: 15
  risky_tld: 20
  suspicious_keyword: 15       # per keyword (max 2)
  punycode_detected: 25
  whois_lookup_failed: 10
  dns_resolution_failed: 15

# Risk classification thresholds
risk_thresholds:
  low: 0        # 0-29
  medium: 30    # 30-59
  high: 60      # 60-79
  critical: 80  # 80-100

# High-risk TLDs (abuse-prone)
risky_tlds:
  - .tk
  - .ml
  - .xyz
  - .top
  - .club
  # ... more

# Suspicious keywords (phishing indicators)
suspicious_keywords:
  - login
  - signin
  - account
  - verify
  - secure
  - banking
  # ... more

# Collector timeouts (seconds)
timeouts:
  dns: 5
  whois: 10
  ssl: 10
```

### Configuration Validation

The system validates configuration at startup:

- ✅ No negative weights
- ✅ Thresholds in ascending order
- ✅ Critical threshold ≤ 100
- ✅ All required fields present

**Invalid configuration causes immediate failure** (fail-fast principle).

### Tuning Guidelines

1. **Increase weight** for signals you consider more critical
2. **Adjust thresholds** based on your risk tolerance
3. **Add keywords** specific to your brand/industry
4. **Add TLDs** based on observed abuse patterns
5. **Test changes** with known good/bad domains

---

## 📊 Risk Scoring Model

### Scoring Formula

```
Risk Score = Σ(weight × triggered_signal)
Capped at 100
```

### Example Calculation

**Domain:** `secure-login.tk` (3 days old)

| Signal | Triggered | Weight | Contribution |
|--------|-----------|--------|--------------|
| Domain age < 7 days | ✓ | 25 | +25 |
| No MX records | ✓ | 15 | +15 |
| No SPF records | ✓ | 10 | +10 |
| SSL invalid | ✓ | 20 | +20 |
| Risky TLD (.tk) | ✓ | 20 | +20 |
| Keyword: "login" | ✓ | 15 | +15 |
| **Total** | | | **105 → 100** |

**Classification:** Critical (≥80)

### Risk Classifications

| Level | Score Range | Interpretation | Action |
|-------|-------------|----------------|--------|
| **Low** | 0-29 | Minimal risk indicators | Monitor |
| **Medium** | 30-59 | Some concerning signals | Investigate |
| **High** | 60-79 | Multiple risk indicators | Block/Alert |
| **Critical** | 80-100 | Severe risk profile | Immediate action |

### Pattern Detection

Beyond individual signals, the engine recognizes composite patterns:

#### Ghost Pattern
- Domain age < 7 days
- No MX records
- **Indicates:** Disposable/automated registration

#### Authority Pattern
- Login-related keywords
- Valid SSL certificate
- **Indicates:** Phishing landing page

#### Homograph Pattern
- Punycode (xn--) detected
- **Indicates:** Character spoofing attack

---

## 🔌 API Reference

### Endpoints

#### POST `/api/v1/analyze`

Analyze a domain for risk indicators.

**Request:**
```json
{
  "domain": "example.com"
}
```

**Response:** `200 OK`
```json
{
  "domain": "example.com",
  "score": 0,
  "classification": "Low",
  "triggered_rules": [],
  "intelligence": { ... }
}
```

**Error Responses:**
- `400 Bad Request`: Invalid domain format
- `500 Internal Server Error`: System error

#### GET `/api/v1/health`

Health check endpoint.

**Response:** `200 OK`
```json
{
  "status": "healthy"
}
```

#### GET `/`

Root endpoint with service information.

**Response:** `200 OK`
```json
{
  "service": "Web Risk Intelligence System",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 🧪 Testing

### Run Tests

```bash
# All tests with coverage
pytest --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_risk_engine.py

# Verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

### Test Coverage

The test suite includes:

- ✅ **Unit tests** for risk engine logic
- ✅ **Boundary condition tests** for thresholds
- ✅ **Input validation tests** for sanitization
- ✅ **API endpoint tests** with TestClient
- ✅ **Configuration validation tests**

**Target coverage:** 80%+

### Example Test

```python
def test_high_risk_new_domain(risk_engine):
    """Test newly registered domain with minimal infrastructure."""
    intel = IntelligenceObject(
        domain="suspicious-login.tk",
        age_days=3,
        has_mx=False,
        has_spf=False,
        ssl_valid=False,
        triggered_keywords=["login"],
        risky_tld=True,
    )

    result = risk_engine.evaluate(intel)

    assert result.score >= 80
    assert result.classification == "Critical"
```

---

## 🐳 Deployment

### Docker Deployment

#### Build Image

```bash
docker build -t risk-intelligence:latest .
```

#### Run Container

```bash
# API mode
docker run -d \
  -p 8000:8000 \
  --name risk-api \
  risk-intelligence:latest

# CLI mode
docker run --rm \
  risk-intelligence:latest \
  python main_cli.py analyze example.com
```

#### Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Considerations

#### Environment Variables

Create `.env` file:

```bash
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

#### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name risk-api.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Systemd Service

```ini
[Unit]
Description=Risk Intelligence API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/risk-intelligence
ExecStart=/opt/risk-intelligence/venv/bin/uvicorn main_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Monitoring

- **Health checks**: `/api/v1/health`
- **Metrics**: Integrate with Prometheus/Grafana
- **Logging**: Structured JSON logs to stdout
- **Alerts**: Monitor error rates and response times

---

## 🔒 Security

### Input Validation

- ✅ RFC-compliant domain regex
- ✅ Length validation (max 253 chars)
- ✅ Protocol/path stripping
- ✅ Punycode detection
- ✅ No SQL injection risk (no database)

### Timeout Protection

All external calls have strict timeouts:
- DNS: 5 seconds
- WHOIS: 10 seconds
- SSL: 10 seconds

### Error Handling

- ✅ No stack traces exposed (unless verbose mode)
- ✅ Graceful degradation on failures
- ✅ Partial results always valid
- ✅ All errors logged

### Deployment Security

- ✅ Non-root Docker user
- ✅ No secrets in repository
- ✅ Environment variable support
- ✅ CORS configurable
- ✅ Rate limiting ready (add middleware)

### Threat Model

**Adversary behaviors detected:**
1. Rapid domain registration cycles
2. Abuse-prone TLD selection
3. Infrastructure minimalism
4. Brand impersonation via keywords
5. WHOIS obfuscation
6. Homograph spoofing

**System limitations:**
- Not real-time (relies on public data)
- Heuristic-based (may have false positives)
- No content analysis
- No reputation data (yet)

---

## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

### Code Quality Tools

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking
mypy app/

# Run all checks
make all
```

### Makefile Commands

```bash
make install      # Install dependencies
make test         # Run tests with coverage
make lint         # Run linter
make format       # Format code
make type-check   # Run type checker
make clean        # Clean cache files
make run-cli      # Run CLI (DOMAIN=example.com)
make run-api      # Run API server
make docker-build # Build Docker image
```

### Adding New Collectors

1. Create collector in `app/collectors/`
2. Implement timeout handling
3. Return tuple of (data, errors)
4. Update `AnalyzerService` to call collector
5. Update `IntelligenceObject` model
6. Add tests

### Adding New Risk Rules

1. Add weight to `config/settings.yaml`
2. Add weight field to `RiskWeights` model
3. Implement evaluation method in `RiskEngine`
4. Add tests for new rule
5. Update documentation

---

## 🗺️ Roadmap

### Phase 1: Core Enhancement (Q2 2024)
- [ ] ASN reputation scoring
- [ ] Brand similarity detection (Levenshtein)
- [ ] Historical domain monitoring
- [ ] Entropy-based scoring

### Phase 2: Integration (Q3 2024)
- [ ] VirusTotal integration
- [ ] Shodan integration
- [ ] URLScan.io integration
- [ ] Threat intelligence feeds

### Phase 3: Scalability (Q4 2024)
- [ ] Redis caching layer
- [ ] PostgreSQL persistence
- [ ] Batch analysis API
- [ ] Async collectors

### Phase 4: Enterprise (2025)
- [ ] Authentication & authorization
- [ ] Rate limiting
- [ ] Webhook notifications
- [ ] Multi-tenancy
- [ ] Custom rule engine
- [ ] ML-based scoring (optional)

---

## 📄 License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:

1. ✅ All tests pass (`pytest`)
2. ✅ Code is formatted (`black`)
3. ✅ Code is linted (`ruff`)
4. ✅ Type hints present (`mypy`)
5. ✅ Documentation updated
6. ✅ Clean architecture maintained

### Contribution Guidelines

- Keep business logic pure (no side effects)
- Maintain separation of concerns
- Add tests for new features
- Update configuration schema if needed
- Follow existing code style

---

## 📧 Support

- **Issues**: Open a GitHub issue
- **Questions**: Use GitHub Discussions
- **Security**: Report privately to security@example.com

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation
- [dnspython](https://www.dnspython.org/) - DNS toolkit
- [python-whois](https://github.com/richardpenman/whois) - WHOIS client

---

**Built with clean architecture principles for production deployment.**

*Last updated: 2024*
