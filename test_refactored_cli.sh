#!/bin/bash
# Test script for Web Risk Intelligence CLI

echo "🧪 Testing Web Risk Intelligence CLI"
echo "====================================="
echo ""

# Test 1: Critical risk domain (JSON)
echo "1️⃣  Critical risk domain (JSON output):"
echo "   Command: python main_cli.py analyze suspicious-login.tk --json"
python main_cli.py analyze suspicious-login.tk --json
echo ""

# Test 2: Low risk domain (JSON)
echo "2️⃣  Low risk domain (JSON output):"
echo "   Command: python main_cli.py analyze example.com --json"
python main_cli.py analyze example.com --json
echo ""

# Test 3: Medium risk domain (JSON)
echo "3️⃣  Medium risk domain (JSON output):"
echo "   Command: python main_cli.py analyze verify-account.xyz --json"
python main_cli.py analyze verify-account.xyz --json
echo ""

# Test 4: Human-readable output
echo "4️⃣  Human-readable output:"
echo "   Command: python main_cli.py analyze suspicious-login.tk"
python main_cli.py analyze suspicious-login.tk
echo ""

# Test 5: Help
echo "5️⃣  Help output:"
echo "   Command: python main_cli.py analyze --help"
python main_cli.py analyze --help
echo ""

echo "✅ All CLI tests completed!"
