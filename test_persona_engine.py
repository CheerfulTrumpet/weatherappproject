"""
Test Suite for Persona Engine Module
=====================================

Tests cover:
- Mood determination from weather conditions
- Narrative generation across different persona styles
- Insight extraction and cognitive factor analysis
- Action recommendations based on weather state
"""

import pytest
from src.persona_engine import (
    PersonaEngine,
    PersonaStyle,
    CognitiveSummary
)


# ============================================================================
# PERSONA STYLE TESTS
# ============================================================================

class TestPersonaStyles:
    """Tests for different persona writing styles."""
    
    @pytest.mark.unit
    def test_all_persona_styles_exist(self):
        """Test that all expected persona styles are available."""
        expected_styles = ["philosopher", "poet", "scientist", "minimalist"]
        for style_name in expected_styles:
            style = PersonaStyle(style_name)
            assert style.value == style_name


# ============================================================================
# MOOD DETERMINATION TESTS
# ============================================================================

class TestMoodDetermination:
    """Tests for weather-to-mood mapping."""
    
    @pytest.mark.unit
    def test_mood_clear_weather(self, philosopher_engine, clear_weather_data):
        """Test mood for clear weather."""
        mood = philosopher_engine._determine_mood(clear_weather_data)
        assert "Clarity" in mood
        assert "Vitality" in mood
    
    @pytest.mark.unit
    def test_mood_rainy_weather(self, philosopher_engine, rainy_weather_data):
        """Test mood for rainy weather."""
        mood = philosopher_engine._determine_mood(rainy_weather_data)
        assert "Reflective" in mood
        assert "Grounded" in mood
    
    @pytest.mark.unit
    def test_mood_stormy_weather(self, philosopher_engine, stormy_weather_data):
        """Test mood for stormy weather."""
        mood = philosopher_engine._determine_mood(stormy_weather_data)
        assert "Volatile" in mood or "High-Stakes" in mood
    
    @pytest.mark.unit
    def test_mood_cloudy_weather(self, philosopher_engine, cloudy_weather_data):
        """Test mood for cloudy weather."""
        mood = philosopher_engine._determine_mood(cloudy_weather_data)
        assert "Contemplative" in mood or "Introspective" in mood
    
    @pytest.mark.unit
    def test_mood_snowy_weather(self, philosopher_engine, snowy_weather_data):
        """Test mood for snowy weather."""
        mood = philosopher_engine._determine_mood(snowy_weather_data)
        assert "Serene" in mood or "Blank Slate" in mood
    
    @pytest.mark.unit
    def test_mood_temperature_modulation_cold(self, philosopher_engine, extreme_cold_data):
        """Test that mood is modulated by extremely cold temperatures."""
        mood = philosopher_engine._determine_mood(extreme_cold_data)
        assert "Cold" in mood or "Invigorating" in mood
    
    @pytest.mark.unit
    def test_mood_temperature_modulation_hot(self, philosopher_engine, extreme_heat_data):
        """Test that mood is modulated by extremely hot temperatures."""
        mood = philosopher_engine._determine_mood(extreme_heat_data)
        assert "Heat" in mood or "Lethargic" in mood


# ============================================================================
# NARRATIVE GENERATION TESTS
# ============================================================================

