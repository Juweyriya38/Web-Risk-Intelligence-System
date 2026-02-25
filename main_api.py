#!/usr/bin/env python3
"""
FastAPI Entry Point
Run with: uvicorn main_api:app --reload
"""

from app.api.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
