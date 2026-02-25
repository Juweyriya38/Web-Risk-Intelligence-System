"""
FastAPI Service for Web Risk Intelligence
Minimal API wrapper around engine.analyze_domain()
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Dict, Any
import re

from app.core.engine import analyze_domain

app = FastAPI(
    title="Web Risk Intelligence API",
    description="Domain threat assessment service",
    version="1.0.0"
)


class DomainRequest(BaseModel):
    """Request model for domain analysis."""
    domain: str = Field(..., description="Domain name to analyze", example="example.com")
    
    @validator('domain')
    def validate_domain(cls, v):
        """Validate domain format."""
        if not v or len(v) > 253:
            raise ValueError("Invalid domain length")
        # Basic domain pattern
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        clean_domain = re.sub(r'^https?://', '', v.lower().strip())
        clean_domain = re.sub(r'/.*$', '', clean_domain)
        if not re.match(pattern, clean_domain):
            raise ValueError("Invalid domain format")
        return v


@app.get("/")
def root():
    """Root endpoint with service info."""
    return {
        "service": "Web Risk Intelligence API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/analyze", response_model=Dict[str, Any])
def analyze(request: DomainRequest):
    """
    Analyze a domain for risk indicators.
    
    Returns risk assessment with score, level, and reasons.
    """
    try:
        result = analyze_domain(request.domain)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
