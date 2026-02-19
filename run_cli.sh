#!/bin/bash
# Run the Web Risk Intelligence System CLI

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import typer" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not installed. Installing...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}Dependencies installed.${NC}"
fi

# Run the CLI with provided arguments
python main_cli.py "$@"
