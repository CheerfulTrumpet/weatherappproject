"""
Integration Test Suite
======================

End-to-end tests verifying complete workflows across multiple system components.

These tests verify that all modules work together correctly in realistic scenarios.
"""

import pytest
from src.weather_api import WeatherAPI, WeatherData, MockWeatherAPI
from src.persona_engine import PersonaEngine, PersonaStyle
from src.theme_manager import ThemeManager, AccessibilityHelper
from src.icon_manager import IconAssetManager


# ============================================================================
# COMPLETE WORKFLOW TESTS
# ============================================================================

class TestCompleteWeatherWorkflow:
    """End-to-end tests for the complete weather data → narrative → theme flow."""
    
    @pytest.mark.integration
    def test_clear_weather_workflow(self, clear_weather_data):
        """Test complete workflow for clear weather conditions."""
        # 1. Have weather data
        assert clear_weather_data.temperature == 72.0
        assert clear_weather_data.weather_condition == "clear"
        
        # 2. Generate cognitive narrative
        engine = PersonaEngine(PersonaStyle.PHILOSOPHER)
        summary = engine.generate_summary(clear_weather_data)
        
        assert "Clarity" in summary.primary_mood
        assert len(summary.narrative_summary) > 0
        assert len(summary.key_insights) > 0
        
        # 3. Get theme
        theme = ThemeManager.get_theme(clear_weather_data.weather_condition)
        assert theme.bg_primary == "#87CEEB"  # Sky blue
        
        # 4. Get icon
        emoji = IconAssetManager.get_emoji(clear_weather_data.weather_condition)
        assert emoji == "☀️"
        
        # Verify accessibility
        contrasts = AccessibilityHelper.validate_theme_accessibility(theme)
        assert contrasts["primary_text_contrast"] >= 4.5
    
    @pytest.mark.integration
    def test_rainy_weather_workflow(self, rainy_weather_data):
        """Test complete workflow for rainy weather conditions."""
        # Weather data
        assert rainy_weather_data.weather_condition == "rainy"
        assert rainy_weather_data.humidity == 85
        
        # Narrative generation
        engine = PersonaEngine(PersonaStyle.POET)
        summary = engine.generate_summary(rainy_weather_data)
        
        assert "Reflective" in summary.primary_mood
        assert len(summary.narrative_summary) > 0
        
        # Theme
        theme = ThemeManager.get_theme(rainy_weather_data.weather_condition)
        assert theme.bg_primary == "#4A6FA5"
        
        # Icon
        emoji = IconAssetManager.get_emoji(rainy_weather_data.weather_condition)
        assert emoji == "🌧️"
    
    @pytest.mark.integration
    def test_stormy_weather_workflow(self, stormy_weather_data):
        """Test complete workflow for stormy weather conditions."""
        # Weather data
        assert stormy_weather_data.weather_condition == "stormy"
        assert stormy_weather_data.wind_speed == 25.0
        
        # Narrative generation
        engine = PersonaEngine(PersonaStyle.SCIENTIST)
        summary = engine.generate_summary(stormy_weather_data)
        
        assert "Volatile" in summary.primary_mood or "High-Stakes" in summary.primary_mood
        
        # Theme
        theme = ThemeManager.get_theme(stormy_weather_data.weather_condition)
        assert theme.accent == "#E74C3C"  # Red for danger
        
        # Icon
        emoji = IconAssetManager.get_emoji(stormy_weather_data.weather_condition)
        assert emoji == "⛈️"
    
    @pytest.mark.integration
    def test_all_weather_conditions_supported(self):
        """Test that all major weather conditions are fully supported."""
        from tests.conftest import WEATHER_CONDITIONS
        
        test_data_map = {
            "clear": WeatherData(70, 70, 50, 1013, "Clear", 5, 10, "01d"),
            "cloudy": WeatherData(65, 65, 60, 1012, "Overcast", 6, 80, "04d"),
            "rainy": WeatherData(55, 52, 85, 1005, "Rain", 12, 95, "10d"),
            "stormy": WeatherData(62, 55, 90, 995, "Thunderstorm", 25, 100, "11d"),
            "snowy": WeatherData(28, 18, 70, 1015, "Snow", 8, 90, "13d"),
            "misty": WeatherData(55, 55, 85, 1010, "Mist", 5, 70, "50d"),
        }
        
        for condition in WEATHER_CONDITIONS:
            weather_data = test_data_map.get(condition)
            if weather_data:
                # 1. Narrative
                engine = PersonaEngine()
                summary = engine.generate_summary(weather_data)
                assert summary is not None
                
                # 2. Theme
                theme = ThemeManager.get_theme(condition)
                assert theme is not None
                
                # 3. Icon
                emoji = IconAssetManager.get_emoji(condition)
                assert emoji is not None and emoji != ""


