"""
FastAPI Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config_loader import ConfigLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup: Load and validate configuration
    logger.info("Loading configuration...")
    try:
        ConfigLoader.load()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Web Risk Intelligence System",
    description="""## Domain Threat Assessment & Risk Scoring API

### Overview
Production-grade domain threat assessment platform that evaluates infrastructure signals to identify potential phishing, impersonation, and malicious domains.

### Features
- 🎯 **Deterministic Scoring**: Same input always produces same output
- 📊 **Risk Classification**: Low (0-29), Medium (30-59), High (60-79), Critical (80-100)
- 🔍 **Intelligence Signals**: DNS, WHOIS, SSL, keywords, TLDs
- ⚡ **Fast Analysis**: Typical response time < 15 seconds
- 🛡️ **Graceful Degradation**: Partial results on collector failures

### Quick Start
1. Use the **POST /api/v1/analyze** endpoint below
2. Click "Try it out"
3. Enter a domain (e.g., "google.com" or "suspicious-login.tk")
4. Click "Execute" to see results

### Test Domains
- **Low Risk**: google.com, github.com, amazon.com
- **Medium Risk**: example.tk, test.ml, shop.xyz
- **High Risk**: secure-login.com, account-verify.net
- **Critical Risk**: secure-login.tk, bank-verify.ml
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "API Support",
        "url": "https://github.com/yourusername/web-risk-intelligence-system",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware (configure as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["analysis"])


@app.get("/", tags=["info"])
async def root():
    """Root endpoint with service information and quick links."""
    return {
        "service": "Web Risk Intelligence System",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
