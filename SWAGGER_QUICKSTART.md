# Swagger UI Quick Start Guide

## 🚀 Access Swagger UI

1. **Start the API server:**
   ```bash
   python main_api.py
   ```

2. **Open your browser and navigate to:**
   - **Swagger UI**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc
   - **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🎯 Testing Endpoints in Browser

### Step 1: Navigate to Swagger UI
Open http://localhost:8000/docs in your browser

### Step 2: Test the Analyze Endpoint

1. **Locate the endpoint**: Find `POST /api/v1/analyze` under the "analysis" section

2. **Click "Try it out"** button (top right of the endpoint)

3. **Enter a domain** in the request body:
   ```json
   {
     "domain": "google.com"
   }
   ```

4. **Click "Execute"** button

5. **View the response** below:
   - Response code (200, 400, 500)
   - Response body with risk score and details
   - Response headers

---

## 📝 Example Test Cases

### Test 1: Low Risk Domain (Legitimate)
```json
{
  "domain": "google.com"
}
```
**Expected**: Score 0-29, Classification "Low"

---

### Test 2: Medium Risk (Risky TLD)
```json
{
  "domain": "example.tk"
}
```
**Expected**: Score 20+, Classification "Medium"

---

### Test 3: High Risk (Suspicious Keywords)
```json
{
  "domain": "secure-login-portal.com"
}
```
**Expected**: Score 30-60, Classification "Medium" or "High"

---

### Test 4: Critical Risk (Compound Threats)
```json
{
  "domain": "secure-login.tk"
}
```
**Expected**: Score 80+, Classification "Critical"

---

### Test 5: Invalid Domain (Error Case)
```json
{
  "domain": "not a valid domain!"
}
```
**Expected**: 400 Bad Request error

---

## 🔍 Understanding the Response

### Successful Response (200 OK)
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

### Response Fields Explained:
- **domain**: The analyzed domain
- **score**: Risk score from 0-100
- **classification**: Low (0-29), Medium (30-59), High (60-79), Critical (80-100)
- **triggered_rules**: List of risk rules that were triggered
- **intelligence**: Raw signals collected (DNS, WHOIS, SSL, etc.)

---

## 🎨 Swagger UI Features

### 1. Interactive Testing
- Click "Try it out" to enable editing
- Modify the request body
- Click "Execute" to send the request
- View real-time responses

### 2. Example Responses
- Click on response examples to see sample outputs
- "Low Risk Domain" example shows legitimate site
- "Critical Risk Domain" example shows suspicious site

### 3. Schema Documentation
- Scroll down to "Schemas" section
- View detailed model definitions
- See field types, constraints, and descriptions

### 4. Response Codes
- **200**: Successful analysis
- **400**: Invalid domain format
- **422**: Validation error (empty domain, too long, etc.)
- **500**: Internal server error

---

## 🧪 Quick Test Sequence

Run these tests in order to validate all functionality:

1. **Health Check**: GET `/api/v1/health`
   - Should return `{"status": "healthy"}`

2. **Legitimate Domain**: POST `/api/v1/analyze`
   - Domain: `google.com`
   - Expected: Low risk

3. **Risky TLD**: POST `/api/v1/analyze`
   - Domain: `example.tk`
   - Expected: Medium risk

4. **Suspicious Keywords**: POST `/api/v1/analyze`
   - Domain: `secure-login.com`
   - Expected: Medium/High risk

5. **Compound Risk**: POST `/api/v1/analyze`
   - Domain: `secure-login.tk`
   - Expected: Critical risk

6. **Invalid Domain**: POST `/api/v1/analyze`
   - Domain: `invalid domain!`
   - Expected: 400 error

---

## 💡 Tips

- **Use the dropdown** to select different example responses
- **Copy cURL commands** from the "curl" tab for command-line testing
- **Download OpenAPI spec** from http://localhost:8000/openapi.json
- **Use ReDoc** (http://localhost:8000/redoc) for alternative documentation view
- **Check response time** shown in the response section

---

## 🐛 Troubleshooting

### Swagger UI not loading?
- Ensure server is running: `curl http://localhost:8000/`
- Check console for errors
- Try clearing browser cache

### Requests timing out?
- Some domains may take 10-15 seconds to analyze
- External DNS/WHOIS lookups have timeouts
- This is normal behavior

### Getting 500 errors?
- Check server logs for details
- Verify `config/settings.yaml` exists
- Ensure all dependencies are installed

---

**Happy Testing! 🎉**

Visit http://localhost:8000/docs to get started!
