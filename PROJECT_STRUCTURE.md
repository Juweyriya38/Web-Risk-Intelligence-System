# Project Structure

```
web-risk-intelligence-system/
│
├── 📁 app/                           # Application source code
│   │
│   ├── 📁 core/                      # ⭐ BUSINESS LOGIC (PURE)
│   │   ├── models.py                 # Pydantic data models (contracts)
│   │   ├── risk_engine.py            # Risk scoring engine (NO I/O)
│   │   ├── validators.py             # Input validation & sanitization
│   │   ├── config_loader.py          # Configuration management
│   │   └── __init__.py
│   │
│   ├── 📁 collectors/                # DATA COLLECTION LAYER
│   │   ├── dns_collector.py          # DNS queries (MX, SPF)
│   │   ├── whois_collector.py        # WHOIS lookups
│   │   ├── ssl_collector.py          # SSL certificate validation
│   │   ├── lexical_analyzer.py       # Keyword/TLD analysis
│   │   └── __init__.py
│   │
│   ├── 📁 services/                  # ORCHESTRATION LAYER
│   │   ├── analyzer_service.py       # Coordinates collectors + engine
│   │   └── __init__.py
│   │
│   ├── 📁 api/                       # REST API INTERFACE
│   │   ├── routes.py                 # FastAPI endpoints
│   │   └── __init__.py
│   │
│   ├── 📁 cli/                       # CLI INTERFACE
│   │   ├── main.py                   # Typer commands
│   │   └── __init__.py
│   │
│   └── __init__.py
│
├── 📁 config/                        # CONFIGURATION
│   └── settings.yaml                 # Risk weights, thresholds, keywords
│
├── 📁 tests/                         # TEST SUITE
│   ├── test_risk_engine.py           # Business logic tests
│   ├── test_validators.py            # Input validation tests
│   ├── test_api.py                   # API endpoint tests
│   └── __init__.py
│
├── 📄 main_cli.py                    # CLI entry point
├── 📄 main_api.py                    # API entry point
│
├── 📄 requirements.txt               # Python dependencies (pip)
├── 📄 pyproject.toml                 # Poetry configuration
│
├── 🐳 Dockerfile                     # Container image definition
├── 🐳 docker-compose.yml             # Container orchestration
├── 📄 .dockerignore                  # Docker build exclusions
│
├── 📄 Makefile                       # Development commands
├── 📄 .pre-commit-config.yaml        # Code quality hooks
├── 📄 .gitignore                     # Git exclusions
├── 📄 .env.example                   # Environment template
│
├── 📖 README.md                      # ⭐ MAIN DOCUMENTATION
├── 📖 QUICKSTART.md                  # 5-minute setup guide
├── 📖 ARCHITECTURE.md                # Architecture decisions
│
└── 📄 LICENSE                        # MIT License

```

## Layer Responsibilities

### 🎯 Core Layer (Pure Business Logic)
**Location:** `app/core/`

**Responsibilities:**
- Risk scoring algorithm
- Data models and contracts
- Input validation
- Configuration schema

**Rules:**
- ✅ NO network calls
- ✅ NO file I/O
- ✅ NO logging
- ✅ NO framework dependencies
- ✅ Pure functions only
- ✅ 100% testable

**Files:**
- `models.py` - Pydantic models (IntelligenceObject, RiskResult, etc.)
- `risk_engine.py` - Risk scoring engine
- `validators.py` - Domain validation
- `config_loader.py` - Configuration loading

---

### 🔍 Collectors Layer
**Location:** `app/collectors/`

**Responsibilities:**
- External data collection
- DNS queries
- WHOIS lookups
- SSL certificate checks
- Lexical analysis

**Rules:**
- ✅ Handle timeouts gracefully
- ✅ Return partial results
- ✅ Never crash the system
- ✅ Treat failures as signals

**Files:**
- `dns_collector.py` - MX/SPF record checks
- `whois_collector.py` - Domain age lookup
- `ssl_collector.py` - Certificate validation
- `lexical_analyzer.py` - Keyword/TLD detection

---

### 🎭 Services Layer (Orchestration)
**Location:** `app/services/`

**Responsibilities:**
- Coordinate collectors
- Invoke risk engine
- Assemble results

**Rules:**
- ✅ NO business logic
- ✅ Orchestration only
- ✅ Shared by CLI and API

**Files:**
- `analyzer_service.py` - Main orchestrator

---

### 🖥️ Interface Layer
**Location:** `app/cli/` and `app/api/`

**Responsibilities:**
- User interaction
- Input/output formatting
- HTTP handling (API)
- Exit codes (CLI)

**Rules:**
- ✅ NO business logic
- ✅ Presentation only
- ✅ Call service layer

**Files:**
- `cli/main.py` - Typer CLI
- `api/routes.py` - FastAPI endpoints

---

## Dependency Flow

```
┌─────────────────────────────────────────┐
│  CLI (Typer)    │    API (FastAPI)      │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         Analyzer Service                │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│  DNS │ WHOIS │ SSL │ Lexical Analyzer   │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│      IntelligenceObject (Contract)      │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│          Risk Engine (Pure)             │
└─────────────────┬───────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────┐
│         RiskResult (Output)             │
└─────────────────────────────────────────┘
```

**Key Principle:** Dependencies always point INWARD toward business logic.

---

## File Purposes

### Entry Points
- `main_cli.py` - Start CLI application
- `main_api.py` - Start API server

### Configuration
- `config/settings.yaml` - Risk weights, thresholds, keywords
- `.env.example` - Environment variable template

### Deployment
- `Dockerfile` - Container image (multi-stage build)
- `docker-compose.yml` - Service orchestration
- `.dockerignore` - Build optimization

### Development
- `Makefile` - Common commands (test, lint, format)
- `.pre-commit-config.yaml` - Git hooks for code quality
- `pyproject.toml` - Poetry dependencies and tool config
- `requirements.txt` - Pip dependencies (alternative)

### Documentation
- `README.md` - Complete documentation
- `QUICKSTART.md` - 5-minute setup
- `ARCHITECTURE.md` - Design decisions
- `LICENSE` - MIT License

### Testing
- `tests/test_risk_engine.py` - Business logic tests
- `tests/test_validators.py` - Input validation tests
- `tests/test_api.py` - API endpoint tests

---

## Adding New Features

### New Risk Signal
1. Add to `IntelligenceObject` in `models.py`
2. Create/update collector in `collectors/`
3. Add weight to `settings.yaml`
4. Add weight field to `RiskWeights` in `models.py`
5. Add evaluation method in `risk_engine.py`
6. Update `analyzer_service.py` to collect signal
7. Add tests

### New Collector
1. Create file in `collectors/`
2. Implement with timeout handling
3. Return tuple of (data, errors)
4. Update `analyzer_service.py`
5. Add tests

### New API Endpoint
1. Add route in `api/routes.py`
2. Use dependency injection
3. Call service layer
4. Add tests in `tests/test_api.py`

---

## Clean Architecture Checklist

When adding code, ensure:

- [ ] Business logic in `core/` has NO I/O
- [ ] Collectors handle timeouts gracefully
- [ ] Service layer has NO business logic
- [ ] Interface layer has NO business logic
- [ ] All data flows through Pydantic models
- [ ] Configuration changes don't require code changes
- [ ] Tests don't require network access (mock collectors)
- [ ] Dependencies point inward

---

**This structure ensures maintainability, testability, and scalability.**
