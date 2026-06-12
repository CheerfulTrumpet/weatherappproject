"""
Pytest Configuration and Fixtures
==================================

This file contains shared test fixtures and configuration for the test suite.
Fixtures allow tests to be concise and focused on behavior rather than setup.
"""

import pytest
from src.weather_api import WeatherData, MockWeatherAPI
from src.persona_engine import PersonaEngine, PersonaStyle
from src.theme_manager import ThemeManager


# ============================================================================
# WEATHER DATA FIXTURES
# ============================================================================

@pytest.fixture
def clear_weather_data() -> WeatherData:
    """Fixture for clear, sunny weather conditions."""
    return WeatherData(
        temperature=72.0,
        feels_like=70.0,
        humidity=45,
        pressure=1013,
        description="Clear Sky",
        wind_speed=5.0,
        cloudiness=10,
        raw_icon_code="01d"
    )


@pytest.fixture
def rainy_weather_data() -> WeatherData:
    """Fixture for rainy weather conditions."""
    return WeatherData(
        temperature=55.0,
        feels_like=52.0,
        humidity=85,
        pressure=1005,
        description="Heavy Rain",
        wind_speed=12.0,
        cloudiness=95,
        raw_icon_code="10d"
    )


@pytest.fixture
def stormy_weather_data() -> WeatherData:
    """Fixture for stormy weather conditions."""
    return WeatherData(
        temperature=62.0,
        feels_like=55.0,
        humidity=90,
        pressure=995,
        description="Thunderstorm",
        wind_speed=25.0,
        cloudiness=100,
        raw_icon_code="11d"
    )


@pytest.fixture
def snowy_weather_data() -> WeatherData:
    """Fixture for snowy weather conditions."""
    return WeatherData(
        temperature=28.0,
        feels_like=18.0,
        humidity=70,
        pressure=1015,
        description="Snow",
        wind_speed=8.0,
        cloudiness=90,
        raw_icon_code="13d"
    )


@pytest.fixture
def cloudy_weather_data() -> WeatherData:
    """Fixture for cloudy weather conditions."""
    return WeatherData(
        temperature=65.0,
        feels_like=64.0,
        humidity=60,
        pressure=1012,
        description="Overcast clouds",
        wind_speed=6.0,
        cloudiness=80,
        raw_icon_code="04d"
    )


@pytest.fixture
def extreme_heat_data() -> WeatherData:
    """Fixture for extreme heat conditions."""
    return WeatherData(
        temperature=98.0,
        feels_like=105.0,
        humidity=65,
        pressure=1009,
        description="Clear Sky",
        wind_speed=3.0,
        cloudiness=5,
        raw_icon_code="01d"
    )


@pytest.fixture
def extreme_cold_data() -> WeatherData:
    """Fixture for extreme cold conditions."""
    return WeatherData(
        temperature=5.0,
        feels_like=-5.0,
        humidity=35,
        pressure=1020,
        description="Clear Sky",
        wind_speed=15.0,
        cloudiness=10,
        raw_icon_code="01d"
    )


@pytest.fixture
def high_humidity_data() -> WeatherData:
    """Fixture for high humidity conditions."""
    return WeatherData(
        temperature=78.0,
        feels_like=88.0,
        humidity=95,
        pressure=1008,
        description="Mist",
        wind_speed=2.0,
        cloudiness=70,
        raw_icon_code="50d"
    )


# ============================================================================
# API FIXTURES
# ============================================================================

@pytest.fixture
def mock_clear_api(clear_weather_data: WeatherData) -> MockWeatherAPI:
    """Mock API that returns clear weather."""
    return MockWeatherAPI(mock_data=clear_weather_data)


@pytest.fixture
def mock_rainy_api(rainy_weather_data: WeatherData) -> MockWeatherAPI:
    """Mock API that returns rainy weather."""
    return MockWeatherAPI(mock_data=rainy_weather_data)


@pytest.fixture
def mock_failing_api() -> MockWeatherAPI:
    """Mock API that returns None (simulating failure)."""
    return MockWeatherAPI(mock_data=None)


# ============================================================================
# PERSONA ENGINE FIXTURES
# ============================================================================

@pytest.fixture
def philosopher_engine() -> PersonaEngine:
    """Persona Engine with philosopher style."""
    return PersonaEngine(persona=PersonaStyle.PHILOSOPHER)


@pytest.fixture
def poet_engine() -> PersonaEngine:
    """Persona Engine with poet style."""
    return PersonaEngine(persona=PersonaStyle.POET)


@pytest.fixture
def scientist_engine() -> PersonaEngine:
    """Persona Engine with scientist style."""
    return PersonaEngine(persona=PersonaStyle.SCIENTIST)


@pytest.fixture
def minimalist_engine() -> PersonaEngine:
    """Persona Engine with minimalist style."""
    return PersonaEngine(persona=PersonaStyle.MINIMALIST)


# ============================================================================
# THEME FIXTURES
# ============================================================================

@pytest.fixture
def all_themes():
    """Fixture providing all available themes."""
    return ThemeManager.get_all_themes()


@pytest.fixture
def clear_theme():
    """Fixture for clear weather theme."""
    return ThemeManager.get_theme("clear")


@pytest.fixture
def stormy_theme():
    """Fixture for stormy weather theme."""
    return ThemeManager.get_theme("stormy")


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# ============================================================================
# PARAMETRIZE COMMON PATTERNS
# ============================================================================

WEATHER_CONDITIONS = ["clear", "rainy", "cloudy", "stormy", "snowy", "misty"]

TEMPERATURE_RANGES = [
    (5, "extreme_cold"),
    (32, "freezing"),
    (55, "cool"),
    (72, "comfortable"),
    (85, "warm"),
    (95, "hot"),
]