class TestNarrativeGeneration:
    """Tests for prose narrative generation."""
    
    @pytest.mark.unit
    def test_narrative_includes_temperature(self, philosopher_engine, clear_weather_data):
        """Test that narratives include temperature data."""
        narrative = philosopher_engine._narrative_philosopher(clear_weather_data)
        assert "72" in narrative or "72.0" in narrative
    
    @pytest.mark.unit
    def test_narrative_includes_humidity(self, philosopher_engine, rainy_weather_data):
        """Test that narratives include humidity data."""
        narrative = philosopher_engine._narrative_philosopher(rainy_weather_data)
        assert "85" in narrative  # humidity %
    
    @pytest.mark.unit
    def test_narrative_includes_wind(self, philosopher_engine, stormy_weather_data):
        """Test that narratives include wind speed for stormy conditions."""
        narrative = philosopher_engine._narrative_philosopher(stormy_weather_data)
        assert "25" in narrative  # wind speed
    
    @pytest.mark.unit
    def test_philosopher_narrative_style(self, philosopher_engine, clear_weather_data):
        """Test that philosopher narrative is contemplative."""
        narrative = philosopher_engine._narrative_philosopher(clear_weather_data)
        assert len(narrative) > 100  # Philosopher style is verbose
        assert any(word in narrative.lower() for word in ["clarity", "expansion", "vitality"])
    
    @pytest.mark.unit
    def test_poet_narrative_style(self, poet_engine, clear_weather_data):
        """Test that poet narrative is concise and metaphorical."""
        narrative = poet_engine._narrative_poet(clear_weather_data)
        # Poet style includes emoji and is shorter
        assert any(emoji in narrative for emoji in ["☀️", "☁️", "🌧️", "⛈️"])
    
    @pytest.mark.unit
    def test_scientist_narrative_style(self, scientist_engine, clear_weather_data):
        """Test that scientist narrative is data-focused."""
        narrative = scientist_engine._narrative_scientist(clear_weather_data)
        assert "temperature" in narrative.lower()
        assert "humidity" in narrative.lower() or "relative" in narrative.lower()
    
    @pytest.mark.unit
    def test_minimalist_narrative_style(self, minimalist_engine, clear_weather_data):
        """Test that minimalist narrative is very brief."""
        narrative = minimalist_engine._narrative_minimalist(clear_weather_data)
        # Minimalist style should be < 50 chars typically
        assert len(narrative) < 100
    
    @pytest.mark.unit
    def test_narrative_for_all_conditions(self, philosopher_engine):
        """Test that engine generates narrative for all weather conditions."""
        from tests.conftest import WEATHER_CONDITIONS
        
        test_data_map = {
            "clear": WeatherData(70, 70, 50, 1013, "Clear", 5, 10, "01d"),
            "cloudy": WeatherData(65, 65, 60, 1012, "Overcast", 6, 80, "04d"),
            "rainy": WeatherData(55, 52, 85, 1005, "Rain", 12, 95, "10d"),
            "stormy": WeatherData(62, 55, 90, 995, "Thunderstorm", 25, 100, "11d"),
            "snowy": WeatherData(28, 18, 70, 1015, "Snow", 8, 90, "13d"),
            "misty": WeatherData(55, 55, 85, 1010, "Mist", 5, 70, "50d"),
        }
        
        from src.weather_api import WeatherData
        
        for condition in WEATHER_CONDITIONS:
            weather_data = test_data_map.get(condition)
            if weather_data:
                narrative = philosopher_engine._create_narrative(weather_data)
                assert len(narrative) > 0
                assert isinstance(narrative, str)


# ============================================================================
# INSIGHT EXTRACTION TESTS
# ============================================================================

class TestInsightExtraction:
    """Tests for extracting cognitive insights from weather data."""
    
    @pytest.mark.unit
    def test_insights_returned_as_list(self, philosopher_engine, clear_weather_data):
        """Test that insights are returned as a list."""
        insights = philosopher_engine._extract_insights(clear_weather_data)
        assert isinstance(insights, list)
        assert len(insights) > 0
    
    @pytest.mark.unit
    def test_insights_include_emoji_labels(self, philosopher_engine, clear_weather_data):
        """Test that insights include emoji labels for accessibility."""
        insights = philosopher_engine._extract_insights(clear_weather_data)
        # Join insights and check for emoji
        all_insights = " ".join(insights)
        assert any(char in all_insights for char in ["☀️", "💧", "💨", "❄️", "☁️"])
    
    @pytest.mark.unit
    def test_cold_temperature_insight(self, philosopher_engine, extreme_cold_data):
        """Test that cold temperatures generate appropriate insights."""
        insights = philosopher_engine._extract_insights(extreme_cold_data)
        cold_insights = [i for i in insights if "cold" in i.lower()]
        assert len(cold_insights) > 0
    
    @pytest.mark.unit
    def test_heat_temperature_insight(self, philosopher_engine, extreme_heat_data):
        """Test that heat generates appropriate insights."""
        insights = philosopher_engine._extract_insights(extreme_heat_data)
        heat_insights = [i for i in insights if "heat" in i.lower()]
        assert len(heat_insights) > 0
    
    @pytest.mark.unit
    def test_humidity_insight(self, philosopher_engine, high_humidity_data):
        """Test humidity-related insights."""
        insights = philosopher_engine._extract_insights(high_humidity_data)
        humidity_insights = [i for i in insights if "humid" in i.lower()]
        assert len(humidity_insights) > 0
    
    @pytest.mark.unit
    def test_wind_insight(self, philosopher_engine, stormy_weather_data):
        """Test wind-related insights for stormy conditions."""
        insights = philosopher_engine._extract_insights(stormy_weather_data)
        wind_insights = [i for i in insights if "wind" in i.lower()]
        assert len(wind_insights) > 0
    
    @pytest.mark.unit
    def test_cloudiness_insight(self, philosopher_engine, cloudy_weather_data):
        """Test insights about cloud cover."""
        insights = philosopher_engine._extract_insights(cloudy_weather_data)
        cloud_insights = [i for i in insights if "cloud" in i.lower()]
        assert len(cloud_insights) > 0


