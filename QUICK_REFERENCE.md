# 🚀 Quick Reference - Web Risk Intelligence System

## Instant Commands

### CLI Usage
```bash
# Activate environment
source venv/bin/activate

# Analyze domain (JSON)
python main_cli.py analyze suspicious-login.tk --json

# Analyze domain (human-readable)
python main_cli.py analyze example.com

# Help
python main_cli.py analyze --help
```

### API Usage
```bash
# Start server
uvicorn main_api:app --reload --port 8001

# Test with curl
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-login.tk"}'

# Health check
curl http://localhost:8001/health

# Swagger UI
open http://localhost:8001/docs
```

### Test Scripts
```bash
# Test CLI
./test_refactored_cli.sh

# Test API (server must be running)
./test_refactored_api.sh
```

---

## Output Format

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

---

## Risk Levels

| Score | Level | Action |
|-------|-------|--------|
| 0-39 | Low | Monitor |
| 40-69 | Medium | Investigate |
| 70-100 | Critical | Block/Alert |

---

## Core Function

```python
from app.core.engine import analyze_domain

result = analyze_domain("example.com")
# Returns: dict with score, risk_level, reasons, etc.
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /analyze | Analyze domain |
| GET | /health | Health check |
| GET | / | Service info |
| GET | /docs | Swagger UI |

---

## Example Domains

**Critical Risk:**
- suspicious-login.tk (score: 80)
- verify-account.xyz (score: 95)
- secure-banking.ml (score: 85)

**Low Risk:**
- example.com (score: 0)
- google.com (score: 0)
- github.com (score: 0)

---

## Files

| File | Purpose |
|------|---------|
| `app/core/engine.py` | Core analysis logic |
| `app/api/main.py` | FastAPI service |
| `main_cli.py` | CLI entry point |
| `main_api.py` | API entry point |
| `REFACTORED_README.md` | Full documentation |
| `IMPLEMENTATION_SUMMARY.md` | Implementation details |

---

## Dependencies

```bash
pip install typer rich fastapi uvicorn pydantic
```

---

## Quick Demo

```bash
# Terminal 1: Start API
uvicorn main_api:app --port 8001

# Terminal 2: Test CLI
python main_cli.py analyze suspicious-login.tk --json

# Terminal 3: Test API
curl -X POST "http://localhost:8001/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-login.tk"}'
```

---

**Ready to use! 🎉**
