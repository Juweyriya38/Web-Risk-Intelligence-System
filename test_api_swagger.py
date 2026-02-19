#!/usr/bin/env python3
"""
Automated API Testing Script for Web Risk Intelligence System
Run comprehensive tests against the API endpoints.
"""

import requests
import json
import sys
from typing import Optional

BASE_URL = "http://localhost:8000"
COLORS = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "END": "\033[0m"
}

def print_header(text: str):
    """Print formatted header."""
    print(f"\n{COLORS['BLUE']}{'='*70}{COLORS['END']}")
    print(f"{COLORS['BLUE']}{text:^70}{COLORS['END']}")
    print(f"{COLORS['BLUE']}{'='*70}{COLORS['END']}")

def print_success(text: str):
    """Print success message."""
    print(f"{COLORS['GREEN']}✓ {text}{COLORS['END']}")

def print_error(text: str):
    """Print error message."""
    print(f"{COLORS['RED']}✗ {text}{COLORS['END']}")

def print_info(text: str):
    """Print info message."""
    print(f"{COLORS['YELLOW']}ℹ {text}{COLORS['END']}")

def test_health_check():
    """Test health check endpoint."""
    print_header("Health Check Test")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print_success(f"Health check passed: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint."""
    print_header("Root Endpoint Test")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Service: {data.get('service')}")
            print_success(f"Version: {data.get('version')}")
            return True
        else:
            print_error(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Root endpoint error: {e}")
        return False

def test_domain_analysis(domain: str, expected_classification: Optional[str] = None, 
                        should_fail: bool = False, expected_status: int = 200):
    """Test domain analysis endpoint."""
    print_header(f"Testing Domain: {domain}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze",
            json={"domain": domain},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if should_fail:
            if response.status_code == expected_status:
                print_success(f"Correctly returned error status {expected_status}")
                print_info(f"Error: {response.json().get('detail', 'N/A')}")
                return True
            else:
                print_error(f"Expected {expected_status}, got {response.status_code}")
                return False
        
        if response.status_code == 200:
            data = response.json()
            print(f"Domain: {data['domain']}")
            print(f"Score: {data['score']}/100")
            print(f"Classification: {data['classification']}")
            print(f"Triggered Rules: {len(data['triggered_rules'])}")
            
            if data['triggered_rules']:
                print("\nTriggered Rules:")
                for rule in data['triggered_rules'][:3]:  # Show first 3
                    print(f"  - {rule['rule']}: {rule['justification']}")
            
            if expected_classification:
                if data['classification'] == expected_classification:
                    print_success(f"Classification matches expected: {expected_classification}")
                    return True
                else:
                    print_error(f"Expected {expected_classification}, got {data['classification']}")
                    return False
            
            print_success("Analysis completed successfully")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Test error: {e}")
        return False

def run_test_suite():
    """Run comprehensive test suite."""
    print(f"\n{COLORS['BLUE']}{'='*70}")
    print(f"{'Web Risk Intelligence System - API Test Suite':^70}")
    print(f"{'='*70}{COLORS['END']}\n")
    
    results = []
    
    # 1. Health and root tests
    results.append(("Health Check", test_health_check()))
    results.append(("Root Endpoint", test_root_endpoint()))
    
    # 2. Legitimate domains (Low Risk)
    results.append(("Legitimate Domain (google.com)", 
                   test_domain_analysis("google.com", "Low")))
    results.append(("Legitimate Domain (github.com)", 
                   test_domain_analysis("github.com", "Low")))
    
    # 3. Risky TLD domains
    results.append(("Risky TLD (.tk)", 
                   test_domain_analysis("example.tk")))
    results.append(("Risky TLD (.ml)", 
                   test_domain_analysis("test.ml")))
    
    # 4. Suspicious keyword domains
    results.append(("Suspicious Keywords (login)", 
                   test_domain_analysis("secure-login-portal.com")))
    results.append(("Suspicious Keywords (verify)", 
                   test_domain_analysis("account-verify.net")))
    
    # 5. Compound risk domains
    results.append(("Compound Risk (login + .tk)", 
                   test_domain_analysis("secure-login.tk")))
    results.append(("Compound Risk (bank + .ml)", 
                   test_domain_analysis("bank-verify.ml")))
    
    # 6. Edge cases
    results.append(("Subdomain", 
                   test_domain_analysis("api.example.com")))
    results.append(("Punycode Domain", 
                   test_domain_analysis("xn--80akhbyknj4f.com")))
    
    # 7. Error cases
    results.append(("Invalid Domain Format", 
                   test_domain_analysis("not a valid domain!", should_fail=True, expected_status=400)))
    results.append(("Empty Domain", 
                   test_domain_analysis("", should_fail=True, expected_status=422)))
    
    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print_success(f"Passed: {passed}")
    if total - passed > 0:
        print_error(f"Failed: {total - passed}")
    
    print("\nDetailed Results:")
    for test_name, result in results:
        status = f"{COLORS['GREEN']}PASS{COLORS['END']}" if result else f"{COLORS['RED']}FAIL{COLORS['END']}"
        print(f"  {status} - {test_name}")
    
    success_rate = (passed / total) * 100
    print(f"\n{COLORS['BLUE']}Success Rate: {success_rate:.1f}%{COLORS['END']}")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_test_suite()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{COLORS['YELLOW']}Tests interrupted by user{COLORS['END']}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        sys.exit(1)
