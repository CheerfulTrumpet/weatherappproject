"""
Test Suite for Weather API Module
==================================

Tests cover:
- WeatherData dataclass validation
- API connection and error handling
- Response parsing and normalization
- Edge cases and malformed data
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

from src.weather_api import (
    WeatherData,
    WeatherAPI,
    WeatherAPIError,
    WeatherAPIConnectionError,
    WeatherAPIDataError,
    MockWeatherAPI
)


# ============================================================================
# WEATHERDATA TESTS
# ============================================================================

class TestWeatherData:
    """Tests for the WeatherData dataclass."""
    
    @pytest.mark.unit
    def test_weather_data_creation(self, clear_weather_data):
        """Test WeatherData object creation and attributes."""
        assert clear_weather_data.temperature == 72.0
        assert clear_weather_data.humidity == 45
        assert clear_weather_data.description == "Clear Sky"
        assert clear_weather_data.cloudiness == 10
    
    @pytest.mark.unit
    def test_weather_condition_clear(self, clear_weather_data):
        """Test weather_condition property for clear sky."""
        assert clear_weather_data.weather_condition == "clear"
    
    @pytest.mark.unit
    def test_weather_condition_rainy(self, rainy_weather_data):
        """Test weather_condition property for rain."""
        assert rainy_weather_data.weather_condition == "rainy"
    
    @pytest.mark.unit
    def test_weather_condition_stormy(self, stormy_weather_data):
        """Test weather_condition property for storms."""
        assert stormy_weather_data.weather_condition == "stormy"
    
    @pytest.mark.unit
    def test_weather_condition_snowy(self, snowy_weather_data):
        """Test weather_condition property for snow."""
        assert snowy_weather_data.weather_condition == "snowy"
    
    @pytest.mark.unit
    def test_weather_condition_misty(self):
        """Test weather_condition property for mist."""
        misty_data = WeatherData(
            temperature=60, feels_like=60, humidity=80,
            pressure=1012, description="Mist", wind_speed=3,
            cloudiness=70, raw_icon_code="50d"
        )
        assert misty_data.weather_condition == "misty"
    
    @pytest.mark.unit
    def test_weather_condition_moderate(self):
        """Test weather_condition property for unknown conditions."""
        unknown_data = WeatherData(
            temperature=70, feels_like=70, humidity=50,
            pressure=1013, description="Unknown Condition", wind_speed=5,
            cloudiness=30, raw_icon_code="99d"
        )
        assert unknown_data.weather_condition == "moderate"
    
    @pytest.mark.unit
    def test_weather_condition_case_insensitive(self):
        """Test that weather_condition is case-insensitive."""
        data = WeatherData(
            temperature=70, feels_like=70, humidity=50,
            pressure=1013, description="CLEAR SKY", wind_speed=5,
            cloudiness=10, raw_icon_code="01d"
        )
        assert data.weather_condition == "clear"


# ============================================================================
# WEATHER API INITIALIZATION TESTS
# ============================================================================

class TestWeatherAPIInit:
    """Tests for WeatherAPI initialization."""
    
    @pytest.mark.unit
    def test_api_initialization_valid(self):
        """Test successful API initialization with valid key."""
        api = WeatherAPI(
            api_key="valid_key_123",
            location="New York, NY",
            units="imperial"
        )
        assert api.api_key == "valid_key_123"
        assert api.location == "New York, NY"
        assert api.units == "imperial"
    
    @pytest.mark.unit
    def test_api_initialization_invalid_key(self):
        """Test API initialization fails with invalid/empty key."""
        with pytest.raises(ValueError):
            WeatherAPI(api_key="", location="New York, NY")
    
    @pytest.mark.unit
    def test_api_initialization_default_key_placeholder(self):
        """Test API initialization fails with default placeholder key."""
        with pytest.raises(ValueError):
            WeatherAPI(
                api_key="your_api_key_here",
                location="New York, NY"
            )
    
    @pytest.mark.unit
    def test_api_initialization_invalid_units(self):
        """Test API initialization fails with invalid units."""
        with pytest.raises(ValueError):
            WeatherAPI(
                api_key="valid_key",
                location="New York, NY",
                units="kelvin"  # Invalid
            )
    
    @pytest.mark.unit
    def test_api_initialization_valid_units(self):
        """Test API accepts both valid unit types."""
        api_imperial = WeatherAPI(
            api_key="valid_key",
            location="New York, NY",
            units="imperial"
        )
        api_metric = WeatherAPI(
            api_key="valid_key",
            location="New York, NY",
            units="metric"
        )
        assert api_imperial.units == "imperial"
        assert api_metric.units == "metric"


# ============================================================================
# API RESPONSE PARSING TESTS
# ============================================================================

class TestAPIResponseParsing:
    """Tests for parsing OpenWeatherMap API responses."""
    
    @pytest.mark.unit
    def test_parse_valid_response(self):
        """Test parsing a complete, valid API response."""
        api = WeatherAPI(api_key="test_key")
        
        mock_response = {
            "main": {
                "temp": 72.5,
                "feels_like": 70.0,
                "humidity": 45,
                "pressure": 1013
            },
            "weather": [{"main": "Clear", "icon": "01d"}],
            "wind": {"speed": 5.5},
            "clouds": {"all": 10}
        }
        
        result = api._parse_response(mock_response)
        
        assert isinstance(result, WeatherData)
        assert result.temperature == 72.5
        assert result.humidity == 45
        assert result.description == "Clear"
    
    @pytest.mark.unit
    def test_parse_response_missing_feels_like(self):
        """Test parsing response that omits feels_like (uses temp instead)."""
        api = WeatherAPI(api_key="test_key")
        
        mock_response = {
            "main": {
                "temp": 72.5,
                "humidity": 45,
                "pressure": 1013
                # feels_like omitted
            },
            "weather": [{"main": "Clear", "icon": "01d"}],
            "wind": {"speed": 5.5},
            "clouds": {"all": 10}
        }
        
        result = api._parse_response(mock_response)
        assert result.feels_like == 72.5  # Falls back to temp
    
    @pytest.mark.unit
    def test_parse_response_missing_required_field(self):
        """Test parsing fails when required field is missing."""
        api = WeatherAPI(api_key="test_key")
        
        mock_response = {
            "main": {
                "temp": 72.5,
                # humidity missing
                "pressure": 1013
            },
            "weather": [{"main": "Clear"}],
        }
        
        with pytest.raises(WeatherAPIDataError):
            api._parse_response(mock_response)
    
    @pytest.mark.unit
    def test_parse_response_malformed_json(self):
        """Test parsing fails with malformed data structure."""
        api = WeatherAPI(api_key="test_key")
        
        with pytest.raises(WeatherAPIDataError):
            api._parse_response({"invalid": "structure"})
    
    @pytest.mark.unit
    def test_parse_response_type_conversion(self):
        """Test that numeric types are properly converted."""
        api = WeatherAPI(api_key="test_key")
        
        mock_response = {
            "main": {
                "temp": "72.5",  # String instead of number
                "feels_like": 70,
                "humidity": "45",  # String instead of number
                "pressure": 1013
            },
            "weather": [{"main": "Clear", "icon": "01d"}],
            "wind": {"speed": 5.5},
            "clouds": {"all": 10}
        }
        
        result = api._parse_response(mock_response)
        assert isinstance(result.temperature, float)
        assert isinstance(result.humidity, int)


# ============================================================================
# MOCK API TESTS
# ============================================================================

class TestMockWeatherAPI:
    """Tests for MockWeatherAPI testing utility."""
    
    @pytest.mark.unit
    def test_mock_api_returns_data(self, clear_weather_data):
        """Test mock API returns provided data."""
        mock_api = MockWeatherAPI(mock_data=clear_weather_data)
        result = mock_api.fetch_weather()
        
        assert result == clear_weather_data
        assert mock_api.call_count == 1
    
    @pytest.mark.unit
    def test_mock_api_returns_none(self):
        """Test mock API can return None for failure simulation."""
        mock_api = MockWeatherAPI(mock_data=None)
        result = mock_api.fetch_weather()
        
        assert result is None
        assert mock_api.call_count == 1
    
    @pytest.mark.unit
    def test_mock_api_multiple_calls(self, clear_weather_data):
        """Test mock API tracks multiple calls."""
        mock_api = MockWeatherAPI(mock_data=clear_weather_data)
        
        mock_api.fetch_weather()
        mock_api.fetch_weather()
        mock_api.fetch_weather()
        
        assert mock_api.call_count == 3


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestWeatherAPIIntegration:
    """Integration tests for Weather API."""
    
    @pytest.mark.integration
    @patch('src.weather_api.requests.get')
    def test_fetch_weather_success(self, mock_get, clear_weather_data):
        """Test successful weather fetch with mocked HTTP request."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "main": {
                "temp": clear_weather_data.temperature,
                "feels_like": clear_weather_data.feels_like,
                "humidity": clear_weather_data.humidity,
                "pressure": clear_weather_data.pressure
            },
            "weather": [{"main": clear_weather_data.description, "icon": clear_weather_data.raw_icon_code}],
            "wind": {"speed": clear_weather_data.wind_speed},
            "clouds": {"all": clear_weather_data.cloudiness}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        api = WeatherAPI(api_key="test_key", location="Test City")
        result = api.fetch_weather()
        
        assert result is not None
        assert result.description == clear_weather_data.description
        mock_get.assert_called_once()
    
    @pytest.mark.integration
    @patch('src.weather_api.requests.get')
    def test_fetch_weather_connection_error(self, mock_get):
        """Test handling of connection errors."""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        api = WeatherAPI(api_key="test_key")
        
        with pytest.raises(WeatherAPIConnectionError):
            api.fetch_weather()
    
    @pytest.mark.integration
    @patch('src.weather_api.requests.get')
    def test_fetch_weather_timeout(self, mock_get):
        """Test handling of timeout errors."""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        api = WeatherAPI(api_key="test_key")
        
        with pytest.raises(WeatherAPIConnectionError):
            api.fetch_weather()
    
    @pytest.mark.integration
    @patch('src.weather_api.requests.get')
    def test_fetch_weather_invalid_api_key(self, mock_get):
        """Test handling of invalid API key (401 response)."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_get.return_value = mock_response
        
        api = WeatherAPI(api_key="invalid_key")
        
        with pytest.raises(WeatherAPIConnectionError):
            api.fetch_weather()
    
    @pytest.mark.integration
    @patch('src.weather_api.requests.get')
    def test_fetch_weather_location_not_found(self, mock_get):
        """Test handling of location not found (404 response)."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        api = WeatherAPI(api_key="test_key", location="InvalidCity123")
        
        with pytest.raises(WeatherAPIConnectionError):
            api.fetch_weather()


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestWeatherAPIEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    @pytest.mark.unit
    def test_extreme_temperatures(self):
        """Test handling of extreme temperature values."""
        # Extremely cold
        cold_data = WeatherData(
            temperature=-50.0,
            feels_like=-60.0,
            humidity=20,
            pressure=1030,
            description="Clear Sky",
            wind_speed=10,
            cloudiness=5,
            raw_icon_code="01d"
        )
        assert cold_data.temperature == -50.0
        assert cold_data.weather_condition == "clear"
        
        # Extremely hot
        hot_data = WeatherData(
            temperature=120.0,
            feels_like=130.0,
            humidity=10,
            pressure=1000,
            description="Clear Sky",
            wind_speed=2,
            cloudiness=0,
            raw_icon_code="01d"
        )
        assert hot_data.temperature == 120.0
    
    @pytest.mark.unit
    def test_extreme_humidity(self):
        """Test handling of extreme humidity values."""
        data = WeatherData(
            temperature=85,
            feels_like=95,
            humidity=100,  # 100% humidity
            pressure=1008,
            description="Heavy Rain",
            wind_speed=5,
            cloudiness=100,
            raw_icon_code="10d"
        )
        assert data.humidity == 100
    
    @pytest.mark.unit
    def test_zero_wind_speed(self):
        """Test handling of zero wind speed."""
        data = WeatherData(
            temperature=72,
            feels_like=72,
            humidity=50,
            pressure=1013,
            description="Clear Sky",
            wind_speed=0.0,  # Calm conditions
            cloudiness=0,
            raw_icon_code="01d"
        )
        assert data.wind_speed == 0.0
    
    @pytest.mark.unit
    def test_very_high_wind_speed(self):
        """Test handling of very high wind speeds."""
        data = WeatherData(
            temperature=40,
            feels_like=25,
            humidity=70,
            pressure=990,
            description="Thunderstorm",
            wind_speed=75.0,  # Hurricane-force winds
            cloudiness=100,
            raw_icon_code="11d"
        )
        assert data.wind_speed == 75.0
