# Architecture Decision Record (ADR)

## Context

This document explains the key architectural decisions made in the Web Risk Intelligence System and the rationale behind them.

---

## Decision 1: Clean Architecture with Pure Business Logic

### Status
**Accepted**

### Context
Need a maintainable, testable system that can evolve without breaking existing functionality.

### Decision
Implement strict clean architecture with the Risk Engine as pure business logic:
- No I/O operations in business logic
- No framework dependencies in core
- All dependencies point inward
- Data flows through standardized contracts

### Consequences

**Positive:**
- 100% testable without mocks
- Easy to change infrastructure (swap DNS library, add caching, etc.)
- Business logic never breaks due to external changes
- Can run risk engine in any context (CLI, API, batch, Lambda, etc.)

**Negative:**
- More initial boilerplate
- Requires discipline to maintain boundaries

### Alternatives Considered
- Monolithic approach with mixed concerns (rejected: hard to test and maintain)
- Microservices (rejected: overkill for this scope)

---

## Decision 2: Configuration-Driven Scoring

### Status
**Accepted**

### Context
Risk weights need to be tunable without code changes. Different organizations have different risk tolerances.

### Decision
Externalize all scoring parameters to `settings.yaml`:
- Risk weights
- Classification thresholds
- Keyword lists
- TLD lists

Validate configuration at startup (fail-fast).

### Consequences

**Positive:**
- Tune scoring without redeployment
- A/B test different configurations
- Transparent scoring logic
- Easy to audit and explain

**Negative:**
- Configuration errors only caught at runtime
- Need to maintain schema validation

### Alternatives Considered
- Hardcoded weights (rejected: inflexible)
- Database configuration (rejected: adds complexity)
- ML-based scoring (rejected: not explainable)

---

## Decision 3: Fail-Safe Collectors

### Status
**Accepted**

### Context
External services (DNS, WHOIS, SSL) can timeout, fail, or return partial data.

### Decision
All collectors:
- Have strict timeouts
- Return partial results on failure
- Treat failures as intelligence signals
- Never crash the system

### Consequences

**Positive:**
- System always returns a result
- Graceful degradation
- Failures provide risk signals (e.g., WHOIS timeout is suspicious)
- Resilient to network issues

**Negative:**
- Results may be incomplete
- Need to handle Optional types throughout

### Alternatives Considered
- Fail-fast on any error (rejected: too brittle)
- Retry logic (rejected: adds latency)

---

## Decision 4: CLI as Primary Interface

### Status
**Accepted**

### Context
Need both interactive use and programmatic integration.

### Decision
Build CLI first with Typer, API second with FastAPI. Both share the same service layer.

### Consequences

**Positive:**
- CLI perfect for security analysts
- Easy to script and automate
- Meaningful exit codes for CI/CD
- API available for integrations
- No code duplication (shared service)

**Negative:**
- Two interfaces to maintain

### Alternatives Considered
- API-only (rejected: less user-friendly for analysts)
- CLI-only (rejected: harder to integrate)

---

## Decision 5: Deterministic Heuristic Scoring

### Status
**Accepted**

### Context
Need explainable, auditable risk assessments for security decisions.

### Decision
Use weighted heuristic scoring instead of machine learning:
- Transparent rules
- Deterministic results
- Full explainability
- No training data required

### Consequences

**Positive:**
- Every score is explainable
- Auditable for compliance
- No black box
- Predictable behavior
- Easy to debug

**Negative:**
- May miss complex patterns
- Requires manual tuning
- Can have false positives

### Alternatives Considered
- Machine learning (rejected: not explainable, needs training data)
- Simple threshold rules (rejected: not nuanced enough)

---

## Decision 6: Pydantic for Data Contracts

### Status
**Accepted**

### Context
Need type-safe data flow between layers with validation.

### Decision
Use Pydantic models for all data structures:
- IntelligenceObject
- RiskResult
- ConfigurationSchema

### Consequences

**Positive:**
- Runtime type validation
- Automatic serialization
- IDE autocomplete
- Self-documenting
- FastAPI integration

**Negative:**
- Slight performance overhead
- Learning curve for team

### Alternatives Considered
- Dataclasses (rejected: no validation)
- Plain dicts (rejected: no type safety)

---

## Decision 7: No Database (Initially)

### Status
**Accepted**

### Context
Need to ship MVP quickly without operational complexity.

### Decision
No persistent storage in v1.0. Each analysis is stateless.

### Consequences

**Positive:**
- Simple deployment
- No database to manage
- Stateless (easy to scale)
- Fast development

**Negative:**
- No historical tracking
- No caching
- Can't monitor domain changes over time

### Future
Add PostgreSQL + Redis in Phase 3 (see Roadmap).

---

## Decision 8: Docker for Deployment

### Status
**Accepted**

### Context
Need consistent deployment across environments.

### Decision
Provide Dockerfile with multi-stage build and docker-compose.

### Consequences

**Positive:**
- Consistent environments
- Easy deployment
- Isolated dependencies
- Production-ready

**Negative:**
- Requires Docker knowledge
- Slightly larger artifact

### Alternatives Considered
- System packages (rejected: dependency conflicts)
- Virtual machines (rejected: too heavy)

---

## Decision 9: Timeout-Based Failure Detection

### Status
**Accepted**

### Context
Some domains intentionally slow down WHOIS/DNS to evade detection.

### Decision
Treat timeouts as risk signals, not just errors.

### Consequences

**Positive:**
- Detects evasion techniques
- Provides additional intelligence
- Keeps system responsive

**Negative:**
- Legitimate slow servers penalized
- Need to tune timeout values

---

## Decision 10: Separation of CLI and API Entry Points

### Status
**Accepted**

### Context
CLI and API have different startup requirements and lifecycles.

### Decision
Separate entry points (`main_cli.py`, `main_api.py`) that both use the same service layer.

### Consequences

**Positive:**
- Clear separation of concerns
- Different logging configurations
- Independent deployment
- No framework coupling

**Negative:**
- Two entry points to maintain

---

## Summary

These decisions prioritize:
1. **Maintainability** - Clean architecture, separation of concerns
2. **Testability** - Pure business logic, dependency injection
3. **Explainability** - Deterministic scoring, transparent rules
4. **Reliability** - Fail-safe collectors, graceful degradation
5. **Flexibility** - Configuration-driven, easy to extend

All decisions support the core goal: **Production-grade, explainable domain risk assessment**.
