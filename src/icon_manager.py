"""
Icon Manager - Weather emoji mapping
"""

import logging

logger = logging.getLogger(__name__)


class IconAssetManager:
    """Manages weather icon assets."""
    
    EMOJI_MAP = {
        "clear": "☀️",
        "cloudy": "☁️",
        "rainy": "🌧️",
        "stormy": "⛈️",
        "snowy": "❄️",
        "misty": "🌫️",
        "moderate": "🌤️"
    }
    
    @staticmethod
    def get_emoji(condition: str) -> str:
        """Get emoji for weather condition."""
        condition = condition.lower()
        return IconAssetManager.EMOJI_MAP.get(condition, "🌍")
    
    @staticmethod
    def get_ctk_image(condition: str, size: tuple = (150, 150)):
        """Placeholder for CTkImage support."""
        return None
