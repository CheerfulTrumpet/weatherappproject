"""
Cognitive Weather Oracle - Main Application
With location switching support
"""

import logging
import sys
import customtkinter as ctk
from typing import Optional

from config import (
    OPENWEATHER_API_KEY,
    DEFAULT_LOCATION,
    DEFAULT_UNITS,
    GUI_THEME_MODE,
    DEFAULT_PERSONA,
    LOG_LEVEL,
    LOG_FILE
)

from src.weather_api import WeatherAPI, WeatherAPIError
from src.persona_engine import PersonaEngine, PersonaStyle
from src.gui import WeatherGUI


# Configure logging
def setup_logging():
    """Configure application logging."""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(log_format))
    
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(log_format))
    
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return logging.getLogger(__name__)


logger = setup_logging()


def validate_configuration() -> bool:
    """Validate configuration."""
    if OPENWEATHER_API_KEY == "your_api_key_here":
        logger.error("API key not configured")
        return False
    return True


class CognitiveWeatherOracleApp:
    """Main application controller with location switching."""
    
    def __init__(self):
        """Initialize the application."""
        logger.info("Initializing Cognitive Weather Oracle...")
        
        # Initialize Persona Engine
        try:
            persona = PersonaStyle(DEFAULT_PERSONA)
            self.persona_engine = PersonaEngine(persona=persona)
            logger.info(f"Persona Engine initialized with {persona.value} persona")
        except ValueError as e:
            logger.error(f"Invalid persona: {e}")
            raise
        
        # Location info
        self.location_coords = {
            "New York": "40.7128,-74.0060",
            "London": "51.5074,-0.1278",
            "Paris": "48.8566,2.3522",
            "Tokyo": "35.6762,139.6503",
            "Sydney": "-33.8688,151.2093",
            "Dubai": "25.2048,55.2708",
            "Singapore": "1.3521,103.8198",
        }
        
        self.current_location = "New York"
        
        # Initialize API with first location
        try:
            self.weather_api = WeatherAPI(
                api_key=OPENWEATHER_API_KEY,
                location=self.location_coords[self.current_location],
                units=DEFAULT_UNITS
            )
            logger.info(f"Weather API initialized for {self.current_location}")
        except ValueError as e:
            logger.error(f"Failed to initialize Weather API: {e}")
            raise
        
        # Initialize GUI
        self.root = ctk.CTk()
        ctk.set_appearance_mode(GUI_THEME_MODE)
        
        self.gui = WeatherGUI(
            root=self.root,
            weather_fetcher=self._fetch_weather,
            narrative_generator=self._generate_narrative,
            location_name=self.current_location,
            on_location_change=self._change_location
        )
        
        logger.info("Application initialization complete")
    
    def _fetch_weather(self) -> Optional:
        """Fetch weather data from API."""
        try:
            return self.weather_api.fetch_weather()
        except WeatherAPIError as e:
            logger.error(f"Weather API error: {e}")
            return None
    
    def _generate_narrative(self, weather_data):
        """Generate cognitive narrative from weather data."""
        return self.persona_engine.generate_summary(weather_data)
    
    def _change_location(self, location_name: str):
        """Change the current location."""
        logger.info(f"Changing location to: {location_name}")
        
        if location_name not in self.location_coords:
            logger.warning(f"Unknown location: {location_name}")
            return
        
        self.current_location = location_name
        
        # Reinitialize API with new location
        try:
            self.weather_api = WeatherAPI(
                api_key=OPENWEATHER_API_KEY,
                location=self.location_coords[location_name],
                units=DEFAULT_UNITS
            )
            logger.info(f"Weather API reinitialized for {location_name}")
            
            # Update GUI location display
            self.gui.update_location_display(location_name)
            
            # Fetch new weather
            self.gui.update_weather()
        
        except ValueError as e:
            logger.error(f"Failed to change location: {e}")
    
    def run(self):
        """Start the application."""
        logger.info("Starting application...")
        
        # Load weather on startup
        self.gui.update_weather()
        
        # Schedule auto-refresh
        self.gui.schedule_auto_refresh()
        
        # Run GUI event loop
        self.gui.run()


def main():
    """Application entry point."""
    try:
        logger.info("=" * 60)
        logger.info("Cognitive Weather Oracle - Starting")
        logger.info("=" * 60)
        
        if not validate_configuration():
            sys.exit(1)
        
        app = CognitiveWeatherOracleApp()
        app.run()
    
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Application terminated")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()