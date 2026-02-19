"""
Unit tests for domain validators.
Tests input sanitization and validation.
"""

import pytest
from app.core.validators import DomainValidator


def test_valid_domains():
    """Test valid domain formats."""
    valid_domains = [
        "example.com",
        "sub.example.com",
        "test-domain.co.uk",
        "a.b.c.d.example.com",
        "123.com",
        "xn--test.com",
    ]

    for domain in valid_domains:
        result = DomainValidator.validate(domain)
        assert result == domain.lower()


def test_domain_sanitization():
    """Test domain sanitization."""
    assert DomainValidator.validate("  EXAMPLE.COM  ") == "example.com"
    assert DomainValidator.validate("https://example.com") == "example.com"
    assert DomainValidator.validate("http://example.com") == "example.com"
    assert DomainValidator.validate("www.example.com") == "example.com"
    assert DomainValidator.validate("example.com/path") == "example.com"
    assert DomainValidator.validate("example.com?query=1") == "example.com"


def test_invalid_domains():
    """Test invalid domain formats."""
    invalid_domains = [
        "",
        "   ",
        "-example.com",
        "example-.com",
        "exam ple.com",
        "example..com",
        ".example.com",
        "example.com.",
        "a" * 64 + ".com",  # Label too long
        "a" * 254,  # Domain too long
    ]

    for domain in invalid_domains:
        with pytest.raises(ValueError):
            DomainValidator.validate(domain)


def test_tld_extraction():
    """Test TLD extraction."""
    assert DomainValidator.extract_tld("example.com") == ".com"
    assert DomainValidator.extract_tld("test.co.uk") == ".uk"
    assert DomainValidator.extract_tld("sub.example.org") == ".org"
    assert DomainValidator.extract_tld("localhost") is None


def test_punycode_detection():
    """Test punycode detection."""
    assert DomainValidator.is_punycode("xn--test.com") is True
    assert DomainValidator.is_punycode("xn--80akhbyknj4f.com") is True
    assert DomainValidator.is_punycode("example.com") is False
    assert DomainValidator.is_punycode("test-domain.com") is False
