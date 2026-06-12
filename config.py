"""
Configuration settings for Cognitive Weather Oracle.
Store sensitive credentials here (or load from environment variables).
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")

# Default Location
DEFAULT_LOCATION = "New York, NY"
DEFAULT_UNITS = "imperial"  # "imperial" for Fahrenheit, "metric" for Celsius

# GUI Configuration
GUI_GEOMETRY = "900x1000"
GUI_REFRESH_INTERVAL_MS = 600000  # 10 minutes in milliseconds
GUI_THEME_MODE = "dark"  # "dark" or "light"

# Persona Configuration
DEFAULT_PERSONA = "philosopher"  # Can be extended: "poet", "scientist", etc.

# API Timeout
API_TIMEOUT_SECONDS = 5

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "cognitive_weather_oracle.log"