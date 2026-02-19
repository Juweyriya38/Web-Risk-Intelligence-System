# 🎯 Swagger UI Visual Guide

## Step-by-Step: Testing Your API in the Browser

---

## Step 1: Start the Server

```bash
cd /home/fuaxz/personal/Web-Risk-Intelligence-System
python main_api.py
```

**You should see:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Loading configuration...
INFO:     Configuration loaded successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 2: Open Swagger UI

**Open your browser and go to:**
```
http://localhost:8000/docs
```

**You will see a page that looks like this:**

```
┌─────────────────────────────────────────────────────────────┐
│  Web Risk Intelligence System                    v1.0.0     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Domain Threat Assessment & Risk Scoring API                 │
│                                                               │
│  Overview                                                     │
│  Production-grade domain threat assessment platform that     │
│  evaluates infrastructure signals to identify potential      │
│  phishing, impersonation, and malicious domains.             │
│                                                               │
│  Features                                                     │
│  🎯 Deterministic Scoring: Same input = same output          │
│  📊 Risk Classification: Low, Medium, High, Critical         │
│  🔍 Intelligence Signals: DNS, WHOIS, SSL, keywords, TLDs    │
│  ⚡ Fast Analysis: Typical response time < 15 seconds        │
│  🛡️ Graceful Degradation: Partial results on failures       │
│                                                               │
│  Quick Start                                                  │
│  1. Use the POST /api/v1/analyze endpoint below              │
│  2. Click "Try it out"                                        │
│  3. Enter a domain (e.g., "google.com")                      │
│  4. Click "Execute" to see results                           │
│                                                               │
│  Test Domains                                                 │
│  • Low Risk: google.com, github.com, amazon.com              │
│  • Medium Risk: example.tk, test.ml, shop.xyz                │
│  • High Risk: secure-login.com, account-verify.net           │
│  • Critical Risk: secure-login.tk, bank-verify.ml            │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│  info                                                         │
│  ▼ GET /  Root endpoint with service information             │
│                                                               │
│  analysis                                                     │
│  ▼ POST /api/v1/analyze  Analyze Domain Risk                 │
│  ▼ GET  /api/v1/health   Health Check                        │
│                                                               │
│  Schemas ▼                                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 3: Expand the Analyze Endpoint

**Click on the green bar that says:**
```
▼ POST /api/v1/analyze  Analyze Domain Risk
```

**It will expand to show:**

```
┌─────────────────────────────────────────────────────────────┐
│  POST /api/v1/analyze                                        │
│  Analyze Domain Risk                                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Perform comprehensive risk assessment of a domain.          │
│                                                               │
│  This endpoint analyzes infrastructure signals including:    │
│  • DNS Records: MX, SPF configuration                        │
│  • WHOIS Data: Domain age and registration info             │
│  • SSL Certificate: Validity and self-signed detection      │
│  • Lexical Analysis: Suspicious keywords and risky TLDs     │
│  • Punycode Detection: Internationalized domain names       │
│                                                               │
│  Returns a risk score (0-100) with detailed justifications.  │
│                                                               │
│  Parameters                                                   │
│  No parameters                                                │
│                                                               │
│  Request body  application/json  *required                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Example Value | Schema                                 │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │ {                                                      │  │
│  │   "domain": "google.com"                               │  │
│  │ }                                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  [Try it out]  ← CLICK THIS BUTTON                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 4: Click "Try it out"

**After clicking "Try it out", the interface becomes editable:**

