"""
Cognitive Weather Oracle - Source Package

A sophisticated weather application that translates meteorological data
into emotionally-resonant, human-centric narratives informed by cognitive science.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .weather_api import WeatherAPI, WeatherData
from .persona_engine import PersonaEngine, PersonaStyle
from .gui import WeatherGUI
from .theme_manager import ThemeManager
from .icon_manager import IconAssetManager

__all__ = [
    'WeatherAPI',
    'WeatherData',
    'PersonaEngine',
    'PersonaStyle',
    'WeatherGUI',
    'ThemeManager',
    'IconAssetManager',
]
