#!/bin/bash
# Run the Web Risk Intelligence System API server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Web Risk Intelligence System API...${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating one...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created.${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}Dependencies not installed. Installing...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}Dependencies installed.${NC}"
fi

# Check if port 8000 is already in use
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}Error: Port 8000 is already in use.${NC}"
    echo -e "${YELLOW}Please stop the process using port 8000 or use a different port.${NC}"
    echo -e "${YELLOW}To find the process: lsof -i :8000${NC}"
    exit 1
fi

# Run the API server
echo -e "${GREEN}Starting API server on http://0.0.0.0:8000${NC}"
echo -e "${GREEN}API Documentation: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

python main_api.py