# ============================================================================
# MULTI-PERSONA CONSISTENCY TESTS
# ============================================================================

class TestMultiPersonaConsistency:
    """Tests verifying consistency across different persona styles."""
    
    @pytest.mark.integration
    def test_all_personas_generate_same_mood(self, clear_weather_data):
        """Test that all personas agree on primary mood for same weather."""
        personas = [
            PersonaStyle.PHILOSOPHER,
            PersonaStyle.POET,
            PersonaStyle.SCIENTIST,
            PersonaStyle.MINIMALIST
        ]
        
        moods = []
        for persona in personas:
            engine = PersonaEngine(persona)
            summary = engine.generate_summary(clear_weather_data)
            moods.append(summary.primary_mood)
        
        # All should have "Clarity" in mood
        assert all("Clarity" in mood for mood in moods)
    
    @pytest.mark.integration
    def test_all_personas_generate_same_insights(self, clear_weather_data):
        """Test that all personas extract the same cognitive insights."""
        personas = [
            PersonaStyle.PHILOSOPHER,
            PersonaStyle.POET,
            PersonaStyle.SCIENTIST,
            PersonaStyle.MINIMALIST
        ]
        
        all_insights = []
        for persona in personas:
            engine = PersonaEngine(persona)
            summary = engine.generate_summary(clear_weather_data)
            all_insights.append(summary.key_insights)
        
        # All should have at least one insight
        assert all(len(insights) > 0 for insights in all_insights)
    
    @pytest.mark.integration
    def test_narratives_differ_by_persona(self, clear_weather_data):
        """Test that different personas produce different narrative styles."""
        philosopher_engine = PersonaEngine(PersonaStyle.PHILOSOPHER)
        poet_engine = PersonaEngine(PersonaStyle.POET)
        minimalist_engine = PersonaEngine(PersonaStyle.MINIMALIST)
        
        philosopher_summary = philosopher_engine.generate_summary(clear_weather_data)
        poet_summary = poet_engine.generate_summary(clear_weather_data)
        minimalist_summary = minimalist_engine.generate_summary(clear_weather_data)
        
        # Narratives should be different lengths
        lengths = [
            len(philosopher_summary.narrative_summary),
            len(poet_summary.narrative_summary),
            len(minimalist_summary.narrative_summary)
        ]
        
        # At least two should be significantly different
        assert max(lengths) - min(lengths) > 100


# ============================================================================
# EXTREME CONDITIONS WORKFLOW TESTS
# ============================================================================

