"""
Test Suite for Cognitive Weather Oracle

This package contains comprehensive unit tests, integration tests,
and end-to-end tests for all application components.

Test Structure:
- test_weather_api.py: Tests for OpenWeatherMap API integration
- test_persona_engine.py: Tests for cognitive narrative generation
- test_theme_manager.py: Tests for color themes and accessibility
- test_integration.py: End-to-end workflow tests
- conftest.py: Shared pytest fixtures and configuration

Running Tests:
    pytest                          # Run all tests
    pytest -v                       # Verbose output
    pytest -m unit                  # Run only unit tests
    pytest -m integration           # Run only integration tests
    pytest --cov                    # Generate coverage report
    pytest tests/test_weather_api.py # Run specific test file
"""
