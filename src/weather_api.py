"""
Weather API Module - One Call API 3.0
Uses OpenWeatherMap One Call API with direct latitude/longitude.
"""

import requests
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class WeatherData:
    """Normalized weather data structure."""
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    description: str
    wind_speed: float
    cloudiness: int
    raw_icon_code: str
    
    @property
    def weather_condition(self) -> str:
        """Normalize the weather description to a primary condition."""
        desc_lower = self.description.lower()
        
        if "clear" in desc_lower or "sunny" in desc_lower:
            return "clear"
        elif "rain" in desc_lower:
            return "rainy"
        elif "cloud" in desc_lower:
            return "cloudy"
        elif "storm" in desc_lower or "thunder" in desc_lower:
            return "stormy"
        elif "snow" in desc_lower:
            return "snowy"
        elif "mist" in desc_lower or "fog" in desc_lower:
            return "misty"
        else:
            return "moderate"


class WeatherAPIError(Exception):
    """Base exception for weather API errors."""
    pass


class WeatherAPIConnectionError(WeatherAPIError):
    """Raised when unable to connect to the weather API."""
    pass


class WeatherAPIDataError(WeatherAPIError):
    """Raised when API returns unexpected data structure."""
    pass


class WeatherAPI:
    """
    Handles OpenWeatherMap One Call API 3.0
    Location should be in format: "latitude,longitude"
    Example: "40.7128,-74.0060" for New York
    """
    
    ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"
    
    def __init__(
        self,
        api_key: str,
        location: str = "40.7128,-74.0060",
        units: str = "imperial"
    ):
        """Initialize the Weather API client."""
        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "Invalid API key. Please set OPENWEATHER_API_KEY environment variable."
            )
        
        if units not in ["imperial", "metric"]:
            raise ValueError("Units must be 'imperial' or 'metric'")
        
        self.api_key = api_key
        self.location = location
        self.units = units
        
        # Parse coordinates from location string
        try:
            parts = location.split(",")
            self.lat = float(parts[0].strip())
            self.lon = float(parts[1].strip())
        except (ValueError, IndexError):
            raise ValueError(f"Location must be in format 'lat,lon', got: {location}")
        
        logger.info(f"WeatherAPI initialized for {location} ({units})")
    
    def fetch_weather(self) -> Optional[WeatherData]:
        """Fetch current weather using One Call API 3.0"""
        try:
            response = self._make_request()
            response.raise_for_status()
            data = response.json()
            
            logger.debug(f"Received weather data")
            return self._parse_response(data)
        
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout")
            raise WeatherAPIConnectionError("Request timed out")
        
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise WeatherAPIConnectionError(f"Failed to connect to API: {e}")
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            if hasattr(e.response, 'status_code'):
                if e.response.status_code == 401:
                    raise WeatherAPIConnectionError("Invalid API key")
                elif e.response.status_code == 429:
                    raise WeatherAPIConnectionError("API rate limit exceeded")
            raise WeatherAPIConnectionError(f"HTTP error: {e}")
        
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to parse API response: {e}")
            raise WeatherAPIDataError(f"Unexpected API response format: {e}")
    
    def _make_request(self) -> requests.Response:
        """Make HTTP request to One Call API 3.0"""
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": self.units
        }
        
        logger.debug(f"Calling One Call API: lat={self.lat}, lon={self.lon}")
        
        response = requests.get(
            self.ONECALL_URL,
            params=params,
            timeout=5
        )
        
        return response
    
    def _parse_response(self, raw_data: dict) -> WeatherData:
        """Parse One Call API 3.0 JSON response into WeatherData"""
        try:
            # One Call API returns 'current' object with weather data
            current = raw_data["current"]
            weather = current["weather"][0]
            
            return WeatherData(
                temperature=float(current["temp"]),
                feels_like=float(current.get("feels_like", current["temp"])),
                humidity=int(current["humidity"]),
                pressure=int(current["pressure"]),
                description=weather.get("main", "Unknown"),
                wind_speed=float(current.get("wind_speed", 0)),
                cloudiness=int(current.get("clouds", 0)),
                raw_icon_code=weather.get("icon", "01d")
            )
        
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Error parsing API response: {e}")
            raise WeatherAPIDataError(
                f"Missing required fields in API response: {e}"
            )


class MockWeatherAPI(WeatherAPI):
    """Mock implementation of WeatherAPI for testing."""
    
    def __init__(self, mock_data: Optional[WeatherData] = None, **kwargs):
        self.mock_data = mock_data
        self.call_count = 0
    
    def fetch_weather(self) -> Optional[WeatherData]:
        """Return mock data instead of making API call."""
        self.call_count += 1
        return self.mock_data
    
    def _make_request(self) -> requests.Response:
        """Mock implementation - not called."""