class TestExtremeConditionsWorkflow:
    """Tests for handling extreme weather conditions."""
    
    @pytest.mark.integration
    def test_extreme_heat_workflow(self, extreme_heat_data):
        """Test workflow handles extreme heat properly."""
        engine = PersonaEngine()
        summary = engine.generate_summary(extreme_heat_data)
        
        # Should mention heat impact
        assert any(word in summary.primary_mood.lower() 
                  for word in ["heat", "lethargic"])
        
        # Should have heat-related insights
        heat_insights = [i for i in summary.key_insights if "heat" in i.lower()]
        assert len(heat_insights) > 0
        
        # Recommendation should mention hydration
        assert "hydrat" in summary.actionable_sentiment.lower()
    
    @pytest.mark.integration
    def test_extreme_cold_workflow(self, extreme_cold_data):
        """Test workflow handles extreme cold properly."""
        engine = PersonaEngine()
        summary = engine.generate_summary(extreme_cold_data)
        
        # Should mention cold impact
        assert any(word in summary.primary_mood.lower() 
                  for word in ["cold", "invigorat"])
        
        # Should have cold-related insights
        cold_insights = [i for i in summary.key_insights if "cold" in i.lower()]
        assert len(cold_insights) > 0
        
        # Recommendation should mention warmth
        assert any(word in summary.actionable_sentiment.lower() 
                  for word in ["warm", "cold"])
    
    @pytest.mark.integration
    def test_high_humidity_workflow(self, high_humidity_data):
        """Test workflow handles high humidity properly."""
        engine = PersonaEngine()
        summary = engine.generate_summary(high_humidity_data)
        
        # Should have humidity insights
        humidity_insights = [i for i in summary.key_insights if "humid" in i.lower()]
        assert len(humidity_insights) > 0


# ============================================================================
# API INTEGRATION TESTS
# ============================================================================

class TestAPIIntegration:
    """Tests for API integration with other components."""
    
    @pytest.mark.integration
    def test_mock_api_to_narrative_workflow(self, mock_clear_api):
        """Test complete workflow using mock API."""
        # Fetch from API
        weather_data = mock_clear_api.fetch_weather()
        assert weather_data is not None
        
        # Generate narrative
        engine = PersonaEngine()
        summary = engine.generate_summary(weather_data)
        assert summary is not None
        
        # Get theme
        theme = ThemeManager.get_theme(weather_data.weather_condition)
        assert theme is not None
    
    @pytest.mark.integration
    def test_api_error_handling(self, mock_failing_api):
        """Test handling when API returns None."""
        weather_data = mock_failing_api.fetch_weather()
        
        # When API returns None, UI should handle gracefully
        assert weather_data is None
    
    @pytest.mark.integration
    def test_multiple_api_calls_consistency(self, mock_clear_api):
        """Test that multiple API calls return consistent data."""
        data1 = mock_clear_api.fetch_weather()
        data2 = mock_clear_api.fetch_weather()
        
        # Should return same data
        assert data1.temperature == data2.temperature
        assert data1.weather_condition == data2.weather_condition
        
        # Call count should increment
        assert mock_clear_api.call_count == 2


# ============================================================================
# PERFORMANCE AND CONSISTENCY TESTS
# ============================================================================

class TestPerformanceAndConsistency:
    """Tests for performance and consistency properties."""
    
    @pytest.mark.integration
    def test_narrative_generation_performance(self, clear_weather_data):
        """Test that narrative generation is reasonably fast."""
        import time
        
        engine = PersonaEngine()
        
        start = time.time()
        summary = engine.generate_summary(clear_weather_data)
        elapsed = time.time() - start
        
        # Should complete in < 1 second
        assert elapsed < 1.0
        assert summary is not None
    
    @pytest.mark.integration
    def test_theme_retrieval_performance(self):
        """Test that theme retrieval is very fast."""
        import time
        
        start = time.time()
        for _ in range(100):
            theme = ThemeManager.get_theme("clear")
        elapsed = time.time() - start
        
        # Should complete 100 retrievals in < 1 second
        assert elapsed < 1.0
    
    @pytest.mark.integration
    def test_repeated_narratives_are_consistent(self, clear_weather_data):
        """Test that repeated narrative generation is consistent."""
        engine = PersonaEngine(PersonaStyle.PHILOSOPHER)
        
        summary1 = engine.generate_summary(clear_weather_data)
        summary2 = engine.generate_summary(clear_weather_data)
        
        # Same weather should always generate same narrative
        assert summary1.narrative_summary == summary2.narrative_summary
        assert summary1.primary_mood == summary2.primary_mood


