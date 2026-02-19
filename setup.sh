#!/bin/bash
# Setup script for Web Risk Intelligence System

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Web Risk Intelligence System - Setup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo -e "${RED}Error: Python 3.11+ is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python version: $PYTHON_VERSION${NC}"

# Create virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ pip upgraded${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Make scripts executable
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x run_api.sh run_cli.sh setup.sh
echo -e "${GREEN}✓ Scripts are executable${NC}"

# Verify installation
echo ""
echo -e "${YELLOW}Verifying installation...${NC}"
python main_cli.py --help > /dev/null 2>&1 && echo -e "${GREEN}✓ CLI is working${NC}" || echo -e "${RED}✗ CLI verification failed${NC}"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo -e "  ${YELLOW}CLI:${NC}  ./run_cli.sh analyze example.com"
echo -e "  ${YELLOW}API:${NC}  ./run_api.sh"
echo ""
echo -e "${BLUE}Examples:${NC}"
echo -e "  ./run_cli.sh analyze google.com"
echo -e "  ./run_cli.sh analyze suspicious-site.tk --json"
echo -e "  ./run_cli.sh analyze example.com --verbose"
echo ""
