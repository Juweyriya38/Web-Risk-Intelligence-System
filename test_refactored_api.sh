#!/bin/bash
# Test script for Web Risk Intelligence API

echo "🧪 Testing Web Risk Intelligence API"
echo "======================================"
echo ""

API_URL="http://localhost:8001"

# Test 1: Health check
echo "1️⃣  Testing health endpoint..."
curl -s "$API_URL/health" | python3 -m json.tool
echo ""

# Test 2: Root endpoint
echo "2️⃣  Testing root endpoint..."
curl -s "$API_URL/" | python3 -m json.tool
echo ""

# Test 3: Analyze critical risk domain
echo "3️⃣  Testing critical risk domain (suspicious-login.tk)..."
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-login.tk"}' | python3 -m json.tool
echo ""

# Test 4: Analyze low risk domain
echo "4️⃣  Testing low risk domain (example.com)..."
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}' | python3 -m json.tool
echo ""

# Test 5: Analyze medium risk domain
echo "5️⃣  Testing medium risk domain (new-verify-account.com)..."
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "new-verify-account.com"}' | python3 -m json.tool
echo ""

# Test 6: Invalid domain
echo "6️⃣  Testing invalid domain..."
curl -s -X POST "$API_URL/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "invalid..domain"}' | python3 -m json.tool
echo ""

echo "✅ All tests completed!"
echo ""
echo "📖 View interactive docs at: $API_URL/docs"
