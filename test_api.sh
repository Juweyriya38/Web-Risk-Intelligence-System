#!/bin/bash

# Web Risk Intelligence System - API Test Script
# Quick testing script using cURL

BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    print_error "jq is not installed. Install it for better output formatting."
    print_info "On Ubuntu/Debian: sudo apt-get install jq"
    print_info "On macOS: brew install jq"
    USE_JQ=false
else
    USE_JQ=true
fi

# Check if server is running
print_header "Checking Server Status"
if curl -s "$BASE_URL/" > /dev/null 2>&1; then
    print_success "Server is running at $BASE_URL"
else
    print_error "Server is not running at $BASE_URL"
    print_info "Start the server with: python main_api.py"
    exit 1
fi

# Test 1: Health Check
print_header "Test 1: Health Check"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/api/v1/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Health check passed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '.'
    else
        echo "$body"
    fi
else
    print_error "Health check failed (Status: $http_code)"
fi

# Test 2: Root Endpoint
print_header "Test 2: Root Endpoint"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Root endpoint passed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '.'
    else
        echo "$body"
    fi
else
    print_error "Root endpoint failed (Status: $http_code)"
fi

# Test 3: Legitimate Domain (Low Risk)
print_header "Test 3: Legitimate Domain (google.com)"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "google.com"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Analysis completed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '{domain, score, classification, triggered_rules: (.triggered_rules | length)}'
    else
        echo "$body"
    fi
else
    print_error "Analysis failed (Status: $http_code)"
fi

# Test 4: Risky TLD Domain
print_header "Test 4: Risky TLD Domain (example.tk)"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.tk"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Analysis completed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '{domain, score, classification, triggered_rules: (.triggered_rules | length)}'
    else
        echo "$body"
    fi
else
    print_error "Analysis failed (Status: $http_code)"
fi

# Test 5: Suspicious Keywords
print_header "Test 5: Suspicious Keywords (secure-login.com)"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "secure-login.com"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Analysis completed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '{domain, score, classification, triggered_keywords: .intelligence.triggered_keywords}'
    else
        echo "$body"
    fi
else
    print_error "Analysis failed (Status: $http_code)"
fi

# Test 6: Compound Risk
print_header "Test 6: Compound Risk (secure-login.tk)"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "secure-login.tk"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "200" ]; then
    print_success "Analysis completed (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '{domain, score, classification}'
        echo -e "\nTriggered Rules:"
        echo "$body" | jq '.triggered_rules[] | "  - \(.rule): \(.justification)"' -r
    else
        echo "$body"
    fi
else
    print_error "Analysis failed (Status: $http_code)"
fi

# Test 7: Invalid Domain (Error Case)
print_header "Test 7: Invalid Domain Format"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": "not a valid domain!"}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "400" ]; then
    print_success "Correctly rejected invalid domain (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '.'
    else
        echo "$body"
    fi
else
    print_error "Expected 400, got $http_code"
fi

# Test 8: Empty Domain (Validation Error)
print_header "Test 8: Empty Domain"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"domain": ""}')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" = "422" ]; then
    print_success "Correctly rejected empty domain (Status: $http_code)"
    if [ "$USE_JQ" = true ]; then
        echo "$body" | jq '.'
    else
        echo "$body"
    fi
else
    print_error "Expected 422, got $http_code"
fi

# Summary
print_header "Test Summary"
print_success "All tests completed!"
print_info "Check the results above for any failures"
print_info "For interactive testing, visit: $BASE_URL/docs"

echo ""
