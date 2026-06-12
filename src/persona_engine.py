"""
Persona Engine Module - Cognitive Weather Translation
The core feature translating meteorological data into psychological narratives.
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum
import logging

from .weather_api import WeatherData

logger = logging.getLogger(__name__)


class PersonaStyle(Enum):
    """Enumeration of available persona writing styles."""
    PHILOSOPHER = "philosopher"
    POET = "poet"
    SCIENTIST = "scientist"
    MINIMALIST = "minimalist"


@dataclass
class CognitiveSummary:
    """Structured output from the Persona Engine."""
    primary_mood: str
    narrative_summary: str
    key_insights: List[str]
    actionable_sentiment: str
    cognitive_factors: Dict[str, str]


class PersonaEngine:
    """Translates weather data into cognitive narratives."""
    
    def __init__(self, persona: PersonaStyle = PersonaStyle.PHILOSOPHER):
        self.persona = persona
        logger.info(f"PersonaEngine initialized with {persona.value} persona")
    
    def generate_summary(self, weather: WeatherData) -> CognitiveSummary:
        """Generate comprehensive cognitive narrative from weather data."""
        return CognitiveSummary(
            primary_mood=self._determine_mood(weather),
            narrative_summary=self._create_narrative(weather),
            key_insights=self._extract_insights(weather),
            actionable_sentiment=self._action_recommendation(weather),
            cognitive_factors=self._analyze_cognitive_factors(weather)
        )
    
    def _determine_mood(self, weather: WeatherData) -> str:
        """Map weather condition to emotional/cognitive state."""
        condition = weather.weather_condition
        temp = weather.temperature
        
        mood_mapping = {
            "clear": "Clarity & Vitality",
            "cloudy": "Contemplative & Introspective",
            "rainy": "Reflective & Grounded",
            "stormy": "Volatile & High-Stakes",
            "snowy": "Serene & Blank Slate",
            "misty": "Ambiguous & Veiled"
        }
        
        base_mood = mood_mapping.get(condition, "Moderate")
        
        if temp < 32:
            base_mood += " + Invigorating Cold"
        elif temp > 85:
            base_mood += " + Lethargic Heat"
        
        return base_mood
    
    def _create_narrative(self, weather: WeatherData) -> str:
        """Generate prose narrative based on cognitive principles."""
        if self.persona == PersonaStyle.PHILOSOPHER:
            return self._narrative_philosopher(weather)
        elif self.persona == PersonaStyle.POET:
            return self._narrative_poet(weather)
        elif self.persona == PersonaStyle.SCIENTIST:
            return self._narrative_scientist(weather)
        elif self.persona == PersonaStyle.MINIMALIST:
            return self._narrative_minimalist(weather)
        else:
            return self._narrative_philosopher(weather)
    
    def _narrative_philosopher(self, weather: WeatherData) -> str:
        """Philosophical, contemplative narrative."""
        temp = weather.temperature
        humidity = weather.humidity
        wind = weather.wind_speed
        condition = weather.weather_condition
        
        narratives = {
            "clear": (
                f"The atmosphere displays clarity and expansiveness. "
                f"At {temp:.0f}°F, conditions exude an accessible vitality. "
                f"The cognitive landscape favors focus, planning, and external engagement. "
                f"Humidity at {humidity}% suggests minimal psychological burden. "
                f"This is a moment of external orientation, where the world's possibilities feel tangible."
            ),
            "cloudy": (
                f"The sky signals introspection and diffused focus. "
                f"At {temp:.0f}°F with {humidity}% humidity, conditions invite "
                f"internal reflection. Ideal for ideation, creative problem-solving, and contemplation. "
                f"The diffused light naturally supports non-linear thinking."
            ),
            "rainy": (
                f"Water descends with grounding presence. "
                f"At {temp:.0f}°F and {humidity}% humidity, atmospheric density supports depth. "
                f"This is an invitation to reflective work, emotional processing, and meaningful connection. "
                f"The rhythm of rain anchors attention inward."
            ),
            "stormy": (
                f"Atmospheric intensity peaks. "
                f"At {temp:.0f}°F with wind at {wind:.1f} mph, conditions demand presence and adaptability. "
                f"This is not a time for passivity. Channel the intensity into deliberate action. "
                f"Leverage the natural arousal for challenging work."
            ),
            "snowy": (
                f"Silence and stillness descend. "
                f"At {temp:.0f}°F, snow transforms the world into a blank slate. "
                f"This supports deep contemplation, creative work, and strategic thinking. "
                f"The visual quietness maps to psychological calm."
            ),
            "misty": (
                f"Boundaries dissolve into ambiguity. "
                f"At {temp:.0f}°F with obscured horizons, certainty fades. "
                f"This creates space for exploratory thinking and creative risk-taking. "
                f"Embrace the mystery; let it fuel imagination."
            )
        }
        return narratives.get(condition, "Moderate conditions prevail.")
    
    def _narrative_poet(self, weather: WeatherData) -> str:
        """Poetic, metaphorical narrative."""
        condition = weather.weather_condition
        temp = weather.temperature
        
        narratives = {
            "clear": (
                f"Light spills across the sky. At {temp:.0f}°F, "
                f"the world glitters with promise. All is visible. All is possible. "
                f"This is the weather of revelation."
            ),
            "cloudy": (
                f"Soft veils drape the heavens. At {temp:.0f}°F, "
                f"the light grows diffuse and contemplative. Imagination awakens. "
                f"This is the weather of the inward gaze."
            ),
            "rainy": (
                f"Water whispers from above. At {temp:.0f}°F, "
                f"the earth drinks deep. All is soft, all is flowing. "
                f"This is the weather of emotion and renewal."
            ),
            "stormy": (
                f"The sky roars. At {temp:.0f}°F, power and fury dance. "
                f"Stand tall. This is the weather of transformation and courage."
            ),
            "snowy": (
                f"Silence crystallizes. At {temp:.0f}°F, the world sleeps in white. "
                f"All is hushed. All is still. This is the weather of dreams."
            ),
            "misty": (
                f"Mystery shrouds the world. At {temp:.0f}°F, boundaries blur. "
                f"The unknown beckons. This is the weather of magic."
            )
        }
        return narratives.get(condition, "The world continues, as it always does.")
    
    def _narrative_scientist(self, weather: WeatherData) -> str:
        """Data-focused, analytical narrative."""
        temp = weather.temperature
        humidity = weather.humidity
        pressure = weather.pressure
        wind = weather.wind_speed
        condition = weather.weather_condition
        
        narratives = {
            "clear": (
                f"Clear conditions: visibility optimal. Temperature {temp:.0f}°F, "
                f"humidity {humidity}%, pressure {pressure} hPa, wind {wind:.1f} mph. "
                f"High-pressure system supports stable atmospheric conditions. "
                f"Clear skies increase solar radiation exposure and vitamin D synthesis."
            ),
            "cloudy": (
                f"Overcast conditions present. Temperature {temp:.0f}°F, "
                f"humidity {humidity}%, pressure {pressure} hPa. "
                f"Cloud cover reduces direct solar radiation. Diffuse light scatters uniformly. "
                f"Cognitive performance often improves under these reduced-glare conditions."
            ),
            "rainy": (
                f"Precipitation detected. Temperature {temp:.0f}°F, "
                f"humidity {humidity}%, pressure {pressure} hPa. "
                f"Water cycle activity peaks. Negative ion concentration increases near precipitation. "
                f"Barometric pressure typically drops with rain systems."
            ),
            "stormy": (
                f"High-energy atmospheric system. Temperature {temp:.0f}°F, "
                f"wind {wind:.1f} mph, pressure {pressure} hPa. "
                f"Electrostatic potential increases. Wind shear and turbulence present. "
                f"Barometric pressure at minimum. System exhibits peak dynamical activity."
            ),
            "snowy": (
                f"Frozen precipitation. Temperature {temp:.0f}°F. "
                f"Snow cover increases albedo (surface reflectivity). "
                f"Humidity {humidity}%. Thermal properties of snow insulate the ground. "
                f"Atmospheric dynamics favor stratification over mixing."
            ),
            "misty": (
                f"Water vapor condensation at surface level. Temperature {temp:.0f}°F, "
                f"humidity {humidity}%. Visibility reduced. Light scatters through water droplets. "
                f"Low-level cloud formation with aerosol nucleation."
            )
        }
        return narratives.get(condition, f"Temperature {temp:.0f}°F, conditions moderate.")
    
    def _narrative_minimalist(self, weather: WeatherData) -> str:
        """Sparse, concise narrative."""
        condition = weather.weather_condition
        temp = weather.temperature
        
        narratives = {
            "clear": f"Clear. {temp:.0f}°F. Focus possible.",
            "cloudy": f"Overcast. {temp:.0f}°F. Introspection invited.",
            "rainy": f"Rain. {temp:.0f}°F. Reflection time.",
            "stormy": f"Storm. {temp:.0f}°F. Stay present.",
            "snowy": f"Snow. {temp:.0f}°F. Stillness.",
            "misty": f"Mist. {temp:.0f}°F. Mystery."
        }
        return narratives.get(condition, f"Conditions: {temp:.0f}°F")
    
    def _extract_insights(self, weather: WeatherData) -> List[str]:
        """Extract key psychological insights."""
        insights = []
        
        if weather.temperature < 32:
            insights.append("Cold Clarity: Sub-freezing temps sharpen alertness and mental processing.")
        elif 32 <= weather.temperature < 55:
            insights.append("Invigorating Cool: This range optimizes cognitive performance.")
        elif 55 <= weather.temperature <= 75:
            insights.append("Optimal Comfort: Peak zone for physical and mental function.")
        elif 75 < weather.temperature <= 85:
            insights.append("Thermal Stress: Heat begins to elevate cognitive load.")
        elif weather.temperature > 85:
            insights.append("Heat Burden: High temps impair executive function and reasoning.")
        
        if weather.humidity > 80:
            insights.append("High Moisture: Excessive humidity creates embodied discomfort and intensity.")
        elif weather.humidity < 30:
            insights.append("Dry Air: Low humidity may cause subtle discomfort and attention drift.")
        
        if weather.wind_speed > 20:
            insights.append("High Winds: Environmental chaos demands adaptive attention and vigilance.")
        elif weather.wind_speed > 10:
            insights.append("Moderate Breeze: Slight instability can promote alertness or mild agitation.")
        
        if weather.cloudiness > 80:
            insights.append("Heavy Overcast: External certainty fades, amplifying internal resources.")
        elif weather.cloudiness < 20:
            insights.append("Clear Skies: High external certainty supports confidence and possibility.")
        
        if weather.pressure < 1010:
            insights.append("Low Pressure: Can amplify mood sensitivity and emotional reactivity.")
        elif weather.pressure > 1020:
            insights.append("High Pressure: Associated with stability and psychological wellbeing.")
        
        if not insights:
            insights.append("Moderate Conditions: Standard cognitive baseline maintained.")
        
        return insights
    
    def _action_recommendation(self, weather: WeatherData) -> str:
        """Suggest activities aligned with cognitive state."""
        condition = weather.weather_condition
        temp = weather.temperature
        
        recommendations = {
            "clear": (
                "Best for: Focused analytical work, strategic planning, social engagement, "
                "decision-making, and external activities. Leverage the mental clarity—tackle "
                "your hardest problems now."
            ),
            "cloudy": (
                "Best for: Creative ideation, writing, deep analysis, brainstorming, and artistic work. "
                "The diffused focus naturally supports non-linear thinking and innovation."
            ),
            "rainy": (
                "Best for: Reflective work, emotional processing, meaningful conversations, "
                "reading, and learning. The grounding presence supports depth and nuance."
            ),
            "stormy": (
                "Best for: Challenging physical tasks, intense focused work, confronting difficulties, "
                "and resilience-building. Channel the intensity into deliberate action."
            ),
            "snowy": (
                "Best for: Meditation and contemplation, creative writing, solitude and rest, "
                "deep focus. The silence supports introspection and strategic thinking."
            ),
            "misty": (
                "Best for: Exploratory thinking, hypothesis generation, creative risk-taking. "
                "Embrace the ambiguity; let it fuel imagination."
            )
        }
        
        base_rec = recommendations.get(condition, "Align activities with your energy level.")
        
        if temp < 32:
            base_rec += " (Ensure adequate warmth for safety and comfort.)"
        elif temp > 85:
            base_rec += " (Stay hydrated; avoid peak heat hours for strenuous activity.)"
        
        return base_rec
    
    def _analyze_cognitive_factors(self, weather: WeatherData) -> Dict[str, str]:
        """Perform deep-dive analysis of cognitive factors."""
        return {
            "circadian_rhythm": (
                "Daylight and cloudiness affect melatonin and cortisol. "
                f"{'Clear skies boost alertness.' if weather.cloudiness < 50 else 'Overcast softens circadian peaks.'}"
            ),
            "thermal_comfort": (
                f"At {weather.temperature:.0f}°F, "
                f"{'optimal comfort zone (55-75°F) supports focus.' if 55 <= weather.temperature <= 75 else 'thermal stress affects cognition.'}"
            ),
            "humidity_effect": (
                f"Humidity at {weather.humidity}% creates "
                f"{'minimal burden' if weather.humidity < 50 else 'heightened embodied perception.'}"
            ),
            "wind_impact": (
                f"Wind at {weather.wind_speed:.1f} mph "
                f"{'suggests calm, stable conditions.' if weather.wind_speed < 10 else 'demands adaptive attention.'}"
            ),
            "light_quality": (
                f"Cloud cover at {weather.cloudiness}% "
                f"{'allows direct focus' if weather.cloudiness < 30 else 'promotes introspection.'}"
            ),
            "pressure_effect": (
                f"Pressure at {weather.pressure} hPa "
                f"{'supports stability' if weather.pressure > 1015 else 'may amplify mood sensitivity.'}"
            )
        }
