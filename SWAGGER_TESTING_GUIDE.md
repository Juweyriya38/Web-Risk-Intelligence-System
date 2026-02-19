# Swagger/OpenAPI Testing Guide

> **Comprehensive guide for testing the Web Risk Intelligence System API using Swagger UI**

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Accessing Swagger UI](#-accessing-swagger-ui)
- [API Endpoints Overview](#-api-endpoints-overview)
- [Test Scenarios](#-test-scenarios)
- [Expected Results](#-expected-results)
- [Error Testing](#-error-testing)
- [Advanced Testing](#-advanced-testing)
- [Automation Scripts](#-automation-scripts)

---

## 🚀 Quick Start

### 1. Start the API Server

```bash
# Option 1: Direct Python
python main_api.py

# Option 2: Uvicorn with reload
uvicorn main_api:app --reload --host 0.0.0.0 --port 8000

# Option 3: Docker
docker-compose up -d
```

### 2. Access Swagger UI

Open your browser and navigate to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🌐 Accessing Swagger UI

### Swagger UI Interface

The Swagger UI provides an interactive interface with:

1. **Endpoint List**: All available API endpoints
2. **Try it out**: Interactive testing buttons
3. **Request Body**: JSON input fields
4. **Execute**: Send requests to the API
5. **Response**: View status codes, headers, and body
6. **Schemas**: Data model definitions

### Navigation

```
http://localhost:8000/docs
├── GET  /                    # Root endpoint
├── GET  /api/v1/health       # Health check
└── POST /api/v1/analyze      # Domain analysis (main endpoint)
```

---

## 📡 API Endpoints Overview

### 1. Root Endpoint

**GET /** - Service information

**Expected Response:**
```json
{
  "service": "Web Risk Intelligence System",
  "version": "1.0.0",
  "docs": "/docs"
}
```

### 2. Health Check

**GET /api/v1/health** - System health status

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### 3. Domain Analysis (Main Endpoint)

**POST /api/v1/analyze** - Analyze domain for risk

**Request Schema:**
```json
{
  "domain": "string"
}
```

**Response Schema:**
```json
{
  "domain": "string",
  "score": 0,
  "classification": "string",
  "triggered_rules": [
    {
      "rule": "string",
      "triggered": true,
      "weight": 0,
      "justification": "string"
    }
  ],
  "intelligence": {
    "age_days": 0,
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

---

## 🧪 Test Scenarios

### Scenario 1: Low Risk Domain (Legitimate)

**Test Case:** Analyze a well-established, legitimate domain

**Steps in Swagger UI:**
1. Click on **POST /api/v1/analyze**
2. Click **Try it out**
3. Enter request body:
```json
{
  "domain": "google.com"
}
```
4. Click **Execute**

**Expected Result:**
- Status Code: `200 OK`
- Score: `0-29`
- Classification: `"Low"`
- Triggered Rules: Empty or minimal

**Sample Response:**
```json
{
  "domain": "google.com",
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

---

### Scenario 2: Medium Risk Domain

**Test Case:** Domain with some concerning signals

**Request:**
```json
{
  "domain": "example-shop.xyz"
}
```

**Expected Result:**
- Status Code: `200 OK`
- Score: `30-59`
- Classification: `"Medium"`
- Triggered Rules: Risky TLD (.xyz)

---

### Scenario 3: High Risk Domain (Suspicious)

**Test Case:** Recently registered domain with suspicious keywords

**Request:**
```json
{
  "domain": "secure-login-verify.tk"
}
```

**Expected Result:**
- Status Code: `200 OK`
- Score: `60-79` or higher
- Classification: `"High"` or `"Critical"`
- Triggered Rules:
  - Risky TLD (.tk)
  - Suspicious keywords (login, verify, secure)
  - Possibly new domain age
  - Possibly no MX/SPF records

**Sample Response:**
```json
{
  "domain": "secure-login-verify.tk",
  "score": 85,
  "classification": "Critical",
  "triggered_rules": [
    {
      "rule": "risky_tld",
      "triggered": true,
      "weight": 20,
      "justification": "Domain uses high-risk TLD: .tk"
    },
    {
      "rule": "suspicious_keyword",
      "triggered": true,
      "weight": 15,
      "justification": "Suspicious keyword detected: login"
    },
    {
      "rule": "suspicious_keyword",
      "triggered": true,
      "weight": 15,
      "justification": "Suspicious keyword detected: verify"
    }
  ],
  "intelligence": {
    "age_days": null,
    "has_mx": false,
    "has_spf": false,
    "ssl_valid": false,
    "is_self_signed": false,
    "triggered_keywords": ["login", "verify", "secure"],
    "risky_tld": true,
    "is_punycode": false,
    "errors": ["WHOIS lookup failed"]
  }
}
```

---

### Scenario 4: Punycode/IDN Domain (Homograph Attack)

**Test Case:** Internationalized domain name (potential spoofing)

**Request:**
```json
{
  "domain": "xn--pple-43d.com"
}
```

**Expected Result:**
- Status Code: `200 OK`
- Score: High (25+ from punycode alone)
- Classification: `"Medium"` or higher
- Triggered Rules: Punycode detected

---

### Scenario 5: Domain with Multiple Risk Factors

**Test Case:** Compound risk scenario

**Request:**
```json
{
  "domain": "paypal-security-verify.ml"
}
```

**Expected Result:**
- Status Code: `200 OK`
- Score: `80-100`
- Classification: `"Critical"`
- Triggered Rules:
  - Risky TLD (.ml)
  - Multiple suspicious keywords (security, verify)
  - Likely no email infrastructure

---

## ❌ Error Testing

### Test Case 1: Invalid Domain Format

**Request:**
```json
{
  "domain": "not a valid domain!"
}
```

**Expected Result:**
- Status Code: `400 Bad Request`
- Error message about invalid domain format

**Sample Response:**
```json
{
  "detail": "Invalid domain format: not a valid domain!"
}
```

---

### Test Case 2: Empty Domain

**Request:**
```json
{
  "domain": ""
}
```

**Expected Result:**
- Status Code: `422 Unprocessable Entity`
- Validation error (min_length=1)

**Sample Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "domain"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

### Test Case 3: Domain Too Long

**Request:**
```json
{
  "domain": "a-very-long-domain-name-that-exceeds-the-maximum-allowed-length-of-253-characters-according-to-rfc-specifications-and-should-be-rejected-by-the-validation-logic-implemented-in-the-api-endpoint-to-prevent-potential-issues-with-dns-resolution-and-other-operations.com"
}
```

**Expected Result:**
- Status Code: `422 Unprocessable Entity`
- Validation error (max_length=253)

---

### Test Case 4: Missing Required Field

**Request:**
```json
{}
```

**Expected Result:**
- Status Code: `422 Unprocessable Entity`
- Missing field error

**Sample Response:**
```json
{
  "detail": [
    {
      "loc": ["body", "domain"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### Test Case 5: Invalid JSON

**Request:**
```
{domain: "example.com"}  // Missing quotes
```

**Expected Result:**
- Status Code: `422 Unprocessable Entity`
- JSON parse error

---

## 🔬 Advanced Testing

### Test Suite: Comprehensive Domain Analysis

Run these tests sequentially in Swagger UI to validate all functionality:

#### 1. Legitimate Domains (Low Risk)
```json
{"domain": "google.com"}
{"domain": "github.com"}
{"domain": "amazon.com"}
{"domain": "microsoft.com"}
```

#### 2. Risky TLDs (Medium-High Risk)
```json
{"domain": "example.tk"}
{"domain": "test.ml"}
{"domain": "site.xyz"}
{"domain": "shop.top"}
{"domain": "promo.club"}
```

#### 3. Suspicious Keywords (High Risk)
```json
{"domain": "login-portal.com"}
{"domain": "account-verify.net"}
{"domain": "secure-banking.org"}
{"domain": "paypal-update.info"}
```

#### 4. Compound Risks (Critical)
```json
{"domain": "secure-login.tk"}
{"domain": "bank-verify.ml"}
{"domain": "paypal-security.xyz"}
```

#### 5. Edge Cases
```json
{"domain": "localhost"}
{"domain": "127.0.0.1"}
{"domain": "sub.domain.example.com"}
{"domain": "xn--80akhbyknj4f.com"}
```

---

## 🤖 Automation Scripts

### cURL Commands

#### Test Low Risk Domain
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "google.com"}'
```

#### Test High Risk Domain
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "secure-login.tk"}'
```

#### Test Invalid Domain
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "invalid domain!"}'
```

#### Health Check
```bash
curl -X GET "http://localhost:8000/api/v1/health"
```

---

### Python Test Script

Create `test_api_swagger.py`:

```python
#!/usr/bin/env python3
"""Automated API testing script."""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(domain: str, expected_classification: str = None):
    """Test a single domain analysis."""
    url = f"{BASE_URL}/api/v1/analyze"
    payload = {"domain": domain}
    
    print(f"\n{'='*60}")
    print(f"Testing: {domain}")
    print(f"{'='*60}")
    
    response = requests.post(url, json=payload)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Score: {data['score']}")
        print(f"Classification: {data['classification']}")
        print(f"Triggered Rules: {len(data['triggered_rules'])}")
        
        if expected_classification:
            assert data['classification'] == expected_classification, \
                f"Expected {expected_classification}, got {data['classification']}"
            print(f"✓ Classification matches expected: {expected_classification}")
    else:
        print(f"Error: {response.json()}")
    
    return response

def main():
    """Run test suite."""
    print("Web Risk Intelligence System - API Test Suite")
    
    # Test health check
    print("\n" + "="*60)
    print("Health Check")
    print("="*60)
    health = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {health.json()['status']}")
    
    # Test legitimate domains
    test_endpoint("google.com", "Low")
    test_endpoint("github.com", "Low")
    
    # Test risky domains
    test_endpoint("example.tk")
    test_endpoint("secure-login.ml")
    
    # Test invalid domains
    print("\n" + "="*60)
    print("Testing Invalid Domain")
    print("="*60)
    response = requests.post(
        f"{BASE_URL}/api/v1/analyze",
        json={"domain": "invalid domain!"}
    )
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 400, "Should return 400 for invalid domain"
    print("✓ Invalid domain correctly rejected")
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()
```

Run the script:
```bash
python test_api_swagger.py
```

---

### Bash Test Script

Create `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "================================"
echo "API Test Suite"
echo "================================"

# Health check
echo -e "\n[TEST] Health Check"
curl -s "$BASE_URL/api/v1/health" | jq

# Test legitimate domain
echo -e "\n[TEST] Legitimate Domain (google.com)"
curl -s -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "google.com"}' | jq '.domain, .score, .classification'

# Test risky domain
echo -e "\n[TEST] Risky Domain (secure-login.tk)"
curl -s -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "secure-login.tk"}' | jq '.domain, .score, .classification'

# Test invalid domain
echo -e "\n[TEST] Invalid Domain"
curl -s -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "invalid!"}' | jq

echo -e "\n================================"
echo "Tests completed!"
echo "================================"
```

Make executable and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📊 Expected Results Summary

| Test Scenario | Status Code | Score Range | Classification |
|--------------|-------------|-------------|----------------|
| Legitimate domain (google.com) | 200 | 0-29 | Low |
| Risky TLD (.tk, .ml) | 200 | 20-40 | Medium |
| Suspicious keywords | 200 | 15-45 | Medium |
| Multiple risk factors | 200 | 60-100 | High/Critical |
| Punycode domain | 200 | 25+ | Medium+ |
| Invalid format | 400 | N/A | Error |
| Empty domain | 422 | N/A | Validation Error |
| Missing field | 422 | N/A | Validation Error |

---

## 🎯 Testing Checklist

Use this checklist to ensure comprehensive testing:

- [ ] Access Swagger UI successfully
- [ ] Test root endpoint (/)
- [ ] Test health check endpoint
- [ ] Test legitimate domain (Low risk)
- [ ] Test risky TLD domain (Medium risk)
- [ ] Test suspicious keyword domain (High risk)
- [ ] Test compound risk domain (Critical)
- [ ] Test punycode/IDN domain
- [ ] Test invalid domain format (400 error)
- [ ] Test empty domain (422 error)
- [ ] Test missing field (422 error)
- [ ] Test domain too long (422 error)
- [ ] Verify response schema matches documentation
- [ ] Verify triggered rules are populated correctly
- [ ] Verify intelligence object contains all fields
- [ ] Test with subdomain
- [ ] Test with IP address
- [ ] Run automated test script
- [ ] Export OpenAPI schema
- [ ] Test CORS headers (if applicable)

---

## 🔍 Troubleshooting

### Swagger UI Not Loading

**Problem:** Cannot access http://localhost:8000/docs

**Solutions:**
1. Verify API server is running: `curl http://localhost:8000/`
2. Check port 8000 is not in use: `lsof -i :8000`
3. Check logs for startup errors
4. Try alternative port: `uvicorn main_api:app --port 8001`

### 500 Internal Server Error

**Problem:** All requests return 500 error

**Solutions:**
1. Check configuration file exists: `config/settings.yaml`
2. Verify configuration is valid
3. Check server logs for detailed error
4. Ensure all dependencies installed: `pip install -r requirements.txt`

### Timeout Errors

**Problem:** Requests timeout or take too long

**Solutions:**
1. Check network connectivity
2. Adjust timeouts in `config/settings.yaml`
3. Test with known-good domain first
4. Check DNS resolver is working

---

## 📝 Notes

- All tests should be run with the API server running
- Some domains may return different results based on current DNS/WHOIS data
- Timeout errors are treated as intelligence signals, not failures
- The system is designed for graceful degradation
- Response times vary based on external data collection

---

**Happy Testing! 🚀**

*For issues or questions, refer to the main [README.md](README.md)*
