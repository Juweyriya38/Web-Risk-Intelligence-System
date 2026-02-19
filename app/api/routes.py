"""
API Routes - REST interface for domain analysis.
Uses dependency injection, no business logic in handlers.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.core.config_loader import ConfigLoader
from app.core.models import ConfigurationSchema, RiskResult
from app.services.analyzer_service import AnalyzerService

logger = logging.getLogger(__name__)

router = APIRouter()


# Request/Response models
class AnalyzeRequest(BaseModel):
    """Domain analysis request."""

    domain: str = Field(..., description="Domain to analyze", min_length=1, max_length=253)


class AnalyzeResponse(BaseModel):
    """Domain analysis response."""

    domain: str
    score: int
    classification: str
    triggered_rules: list[dict]
    intelligence: dict


# Dependency injection
def get_config() -> ConfigurationSchema:
    """Get configuration instance."""
    try:
        return ConfigLoader.get_instance()
    except RuntimeError:
        # Load if not already loaded
        return ConfigLoader.load()


def get_analyzer_service(config: ConfigurationSchema = Depends(get_config)) -> AnalyzerService:
    """Get analyzer service instance."""
    return AnalyzerService(config)


# Routes
@router.post("/analyze", response_model=AnalyzeResponse, status_code=200)
async def analyze_domain(
    request: AnalyzeRequest,
    service: AnalyzerService = Depends(get_analyzer_service),
) -> AnalyzeResponse:
    """
    Analyze a domain for risk indicators.

    Returns comprehensive risk assessment including:
    - Risk score (0-100)
    - Classification (Low, Medium, High, Critical)
    - Triggered risk rules
    - Intelligence signals
    """
    try:
        result: RiskResult = service.analyze_domain(request.domain)

        return AnalyzeResponse(
            domain=result.domain,
            score=result.score,
            classification=result.classification,
            triggered_rules=[
                {
                    "rule": rule.rule_name,
                    "triggered": rule.triggered,
                    "weight": rule.weight,
                    "justification": rule.justification,
                }
                for rule in result.triggered_rules
                if rule.triggered
            ],
            intelligence={
                "age_days": result.intelligence.age_days,
                "has_mx": result.intelligence.has_mx,
                "has_spf": result.intelligence.has_spf,
                "ssl_valid": result.intelligence.ssl_valid,
                "is_self_signed": result.intelligence.is_self_signed,
                "triggered_keywords": result.intelligence.triggered_keywords,
                "risky_tld": result.intelligence.risky_tld,
                "is_punycode": result.intelligence.is_punycode,
                "errors": result.intelligence.errors,
            },
        )

    except ValueError as e:
        logger.warning(f"Invalid domain: {request.domain} - {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Analysis error for {request.domain}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/health", status_code=200)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