```
┌─────────────────────────────────────────────────────────────┐
│  Request body  application/json  *required                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ {                                                      │  │
│  │   "domain": "google.com"  ← YOU CAN EDIT THIS         │  │
│  │ }                                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  [Execute]  [Clear]  [Cancel]                                │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 5: Enter a Domain

**Edit the JSON to test different domains:**

### Example 1: Low Risk Domain
```json
{
  "domain": "google.com"
}
```

### Example 2: Critical Risk Domain
```json
{
  "domain": "secure-login.tk"
}
```

### Example 3: Invalid Domain (to test error handling)
```json
{
  "domain": "not a valid domain!"
}
```

---

## Step 6: Click "Execute"

**After clicking Execute, you'll see:**

```
┌─────────────────────────────────────────────────────────────┐
│  [Execute]  [Clear]  [Cancel]                                │
│                                                               │
│  ⏳ Loading...                                                │
└─────────────────────────────────────────────────────────────┘
```

**Then after a few seconds:**

```
┌─────────────────────────────────────────────────────────────┐
│  Responses                                                    │
├─────────────────────────────────────────────────────────────┤
│  Curl                                                         │
│  curl -X 'POST' \                                            │
│    'http://localhost:8000/api/v1/analyze' \                  │
│    -H 'accept: application/json' \                           │
│    -H 'Content-Type: application/json' \                     │
│    -d '{"domain": "google.com"}'                             │
│                                                               │
│  Request URL                                                  │
│  http://localhost:8000/api/v1/analyze                        │
│                                                               │
│  Server response                                              │
│  Code: 200  ✓                                                │
│  Response body                                                │
│  {                                                            │
│    "domain": "google.com",                                   │
│    "score": 0,                                               │
│    "classification": "Low",                                  │
│    "triggered_rules": [],                                    │
│    "intelligence": {                                         │
│      "age_days": 9000,                                       │
│      "has_mx": true,                                         │
│      "has_spf": true,                                        │
│      "ssl_valid": true,                                      │
│      "is_self_signed": false,                                │
│      "triggered_keywords": [],                               │
│      "risky_tld": false,                                     │
│      "is_punycode": false,                                   │
│      "errors": []                                            │
│    }                                                          │
│  }                                                            │
│                                                               │
│  Response headers                                             │
│  content-length: 234                                         │
│  content-type: application/json                              │
│  date: Mon, 01 Jan 2024 12:00:00 GMT                        │
│                                                               │
│  Responses                                                    │
│  Code  Description                                           │
│  200   Successful analysis                                   │
│  400   Invalid domain format                                 │
│  422   Validation Error                                      │
│  500   Internal server error                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 7: Test Different Scenarios

### Scenario A: Critical Risk Domain

**Input:**
```json
{
  "domain": "secure-login.tk"
}
```

**Expected Output:**
```json
{
  "domain": "secure-login.tk",
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
    }
  ],
  "intelligence": {
    "age_days": null,
    "has_mx": false,
    "has_spf": false,
    "ssl_valid": false,
    "is_self_signed": false,
    "triggered_keywords": ["login", "secure"],
    "risky_tld": true,
    "is_punycode": false,
    "errors": ["WHOIS lookup failed"]
  }
}
```

---

### Scenario B: Invalid Domain (Error Case)

**Input:**
```json
{
  "domain": "not a valid domain!"
}
```

**Expected Output:**
```
Code: 400  ✗

{
  "detail": "Invalid domain format: not a valid domain!"
}
```

---

## Step 8: Explore Other Endpoints

### Health Check Endpoint

**Click on:**
```
▼ GET /api/v1/health  Health Check
```

**Click "Try it out" → "Execute"**

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Root Endpoint

**Click on:**
```
▼ GET /  Root endpoint with service information
```

**Click "Try it out" → "Execute"**

**Response:**
```json
{
  "service": "Web Risk Intelligence System",
  "version": "1.0.0",
  "docs": "/docs",
  "redoc": "/redoc",
  "openapi": "/openapi.json",
  "health": "/api/v1/health"
}
```

---

## Step 9: View Schemas

**Scroll down to the bottom of the page and click "Schemas ▼"**

You'll see detailed model definitions:
- **AnalyzeRequest** - Request body structure
- **AnalyzeResponse** - Response body structure
- **Intelligence** - Intelligence signals structure
- **TriggeredRule** - Triggered rule structure

---

## 🎯 Quick Test Checklist

Use this checklist to test all functionality:

- [ ] Open http://localhost:8000/docs
- [ ] Test GET / (root endpoint)
- [ ] Test GET /api/v1/health
- [ ] Test POST /api/v1/analyze with "google.com" (Low risk)
- [ ] Test POST /api/v1/analyze with "example.tk" (Medium risk)
- [ ] Test POST /api/v1/analyze with "secure-login.tk" (Critical risk)
- [ ] Test POST /api/v1/analyze with "invalid domain!" (400 error)
- [ ] Test POST /api/v1/analyze with "" (422 validation error)
- [ ] View response examples dropdown
- [ ] View schemas section
- [ ] Copy cURL command and test in terminal

---

## 🎨 Additional Features to Explore

### 1. Response Examples Dropdown
Click the dropdown next to "Example Value" to see:
- Low Risk Domain example
- Critical Risk Domain example

### 2. Copy cURL Command
After executing, copy the cURL command to test from terminal

### 3. Download OpenAPI Spec
Visit http://localhost:8000/openapi.json to download the full API specification

### 4. Alternative Documentation
Visit http://localhost:8000/redoc for a cleaner, read-only documentation view

---

## 🚀 You're All Set!

Your Swagger UI is fully functional and ready to use. Start testing your API endpoints directly in the browser!

**Access it at: http://localhost:8000/docs**
