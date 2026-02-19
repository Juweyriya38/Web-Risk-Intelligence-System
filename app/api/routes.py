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

    domain: str = Field(
        ...,
        description="Domain name to analyze (e.g., example.com)",
        min_length=1,
        max_length=253,
        examples=["google.com", "suspicious-login.tk", "secure-banking.ml"]
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {"domain": "google.com"},
                {"domain": "secure-login.tk"},
                {"domain": "bank-verify.ml"},
            ]
        }


class TriggeredRule(BaseModel):
    """Individual triggered risk rule."""
    rule: str = Field(..., description="Rule identifier")
    triggered: bool = Field(..., description="Whether rule was triggered")
    weight: int = Field(..., description="Risk weight contribution")
    justification: str = Field(..., description="Human-readable explanation")


class Intelligence(BaseModel):
    """Intelligence signals collected."""
    age_days: int | None = Field(None, description="Domain age in days")
    has_mx: bool = Field(..., description="Has MX records (email infrastructure)")
    has_spf: bool = Field(..., description="Has SPF records")
    ssl_valid: bool = Field(..., description="Valid SSL certificate")
    is_self_signed: bool = Field(..., description="Self-signed SSL certificate")
    triggered_keywords: list[str] = Field(..., description="Suspicious keywords found")
    risky_tld: bool = Field(..., description="Uses high-risk TLD")
    is_punycode: bool = Field(..., description="Internationalized domain (punycode)")
    errors: list[str] = Field(..., description="Collection errors encountered")


class AnalyzeResponse(BaseModel):
    """Domain analysis response."""

    domain: str = Field(..., description="Analyzed domain")
    score: int = Field(..., description="Risk score (0-100)", ge=0, le=100)
    classification: str = Field(
        ...,
        description="Risk classification",
        examples=["Low", "Medium", "High", "Critical"]
    )
    triggered_rules: list[TriggeredRule] = Field(..., description="Rules that triggered")
    intelligence: Intelligence = Field(..., description="Collected intelligence signals")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "domain": "google.com",
                    "score": 0,
                    "classification": "Low",
                    "triggered_rules": [],
                    "intelligence": {
                        "age_days": 9000,
                        "has_mx": True,
                        "has_spf": True,
                        "ssl_valid": True,
                        "is_self_signed": False,
                        "triggered_keywords": [],
                        "risky_tld": False,
                        "is_punycode": False,
                        "errors": []
                    }
                },
                {
                    "domain": "secure-login.tk",
                    "score": 85,
                    "classification": "Critical",
                    "triggered_rules": [
                        {
                            "rule": "risky_tld",
                            "triggered": True,
                            "weight": 20,
                            "justification": "Domain uses high-risk TLD: .tk"
                        },
                        {
                            "rule": "suspicious_keyword",
                            "triggered": True,
                            "weight": 15,
                            "justification": "Suspicious keyword detected: login"
                        }
                    ],
                    "intelligence": {
                        "age_days": None,
                        "has_mx": False,
                        "has_spf": False,
                        "ssl_valid": False,
                        "is_self_signed": False,
                        "triggered_keywords": ["login", "secure"],
                        "risky_tld": True,
                        "is_punycode": False,
                        "errors": ["WHOIS lookup failed"]
                    }
                }
            ]
        }


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
@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    status_code=200,
    summary="Analyze Domain Risk",
    description="""Perform comprehensive risk assessment of a domain.
    
    This endpoint analyzes infrastructure signals including:
    - **DNS Records**: MX, SPF configuration
    - **WHOIS Data**: Domain age and registration info
    - **SSL Certificate**: Validity and self-signed detection
    - **Lexical Analysis**: Suspicious keywords and risky TLDs
    - **Punycode Detection**: Internationalized domain names
    
    Returns a risk score (0-100) with detailed justifications.
    """,
    responses={
        200: {
            "description": "Successful analysis",
            "content": {
                "application/json": {
                    "examples": {
                        "low_risk": {
                            "summary": "Low Risk Domain (Legitimate)",
                            "value": {
                                "domain": "google.com",
                                "score": 0,
                                "classification": "Low",
                                "triggered_rules": [],
                                "intelligence": {
                                    "age_days": 9000,
                                    "has_mx": True,
                                    "has_spf": True,
                                    "ssl_valid": True,
                                    "is_self_signed": False,
                                    "triggered_keywords": [],
                                    "risky_tld": False,
                                    "is_punycode": False,
                                    "errors": []
                                }
                            }
                        },
                        "critical_risk": {
                            "summary": "Critical Risk Domain (Suspicious)",
                            "value": {
                                "domain": "secure-login.tk",
                                "score": 85,
                                "classification": "Critical",
                                "triggered_rules": [
                                    {
                                        "rule": "risky_tld",
                                        "triggered": True,
                                        "weight": 20,
                                        "justification": "Domain uses high-risk TLD: .tk"
                                    },
                                    {
                                        "rule": "suspicious_keyword",
                                        "triggered": True,
                                        "weight": 15,
                                        "justification": "Suspicious keyword detected: login"
                                    }
                                ],
                                "intelligence": {
                                    "age_days": None,
                                    "has_mx": False,
                                    "has_spf": False,
                                    "ssl_valid": False,
                                    "is_self_signed": False,
                                    "triggered_keywords": ["login", "secure"],
                                    "risky_tld": True,
                                    "is_punycode": False,
                                    "errors": ["WHOIS lookup failed"]
                                }
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid domain format",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid domain format: not a valid domain!"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            }
        }
    }
)
async def analyze_domain(
    request: AnalyzeRequest,
    service: AnalyzerService = Depends(get_analyzer_service),
) -> AnalyzeResponse:
    """Analyze a domain for risk indicators."""
    try:
        result: RiskResult = service.analyze_domain(request.domain)

        return AnalyzeResponse(
            domain=result.domain,
            score=result.score,
            classification=result.classification,
            triggered_rules=[
                TriggeredRule(
                    rule=rule.rule_name,
                    triggered=rule.triggered,
                    weight=rule.weight,
                    justification=rule.justification,
                )
                for rule in result.triggered_rules
                if rule.triggered
            ],
            intelligence=Intelligence(
                age_days=result.intelligence.age_days,
                has_mx=result.intelligence.has_mx,
                has_spf=result.intelligence.has_spf,
                ssl_valid=result.intelligence.ssl_valid,
                is_self_signed=result.intelligence.is_self_signed,
                triggered_keywords=result.intelligence.triggered_keywords,
                risky_tld=result.intelligence.risky_tld,
                is_punycode=result.intelligence.is_punycode,
                errors=result.intelligence.errors,
            ),
        )

    except ValueError as e:
        logger.warning(f"Invalid domain: {request.domain} - {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(f"Analysis error for {request.domain}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/health",
    status_code=200,
    summary="Health Check",
    description="Check if the API service is running and healthy.",
    responses={
        200: {
            "description": "Service is healthy",
            "content": {
                "application/json": {
                    "example": {"status": "healthy"}
                }
            }
        }
    }
)
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "healthy"}