# ============================================================================
# ACTION RECOMMENDATION TESTS
# ============================================================================

class TestActionRecommendations:
    """Tests for activity recommendations based on weather."""
    
    @pytest.mark.unit
    def test_recommendation_returned_as_string(self, philosopher_engine, clear_weather_data):
        """Test that recommendations are returned as strings."""
        rec = philosopher_engine._action_recommendation(clear_weather_data)
        assert isinstance(rec, str)
        assert len(rec) > 0
    
    @pytest.mark.unit
    def test_clear_weather_recommendations(self, philosopher_engine, clear_weather_data):
        """Test recommendations for clear weather."""
        rec = philosopher_engine._action_recommendation(clear_weather_data)
        # Should mention analytical or external activities
        assert any(keyword in rec.lower() for keyword in ["focused", "planning", "social"])
    
    @pytest.mark.unit
    def test_rainy_weather_recommendations(self, philosopher_engine, rainy_weather_data):
        """Test recommendations for rainy weather."""
        rec = philosopher_engine._action_recommendation(rainy_weather_data)
        # Should mention introspective activities
        assert any(keyword in rec.lower() for keyword in ["reflection", "reading", "emotional"])
    
    @pytest.mark.unit
    def test_stormy_weather_recommendations(self, philosopher_engine, stormy_weather_data):
        """Test recommendations for stormy weather."""
        rec = philosopher_engine._action_recommendation(stormy_weather_data)
        # Should mention challenging activities
        assert any(keyword in rec.lower() for keyword in ["challenging", "intense", "resilience"])
    
    @pytest.mark.unit
    def test_extreme_heat_adds_caveat(self, philosopher_engine, extreme_heat_data):
        """Test that extreme heat adds temperature caveats."""
        rec = philosopher_engine._action_recommendation(extreme_heat_data)
        assert "hydrated" in rec.lower() or "heat" in rec.lower()
    
    @pytest.mark.unit
    def test_extreme_cold_adds_caveat(self, philosopher_engine, extreme_cold_data):
        """Test that extreme cold adds temperature caveats."""
        rec = philosopher_engine._action_recommendation(extreme_cold_data)
        assert "warm" in rec.lower() or "cold" in rec.lower()


# ============================================================================
# COGNITIVE FACTOR ANALYSIS TESTS
# ============================================================================

class TestCognitiveFactorAnalysis:
    """Tests for deep-dive cognitive factor analysis."""
    
    @pytest.mark.unit
    def test_cognitive_factors_returned_as_dict(self, philosopher_engine, clear_weather_data):
        """Test that cognitive factors are returned as a dictionary."""
        factors = philosopher_engine._analyze_cognitive_factors(clear_weather_data)
        assert isinstance(factors, dict)
    
    @pytest.mark.unit
    def test_cognitive_factors_include_all_categories(self, philosopher_engine, clear_weather_data):
        """Test that all expected cognitive factor categories are present."""
        factors = philosopher_engine._analyze_cognitive_factors(clear_weather_data)
        expected_keys = {
            "circadian_rhythm_impact",
            "thermal_comfort_zone",
            "humidity_embodiment",
            "wind_volatility",
            "light_diffusion",
            "barometric_pressure"
        }
        assert expected_keys == set(factors.keys())
    
    @pytest.mark.unit
    def test_cognitive_factors_have_string_values(self, philosopher_engine, clear_weather_data):
        """Test that all cognitive factors have string explanations."""
        factors = philosopher_engine._analyze_cognitive_factors(clear_weather_data)
        for key, value in factors.items():
            assert isinstance(value, str)
            assert len(value) > 20  # Should be substantive explanation


