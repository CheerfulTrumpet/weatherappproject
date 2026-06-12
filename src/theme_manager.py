"""
Theme Manager Module
====================
Encapsulates all color schemes and visual theming logic.

This module demonstrates how to parameterize visual design, making it easy
to test different themes and extend the application with new color schemes.
"""

from dataclasses import dataclass
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class ColorScheme:
    """Represents a complete color theme."""
    
    bg_primary: str      # Main background color
    bg_secondary: str    # Secondary background (for frames/containers)
    text_primary: str    # Primary text color (headers, labels)
    text_secondary: str  # Secondary text color (descriptions, details)
    accent: str          # Accent color (buttons, highlights)
    border: str          # Border/divider color
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for easy access."""
        return {
            'bg_primary': self.bg_primary,
            'bg_secondary': self.bg_secondary,
            'text_primary': self.text_primary,
            'text_secondary': self.text_secondary,
            'accent': self.accent,
            'border': self.border
        }


class ThemeManager:
    """
    Manages color schemes and theming for different weather conditions.
    
    This class ensures visual design is data-driven and easy to modify.
    Each weather condition has a carefully chosen color palette that
    reinforces the cognitive narrative.
    
    Design Philosophy:
        - Clear: Bright, light colors (hope, energy, clarity)
        - Cloudy: Muted, medium tones (contemplation, balance)
        - Rainy: Cool, deep blues (reflection, grounding)
        - Stormy: Dark, intense colors (volatility, danger)
        - Snowy: Whites and cool pastels (serenity, stillness)
        - Misty: Soft, ambiguous grays (uncertainty, mystery)
    """
    
    # Carefully selected color schemes for each weather condition
    THEMES = {
        "clear": ColorScheme(
            bg_primary="#87CEEB",        # Sky blue
            bg_secondary="#E0F6FF",      # Light azure
            text_primary="#0C3D6E",      # Dark navy
            text_secondary="#1E5F8F",    # Medium blue
            accent="#FFD700",            # Gold (sun)
            border="#87CEEB"
        ),
        "cloudy": ColorScheme(
            bg_primary="#B0C4DE",        # Light steel blue
            bg_secondary="#D3D3D3",      # Light gray
            text_primary="#2F4F4F",      # Dark slate gray
            text_secondary="#696969",    # Dim gray
            accent="#708090",            # Slate gray
            border="#A9A9A9"
        ),
        "rainy": ColorScheme(
            bg_primary="#4A6FA5",        # Storm blue
            bg_secondary="#6C7D8F",      # Muted blue-gray
            text_primary="#E8F0F7",      # Very light blue
            text_secondary="#B8C5D6",    # Soft blue-gray
            accent="#87CEEB",            # Light blue (water)
            border="#5A7FB8"
        ),
        "stormy": ColorScheme(
            bg_primary="#2C3E50",        # Dark charcoal
            bg_secondary="#34495E",      # Darker slate
            text_primary="#ECF0F1",      # Off-white
            text_secondary="#BDC3C7",    # Light gray
            accent="#E74C3C",            # Red (danger/electricity)
            border="#1A252F"
        ),
        "snowy": ColorScheme(
            bg_primary="#F0F8FF",        # Alice blue (very light)
            bg_secondary="#FFFAFA",      # Snow white
            text_primary="#1C1C1C",      # Nearly black
            text_secondary="#4F4F4F",    # Dark gray
            accent="#B0E0E6",            # Powder blue
            border="#D3D3D3"
        ),
        "misty": ColorScheme(
            bg_primary="#9BA3A8",        # Light taupe
            bg_secondary="#B8BFBF",      # Soft gray
            text_primary="#EFEFEF",      # Off-white
            text_secondary="#A0A0A0",    # Medium gray
            accent="#C0C0C0",            # Silver
            border="#808080"
        ),
        "moderate": ColorScheme(
            bg_primary="#D3D3D3",        # Light gray (neutral)
            bg_secondary="#E8E8E8",      # Very light gray
            text_primary="#333333",      # Dark gray
            text_secondary="#666666",    # Medium gray
            accent="#4169E1",            # Royal blue
            border="#BFBFBF"
        )
    }
    
    @classmethod
    def get_theme(cls, condition: str) -> ColorScheme:
        """
        Retrieve color scheme for a given weather condition.
        
        Args:
            condition: Weather condition string (from WeatherData.weather_condition)
        
        Returns:
            ColorScheme: Color palette for the condition
        """
        condition_lower = condition.lower()
        
        if condition_lower in cls.THEMES:
            return cls.THEMES[condition_lower]
        else:
            logger.warning(f"Unknown weather condition '{condition}', using 'moderate' theme")
            return cls.THEMES["moderate"]
    
    @classmethod
    def get_all_themes(cls) -> Dict[str, ColorScheme]:
        """Get all available themes."""
        return cls.THEMES.copy()
    
    @classmethod
    def validate_theme(cls, theme: ColorScheme) -> bool:
        """
        Validate that a theme has all required colors.
        
        Args:
            theme: ColorScheme to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        required_fields = {'bg_primary', 'bg_secondary', 'text_primary', 
                          'text_secondary', 'accent', 'border'}
        theme_fields = set(theme.to_dict().keys())
        return required_fields == theme_fields


class AccessibilityHelper:
    """
    Provides accessibility utilities for color contrast and readability.
    
    In a production application, this ensures WCAG AA compliance.
    """
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def calculate_luminance(rgb: Tuple[int, int, int]) -> float:
        """
        Calculate relative luminance (WCAG standard).
        
        Higher value = lighter color.
        """
        r, g, b = [x / 255.0 for x in rgb]
        
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    @staticmethod
    def contrast_ratio(color1: str, color2: str) -> float:
        """
        Calculate contrast ratio between two colors (WCAG standard).
        
        Ratio >= 4.5 = AA compliant
        Ratio >= 7 = AAA compliant
        """
        rgb1 = AccessibilityHelper.hex_to_rgb(color1)
        rgb2 = AccessibilityHelper.hex_to_rgb(color2)
        
        lum1 = AccessibilityHelper.calculate_luminance(rgb1)
        lum2 = AccessibilityHelper.calculate_luminance(rgb2)
        
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        
        return (lighter + 0.05) / (darker + 0.05)
    
    @classmethod
    def validate_theme_accessibility(cls, theme: ColorScheme) -> Dict[str, float]:
        """
        Check contrast ratios in a theme.
        
        Args:
            theme: ColorScheme to validate
        
        Returns:
            Dict: Contrast ratios for different element pairs
        """
        return {
            "primary_text_contrast": cls.contrast_ratio(
                theme.text_primary, theme.bg_primary
            ),
            "secondary_text_contrast": cls.contrast_ratio(
                theme.text_secondary, theme.bg_secondary
            ),
            "accent_contrast": cls.contrast_ratio(
                theme.accent, theme.bg_primary
            )
        }
