# Web Risk Intelligence System - Refactored

Production-ready domain threat assessment with modular engine architecture.

## 🎯 Quick Start

### 1. Install Dependencies
```bash
source venv/bin/activate
pip install typer rich fastapi uvicorn pydantic
```

### 2. Test CLI
```bash
# JSON output
python main_cli.py analyze suspicious-login.tk --json

# Human-readable output
python main_cli.py analyze example.com
```

### 3. Start API Server
```bash
uvicorn main_api:app --reload --port 8001
```

### 4. Test API
```bash
# Using curl
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-login.tk"}'

# Access Swagger UI
open http://localhost:8001/docs
```

---

## 📊 Output Format

Both CLI (with `--json`) and API return identical structure:

```json
{
  "domain": "suspicious-login.tk",
  "score": 80,
  "risk_level": "Critical",
  "reasons": [
    "New domain (< 7 days)",
    "Suspicious keywords: login",
    "High-risk TLD: .tk",
    "Invalid SSL certificate"
  ],
  "domain_age_days": 5,
  "ssl_valid": false,
  "ssl_expires_in_days": 0
}
```

### Risk Levels
- **Low**: score < 40
- **Medium**: 40 ≤ score < 70
- **Critical**: score ≥ 70

---

## 🏗️ Architecture

### Modular Design
```
app/
├── core/
│   └── engine.py          # Core analyze_domain() function
├── api/
│   └── main.py            # FastAPI wrapper
main_cli.py                # CLI wrapper
main_api.py                # API entry point
```

### Key Function: `analyze_domain()`

Located in `app/core/engine.py`, this is the **single source of truth** for risk analysis:

```python
from app.core.engine import analyze_domain

result = analyze_domain("example.com")
# Returns: dict with score, risk_level, reasons, etc.
```

**Used by:**
- ✅ CLI (`main_cli.py`)
- ✅ FastAPI (`app/api/main.py`)
- ✅ Future integrations (webhooks, batch processing, etc.)

---

## 🔍 Risk Scoring Logic

### Scoring Rules

| Signal | Points | Trigger |
|--------|--------|---------|
| Very new domain (< 7 days) | +30 | Domain age |
| Recent domain (< 30 days) | +20 | Domain age |
| No MX record | +20 | DNS check |
| Suspicious keywords | +15 each (max 2) | Lexical analysis |
| High-risk TLD | +15 | TLD check |
| Invalid SSL | +20 | SSL check |
| SSL expires soon (< 30 days) | +10 | SSL check |

**Total capped at 100**

### Detection Patterns

**Suspicious Keywords:**
- login, signin, account, verify, secure, banking
- paypal, amazon, update, confirm, password, wallet

**High-Risk TLDs:**
- .tk, .ml, .ga, .cf, .gq, .xyz, .top, .club

---

## 🧪 Testing

### CLI Tests
```bash
# Critical risk domain
python main_cli.py analyze suspicious-login.tk --json

# Low risk domain
python main_cli.py analyze example.com --json

# Medium risk domain
python main_cli.py analyze new-site-verify.com --json
```

### API Tests
```bash
# Start server
uvicorn main_api:app --port 8001 &

# Test endpoints
curl http://localhost:8001/health
curl http://localhost:8001/

# Analyze domain
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-login.tk"}'
```

### Expected Results

**suspicious-login.tk** → Score: 80, Level: Critical
- Reasons: New domain, suspicious keyword "login", risky TLD .tk, invalid SSL

**example.com** → Score: 0, Level: Low
- Reasons: No significant risk indicators

---

## 📡 API Reference

### Endpoints

#### `POST /analyze`
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
  "risk_level": "Low",
  "reasons": ["No significant risk indicators"],
  "domain_age_days": 3650,
  "ssl_valid": true,
  "ssl_expires_in_days": 90
}
```

**Error:** `400 Bad Request`
```json
{
  "detail": "Invalid domain format"
}
```

#### `GET /health`
Health check endpoint.

**Response:** `200 OK`
```json
{
  "status": "healthy"
}
```

#### `GET /`
Service information.

**Response:** `200 OK`
```json
{
  "service": "Web Risk Intelligence API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

## 🚀 Deployment

### Local Development
```bash
# CLI
python main_cli.py analyze <domain> --json

# API
uvicorn main_api:app --reload --port 8001
```

### Production
```bash
# API with workers
uvicorn main_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```bash
docker build -t risk-intelligence .
docker run -p 8000:8000 risk-intelligence
```

---

## 🔧 Configuration

### Mock Data Behavior

The engine uses **deterministic mock data** for demo purposes:

- **Domain Age**: Based on domain length and keywords
- **MX Records**: Well-known domains have MX
- **SSL**: Valid for established domains
- **Expiry**: 365 days for long domains, 90 for short

### Customization

Edit `app/core/engine.py` to:
- Adjust scoring weights
- Add/remove suspicious keywords
- Modify risk thresholds
- Add new detection rules

---

## 📝 Example Usage

### Python Integration
```python
from app.core.engine import analyze_domain

# Analyze domain
result = analyze_domain("suspicious-login.tk")

print(f"Domain: {result['domain']}")
print(f"Risk: {result['risk_level']} ({result['score']}/100)")
print(f"Reasons: {', '.join(result['reasons'])}")
```

### Batch Processing
```python
domains = ["example.com", "suspicious-login.tk", "test-verify.xyz"]

for domain in domains:
    result = analyze_domain(domain)
    if result['risk_level'] == 'Critical':
        print(f"⚠️  {domain}: {result['score']}/100")
```

---

## 🎓 Key Features

✅ **Modular Engine**: Single `analyze_domain()` function  
✅ **Dual Interface**: CLI + REST API  
✅ **Deterministic**: Same input = same output  
✅ **Explainable**: Every score includes reasons  
✅ **Mock Data**: No blocking network calls  
✅ **Production Ready**: Pydantic validation, error handling  
✅ **Swagger UI**: Interactive API documentation  

---

## 🔮 Future Enhancements

- [ ] Real DNS/WHOIS/SSL checks (with caching)
- [ ] Database persistence
- [ ] Batch analysis endpoint
- [ ] Webhook notifications
- [ ] Rate limiting
- [ ] Authentication
- [ ] Historical tracking
- [ ] ML-based scoring

---

## 📄 License

MIT License - See LICENSE file

---

**Built with Python 3.11 | FastAPI | Typer**