# ============================================================================
# SUMMARY GENERATION TESTS
# ============================================================================

class TestSummaryGeneration:
    """Tests for complete summary generation."""
    
    @pytest.mark.unit
    def test_summary_is_cognitive_summary(self, philosopher_engine, clear_weather_data):
        """Test that generate_summary returns CognitiveSummary object."""
        summary = philosopher_engine.generate_summary(clear_weather_data)
        assert isinstance(summary, CognitiveSummary)
    
    @pytest.mark.unit
    def test_summary_contains_all_fields(self, philosopher_engine, clear_weather_data):
        """Test that summary contains all expected fields."""
        summary = philosopher_engine.generate_summary(clear_weather_data)
        assert hasattr(summary, 'primary_mood')
        assert hasattr(summary, 'narrative_summary')
        assert hasattr(summary, 'key_insights')
        assert hasattr(summary, 'actionable_sentiment')
        assert hasattr(summary, 'cognitive_factors')
    
    @pytest.mark.unit
    def test_summary_fields_have_correct_types(self, philosopher_engine, clear_weather_data):
        """Test that summary fields have correct data types."""
        summary = philosopher_engine.generate_summary(clear_weather_data)
        assert isinstance(summary.primary_mood, str)
        assert isinstance(summary.narrative_summary, str)
        assert isinstance(summary.key_insights, list)
        assert isinstance(summary.actionable_sentiment, str)
        assert isinstance(summary.cognitive_factors, dict)
    
    @pytest.mark.unit
    def test_summary_across_all_personas(
        self,
        clear_weather_data,
        philosopher_engine,
        poet_engine,
        scientist_engine,
        minimalist_engine
    ):
        """Test that summary generation works for all persona styles."""
        engines = [philosopher_engine, poet_engine, scientist_engine, minimalist_engine]
        
        for engine in engines:
            summary = engine.generate_summary(clear_weather_data)
            assert isinstance(summary, CognitiveSummary)
            assert summary.narrative_summary != ""
    
    @pytest.mark.unit
    def test_summary_varies_by_persona(self, clear_weather_data):
        """Test that different personas generate different narratives."""
        philosopher_summary = PersonaEngine(PersonaStyle.PHILOSOPHER).generate_summary(clear_weather_data)
        poet_summary = PersonaEngine(PersonaStyle.POET).generate_summary(clear_weather_data)
        
        # Narratives should be different
        assert philosopher_summary.narrative_summary != poet_summary.narrative_summary


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestPersonaEngineIntegration:
    """Integration tests for complete persona engine workflow."""
    
    @pytest.mark.integration
    def test_full_workflow_clear_weather(self, philosopher_engine, clear_weather_data):
        """Test complete workflow: data → mood → narrative → insights → recommendations."""
        summary = philosopher_engine.generate_summary(clear_weather_data)
        
        # Verify coherence: mood should relate to narrative
        assert "clear" in summary.narrative_summary.lower() or "clarity" in summary.narrative_summary.lower()
        
        # Insights should exist and be meaningful
        assert len(summary.key_insights) > 0
        assert all(isinstance(insight, str) for insight in summary.key_insights)
        
        # Recommendations should suggest external/active engagement
        assert any(word in summary.actionable_sentiment.lower() 
                  for word in ["focused", "planning", "social", "external"])
    
    @pytest.mark.integration
    def test_full_workflow_rainy_weather(self, philosopher_engine, rainy_weather_data):
        """Test complete workflow with rainy weather."""
        summary = philosopher_engine.generate_summary(rainy_weather_data)
        
        # Mood should reflect introspection
        assert "reflective" in summary.primary_mood.lower()
        
        # Recommendations should suggest internal/introspective activities
        assert any(word in summary.actionable_sentiment.lower() 
                  for word in ["reflection", "emotional", "meaningful"])
