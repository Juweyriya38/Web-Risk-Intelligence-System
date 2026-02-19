.PHONY: help install test lint format type-check clean run-cli run-api docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linter"
	@echo "  make format       - Format code"
	@echo "  make type-check   - Run type checker"
	@echo "  make clean        - Clean cache files"
	@echo "  make run-cli      - Run CLI (example: make run-cli DOMAIN=example.com)"
	@echo "  make run-api      - Run API server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pre-commit install

test:
	pytest --cov=app --cov-report=term-missing --cov-report=html

lint:
	ruff check app/ tests/

format:
	black app/ tests/

type-check:
	mypy app/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov

run-cli:
	python main_cli.py analyze $(DOMAIN)

run-api:
	uvicorn main_api:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t risk-intelligence:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

all: format lint type-check test