# ============================================================================
# DATA VALIDATION TESTS
# ============================================================================

class TestDataValidationIntegration:
    """Tests for data validation across system."""
    
    @pytest.mark.integration
    def test_weather_data_remains_valid_through_pipeline(self, clear_weather_data):
        """Test that WeatherData remains valid through entire pipeline."""
        # Original data
        assert clear_weather_data.temperature > 0
        assert 0 <= clear_weather_data.humidity <= 100
        assert 0 <= clear_weather_data.cloudiness <= 100
        
        # Through narrative generation
        engine = PersonaEngine()
        summary = engine.generate_summary(clear_weather_data)
        
        # Original data should be unchanged
        assert clear_weather_data.temperature == 72.0
        assert clear_weather_data.humidity == 45
    
    @pytest.mark.integration
    def test_theme_remains_valid_through_usage(self):
        """Test that theme remains valid through usage."""
        theme = ThemeManager.get_theme("clear")
        
        # Should be valid
        assert ThemeManager.validate_theme(theme)
        
        # Should remain valid after retrieval
        theme_again = ThemeManager.get_theme("clear")
        assert theme_again == theme
        assert ThemeManager.validate_theme(theme_again)


# ============================================================================
# USER WORKFLOW SIMULATION TESTS
# ============================================================================

class TestUserWorkflowSimulation:
    """Simulates realistic user workflows."""
    
    @pytest.mark.integration
    def test_app_startup_workflow(self):
        """Simulate complete app startup workflow."""
        # 1. Initialize API with mock data
        api = MockWeatherAPI(
            mock_data=WeatherData(70, 70, 50, 1013, "Clear Sky", 5, 10, "01d")
        )
        
        # 2. Fetch weather
        weather = api.fetch_weather()
        assert weather is not None
        
        # 3. Initialize persona engine
        engine = PersonaEngine(PersonaStyle.PHILOSOPHER)
        
        # 4. Generate narrative
        summary = engine.generate_summary(weather)
        assert summary is not None
        
        # 5. Get theme
        theme = ThemeManager.get_theme(weather.weather_condition)
        assert theme is not None
        
        # 6. Get icon
        emoji = IconAssetManager.get_emoji(weather.weather_condition)
        assert emoji is not None
    
    @pytest.mark.integration
    def test_user_refreshes_weather(self):
        """Simulate user clicking refresh button."""
        api = MockWeatherAPI(
            mock_data=WeatherData(72, 70, 50, 1013, "Clear Sky", 5, 10, "01d")
        )
        
        engine = PersonaEngine()
        
        # First refresh
        weather1 = api.fetch_weather()
        summary1 = engine.generate_summary(weather1)
        theme1 = ThemeManager.get_theme(weather1.weather_condition)
        
        # Second refresh (simulated)
        weather2 = api.fetch_weather()
        summary2 = engine.generate_summary(weather2)
        theme2 = ThemeManager.get_theme(weather2.weather_condition)
        
        # Should have same data (mock returns same thing)
        assert weather1.temperature == weather2.temperature
        assert summary1.primary_mood == summary2.primary_mood
        assert theme1.bg_primary == theme2.bg_primary
    
    @pytest.mark.integration
    def test_switching_between_personas(self, clear_weather_data):
        """Simulate user switching between different personas."""
        personas_to_try = [
            PersonaStyle.PHILOSOPHER,
            PersonaStyle.POET,
            PersonaStyle.SCIENTIST
        ]
        
        summaries = []
        for persona in personas_to_try:
            engine = PersonaEngine(persona)
            summary = engine.generate_summary(clear_weather_data)
            summaries.append(summary)
        
        # All should have narratives
        assert all(s.narrative_summary for s in summaries)
        
        # Narratives should vary by persona
        narratives = [s.narrative_summary for s in summaries]
        assert len(set(narratives)) > 1  # At least 2 different narratives
