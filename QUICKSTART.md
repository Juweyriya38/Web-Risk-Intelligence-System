# Quick Start Guide

## 5-Minute Setup

### 1. Install

```bash
# Clone and enter directory
git clone <repo-url>
cd web-risk-intelligence-system

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run

```bash
# Analyze a domain
python main_cli.py analyze example.com

# Get JSON output
python main_cli.py analyze suspicious-site.tk --json

# Start API server
python main_api.py
# Visit http://localhost:8000/docs
```

### 3. Test

```bash
pytest
```

## Common Commands

```bash
# CLI with verbose logging
python main_cli.py analyze example.com --verbose

# CLI with custom config
python main_cli.py analyze example.com --config custom.yaml

# API with curl
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# Docker
docker-compose up -d
```

## Exit Codes

- `0` = Low/Medium risk
- `1` = High/Critical risk
- `2` = Error

## Configuration

Edit `config/settings.yaml` to tune:
- Risk weights
- Thresholds
- Keywords
- TLDs

## Architecture

```
CLI/API → Service → Collectors → Risk Engine
                                     ↑
                              Configuration
```

**Key principle:** Business logic (Risk Engine) is pure - no I/O, no side effects.

## Need Help?

- Full docs: See `README.md`
- API docs: http://localhost:8000/docs
- Tests: `pytest -v`
