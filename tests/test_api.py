"""
API endpoint tests.
Tests FastAPI routes using TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from main_api import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_valid_domain():
    """Test domain analysis with valid input."""
    response = client.post("/api/v1/analyze", json={"domain": "example.com"})

    assert response.status_code == 200
    data = response.json()

    assert "domain" in data
    assert "score" in data
    assert "classification" in data
    assert "triggered_rules" in data
    assert "intelligence" in data

    assert data["domain"] == "example.com"
    assert 0 <= data["score"] <= 100
    assert data["classification"] in ["Low", "Medium", "High", "Critical"]


def test_analyze_invalid_domain():
    """Test domain analysis with invalid input."""
    response = client.post("/api/v1/analyze", json={"domain": "invalid..domain"})

    assert response.status_code == 400
    assert "detail" in response.json()


def test_analyze_empty_domain():
    """Test domain analysis with empty input."""
    response = client.post("/api/v1/analyze", json={"domain": ""})

    assert response.status_code == 422  # Validation error


def test_analyze_domain_sanitization():
    """Test that API sanitizes domain input."""
    response = client.post("/api/v1/analyze", json={"domain": "https://EXAMPLE.COM/path"})

    assert response.status_code == 200
    data = response.json()
    assert data["domain"] == "example.com"


def test_openapi_docs():
    """Test that OpenAPI docs are available."""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
