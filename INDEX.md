# 📚 Documentation Index

Welcome to the Web Risk Intelligence System documentation!

---

## 🚀 Getting Started

**New to the project? Start here:**

1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
   - Installation
   - First analysis
   - Basic commands

2. **[README.md](README.md)** - Complete documentation
   - Full feature overview
   - Detailed usage examples
   - Configuration guide
   - API reference

---

## 🏗️ Understanding the System

**Learn about the architecture:**

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Design decisions
   - Why clean architecture?
   - Key architectural choices
   - Trade-offs and rationale

4. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - File organization
   - Directory layout
   - Layer responsibilities
   - Where to add new features

5. **[FLOW_DIAGRAM.md](FLOW_DIAGRAM.md)** - System flow
   - Request processing
   - Data flow visualization
   - Error handling

---

## 📖 Reference Documentation

### Core Concepts

- **Clean Architecture**: Business logic isolated from infrastructure
- **Pure Functions**: Risk engine has zero side effects
- **Fail-Safe Design**: Collectors handle errors gracefully
- **Configuration-Driven**: All weights in YAML

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Risk Engine | `app/core/risk_engine.py` | Pure business logic |
| Collectors | `app/collectors/` | External data gathering |
| Service | `app/services/analyzer_service.py` | Orchestration |
| CLI | `app/cli/main.py` | Command-line interface |
| API | `app/api/routes.py` | REST endpoints |

---

## 💻 Usage Guides

### CLI Usage

```bash
# Basic analysis
python main_cli.py analyze example.com

# JSON output
python main_cli.py analyze example.com --json

# Verbose mode
python main_cli.py analyze example.com --verbose

# Custom config
python main_cli.py analyze example.com --config custom.yaml
```

**Exit Codes:**
- `0` = Low/Medium risk
- `1` = High/Critical risk
- `2` = Error

### API Usage

```bash
# Start server
uvicorn main_api:app --reload

# Analyze domain
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# Health check
curl http://localhost:8000/api/v1/health
```

**Interactive Docs:** http://localhost:8000/docs

---

## ⚙️ Configuration

### Main Configuration File

**Location:** `config/settings.yaml`

**Contains:**
- Risk weights for each signal
- Classification thresholds
- Suspicious keyword list
- High-risk TLD list
- Collector timeouts

**Example:**
```yaml
risk_weights:
  domain_age_very_new: 25
  no_mx_records: 15
  risky_tld: 20

risk_thresholds:
  low: 0
  medium: 30
  high: 60
  critical: 80
```

### Environment Variables

**Location:** `.env` (copy from `.env.example`)

```bash
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test
pytest tests/test_risk_engine.py -v
```

**Test Files:**
- `tests/test_risk_engine.py` - Business logic tests
- `tests/test_validators.py` - Input validation tests
- `tests/test_api.py` - API endpoint tests

---

## 🐳 Deployment

### Docker

```bash
# Build image
docker build -t risk-intelligence:latest .

# Run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Production

See [README.md - Deployment](README.md#-deployment) for:
- Reverse proxy setup (Nginx)
- Systemd service
- Monitoring
- Security considerations

---

## 🛠️ Development

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type check
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
```

---

## 📊 Risk Scoring

### Formula

```
Risk Score = Σ(weight × triggered_signal)
Capped at 100
```

### Signals

| Category | Signals |
|----------|---------|
| **Infrastructure** | Domain age, MX records, SPF records, SSL validity, Self-signed certs |
| **Behavioral** | Suspicious keywords, High-risk TLDs, Punycode detection |
| **Failure** | WHOIS timeouts, DNS failures, SSL errors |

### Classifications

- **Low** (0-29): Minimal risk indicators
- **Medium** (30-59): Some concerning signals
- **High** (60-79): Multiple risk indicators
- **Critical** (80-100): Severe risk profile

---

## 🔧 Extending the System

### Add New Risk Signal

1. Update `IntelligenceObject` in `app/core/models.py`
2. Create/update collector in `app/collectors/`
3. Add weight to `config/settings.yaml`
4. Add weight field to `RiskWeights` in `app/core/models.py`
5. Add evaluation method in `app/core/risk_engine.py`
6. Update `app/services/analyzer_service.py`
7. Add tests

### Add New Collector

1. Create file in `app/collectors/`
2. Implement with timeout handling
3. Return tuple of (data, errors)
4. Update `AnalyzerService`
5. Add tests

### Add New API Endpoint

1. Add route in `app/api/routes.py`
2. Use dependency injection
3. Call service layer
4. Add tests

---

## 🔒 Security

### Input Validation
- RFC-compliant domain regex
- Length validation
- Protocol/path stripping
- Punycode detection

### Timeout Protection
- DNS: 5 seconds
- WHOIS: 10 seconds
- SSL: 10 seconds

### Error Handling
- No stack traces exposed (unless verbose)
- Graceful degradation
- Partial results valid

### Deployment Security
- Non-root Docker user
- No secrets in repository
- Environment variable support
- CORS configurable

---

## 🗺️ Roadmap

### Phase 1: Core Enhancement
- [ ] ASN reputation scoring
- [ ] Brand similarity detection
- [ ] Historical monitoring

### Phase 2: Integration
- [ ] VirusTotal integration
- [ ] Shodan integration
- [ ] Threat intelligence feeds

### Phase 3: Scalability
- [ ] Redis caching
- [ ] PostgreSQL persistence
- [ ] Batch analysis API

### Phase 4: Enterprise
- [ ] Authentication
- [ ] Rate limiting
- [ ] Webhooks
- [ ] Multi-tenancy

---

## 📧 Support

- **Documentation Issues**: Check this index
- **Bug Reports**: Open GitHub issue
- **Feature Requests**: Open GitHub issue
- **Questions**: GitHub Discussions

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🎯 Quick Links

| Document | Purpose | Audience |
|----------|---------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5-min setup | New users |
| [README.md](README.md) | Complete docs | All users |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Design decisions | Developers |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | File organization | Developers |
| [FLOW_DIAGRAM.md](FLOW_DIAGRAM.md) | System flow | Developers |
| [SUMMARY.md](SUMMARY.md) | Project overview | Stakeholders |

---

**Last Updated:** 2024

**Version:** 1.0.0

**Status:** ✅ Production Ready
