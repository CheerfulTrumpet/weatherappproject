.PHONY: help install install-dev test test-unit test-integration test-cov lint format clean run docs

# Default target
help:
	@echo "Cognitive Weather Oracle - Development Commands"
	@echo "================================================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install production dependencies"
	@echo "  make install-dev      Install development dependencies"
	@echo "  make setup            Full setup (venv + dependencies)"
	@echo ""
	@echo "Development:"
	@echo "  make run              Run the application"
	@echo "  make lint             Run code linting (flake8)"
	@echo "  make format           Format code (black)"
	@echo "  make type-check       Run type checking (mypy)"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run all tests with coverage"
	@echo "  make test-unit        Run only unit tests"
	@echo "  make test-integration Run only integration tests"
	@echo "  make test-cov         Run tests with detailed coverage report"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and caches"
	@echo "  make clean-test       Remove test artifacts"
	@echo "  make clean-build      Remove build artifacts"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Generate documentation"
	@echo ""

# Setup targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install black flake8 mypy pytest-cov

setup: install-dev
	@echo "Setup complete! Configure .env and run 'make run'"

# Run application
run:
	python main.py

# Linting and formatting
lint:
	flake8 src tests main.py --max-line-length=100 --exclude=__pycache__

format:
	black src tests main.py config.py

type-check:
	mypy src --ignore-missing-imports

# Testing targets
test:
	pytest tests/ -v --cov=src --cov-report=html

test-unit:
	pytest tests/ -v -m unit

test-integration:
	pytest tests/ -v -m integration

test-cov:
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/index.html"

test-fast:
	pytest tests/ -v -m "not slow"

test-verbose:
	pytest tests/ -vv --tb=long

# Specific test files
test-api:
	pytest tests/test_weather_api.py -v

test-persona:
	pytest tests/test_persona_engine.py -v

test-theme:
	pytest tests/test_theme_manager.py -v

# Cleanup targets
clean: clean-build clean-test
	@echo "Cleaned build and test artifacts"

clean-test:
	rm -f .coverage
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f pytest.log
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '*.egg' -delete

clean-logs:
	rm -f *.log

# Documentation
docs:
	@echo "Documentation files:"
	@echo "  - README.md"
	@echo "  - COGNITIVE_MAPPING.md"
	@echo "  - QUICKSTART.md"
	@echo ""
	@echo "View with:"
	@echo "  less README.md"
	@echo "  less COGNITIVE_MAPPING.md"

# Development workflow
all: clean install-dev lint test
	@echo "Full development check completed!"

# Quick development loop
dev-loop: lint test-fast run

# Pre-commit checks (useful for git hooks)
pre-commit: lint type-check test-unit
	@echo "Pre-commit checks passed!"

# Build package
build: clean
	python setup.py sdist bdist_wheel

# Install package locally in development mode
install-local:
	pip install -e .

# Version management
version:
	@grep "version" setup.py | head -1

# Environment info
info:
	@echo "System Information:"
	@echo "  Python: $$(python --version)"
	@echo "  Pip: $$(pip --version)"
	@which python
	@echo ""
	@echo "Project Structure:"
	@echo "  Source files: $$(find src -name '*.py' | wc -l)"
	@echo "  Test files: $$(find tests -name '*.py' | wc -l)"
	@echo "  Total lines of code: $$(find src tests -name '*.py' -exec wc -l {} + | tail -1)"
	@echo ""

# Help target (most helpful)
.DEFAULT_GOAL := help

# Phony targets (don't represent actual files)
.PHONY: $(MAKECMDGOALS)
