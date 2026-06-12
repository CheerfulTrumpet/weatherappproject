#!/usr/bin/env python3
"""
Example Script: Cognitive Weather Oracle Features Showcase
===========================================================

This script demonstrates all key features of the application:
- Fetching weather data
- Generating narratives in multiple personas
- Applying themes
- Generating icons
- Analyzing cognitive factors

Run this to see the application in action without the GUI.
"""

import sys
from typing import Optional

# Add src to path
sys.path.insert(0, '/home/claude/cognitive-weather-oracle')

from src.weather_api import WeatherData, MockWeatherAPI
from src.persona_engine import PersonaEngine, PersonaStyle
from src.theme_manager import ThemeManager, AccessibilityHelper
from src.icon_manager import IconAssetManager


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n  📌 {title}")
    print("  " + "-" * 70 + "\n")


def demo_weather_data():
    """Demonstrate WeatherData object creation and properties."""
    print_section("1. WEATHER DATA")
    
    weather = WeatherData(
        temperature=72.0,
        feels_like=70.0,
        humidity=45,
        pressure=1013,
        description="Clear Sky",
        wind_speed=5.0,
        cloudiness=10,
        raw_icon_code="01d"
    )
    
    print(f"  Temperature:    {weather.temperature}°F")
    print(f"  Feels Like:     {weather.feels_like}°F")
    print(f"  Humidity:       {weather.humidity}%")
    print(f"  Pressure:       {weather.pressure} hPa")
    print(f"  Description:    {weather.description}")
    print(f"  Wind Speed:     {weather.wind_speed} mph")
    print(f"  Cloud Cover:    {weather.cloudiness}%")
    print(f"  Detected Condition: {weather.weather_condition}")
    
    return weather


def demo_persona_engine(weather: WeatherData):
    """Demonstrate Persona Engine with multiple styles."""
    print_section("2. PERSONA ENGINE - COGNITIVE NARRATIVES")
    
    personas = [
        PersonaStyle.PHILOSOPHER,
        PersonaStyle.POET,
        PersonaStyle.SCIENTIST,
        PersonaStyle.MINIMALIST
    ]
    
    for persona in personas:
        print_subsection(f"{persona.value.upper()} STYLE")
        
        engine = PersonaEngine(persona=persona)
        summary = engine.generate_summary(weather)
        
        print(f"  MOOD: {summary.primary_mood}\n")
        
        print("  NARRATIVE:")
        # Print narrative with indentation
        for line in summary.narrative_summary.split('\n'):
            print(f"    {line}")
        
        print(f"\n  KEY INSIGHTS:")
        for i, insight in enumerate(summary.key_insights[:2]):  # Show first 2
            print(f"    • {insight}\n")
        
        print(f"  RECOMMENDATION:")
        rec_lines = summary.actionable_sentiment.split('\n')
        for line in rec_lines[:3]:  # Show first 3 lines
            print(f"    {line}")


def demo_theme_manager(weather: WeatherData):
    """Demonstrate Theme Manager and theming."""
    print_section("3. REACTIVE THEMING")
    
    theme = ThemeManager.get_theme(weather.weather_condition)
    
    print(f"  Weather Condition: {weather.weather_condition.upper()}")
    print(f"\n  COLOR SCHEME:")
    print(f"    Primary Background:   {theme.bg_primary}")
    print(f"    Secondary Background: {theme.bg_secondary}")
    print(f"    Primary Text:         {theme.text_primary}")
    print(f"    Secondary Text:       {theme.text_secondary}")
    print(f"    Accent:               {theme.accent}")
    print(f"    Border:               {theme.border}")
    
    print(f"\n  ACCESSIBILITY (WCAG):")
    contrasts = AccessibilityHelper.validate_theme_accessibility(theme)
    for label, ratio in contrasts.items():
        wcag_level = "🟢 AAA" if ratio >= 7.0 else "🟡 AA" if ratio >= 4.5 else "🔴 Fail"
        print(f"    {label:25} {ratio:5.2f}:1  {wcag_level}")


def demo_icon_manager(weather: WeatherData):
    """Demonstrate Icon Manager."""
    print_section("4. DYNAMIC ICONS")
    
    emoji = IconAssetManager.get_emoji(weather.weather_condition)
    print(f"  Emoji Icon for '{weather.weather_condition}': {emoji}")
    
    print(f"\n  SVG Icon Preview (markup):")
    svg = IconAssetManager.get_icon(weather.weather_condition)
    # Show first few lines of SVG
    svg_lines = svg.strip().split('\n')[:5]
    for line in svg_lines:
        print(f"    {line.strip()}")
    print(f"    ... ({len(svg)} characters total)")


def demo_all_conditions():
    """Demonstrate all weather conditions."""
    print_section("5. ALL WEATHER CONDITIONS")
    
    test_data = {
        "clear": WeatherData(72, 70, 50, 1013, "Clear Sky", 5, 10, "01d"),
        "cloudy": WeatherData(65, 65, 60, 1012, "Overcast", 6, 80, "04d"),
        "rainy": WeatherData(55, 52, 85, 1005, "Heavy Rain", 12, 95, "10d"),
        "stormy": WeatherData(62, 55, 90, 995, "Thunderstorm", 25, 100, "11d"),
        "snowy": WeatherData(28, 18, 70, 1015, "Snow", 8, 90, "13d"),
    }
    
    print_subsection("CONDITION MATRIX")
    print(f"  {'Condition':<15} {'Temp':<8} {'Emoji':<8} {'Theme Primary':<20} {'Mood Snippet':<30}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*20} {'-'*30}")
    
    for condition, weather in test_data.items():
        theme = ThemeManager.get_theme(condition)
        engine = PersonaEngine(PersonaStyle.PHILOSOPHER)
        summary = engine.generate_summary(weather)
        emoji = IconAssetManager.get_emoji(condition)
        
        mood = summary.primary_mood.split()[0]  # First word
        print(f"  {condition:<15} {weather.temperature:<8.0f} {emoji:<8} {theme.bg_primary:<20} {mood:<30}")


def demo_extreme_conditions():
    """Demonstrate handling of extreme conditions."""
    print_section("6. EXTREME CONDITIONS")
    
    conditions = {
        "Extreme Cold": WeatherData(-10, -20, 30, 1025, "Clear", 10, 5, "01d"),
        "Extreme Heat": WeatherData(105, 115, 20, 1000, "Clear", 2, 0, "01d"),
        "High Humidity": WeatherData(85, 95, 100, 1008, "Mist", 1, 70, "50d"),
        "Very Windy": WeatherData(55, 35, 65, 990, "Windy", 40, 100, "01d"),
    }
    
    engine = PersonaEngine(PersonaStyle.SCIENTIST)
    
    for name, weather in conditions.items():
        print_subsection(name)
        summary = engine.generate_summary(weather)
        
        # Show most relevant insight
        print(f"  Temperature: {weather.temperature}°F")
        print(f"  Mood: {summary.primary_mood}")
        print(f"\n  Relevant Insights:")
        for insight in summary.key_insights[:2]:
            print(f"    • {insight}\n")


def demo_cognitive_factors(weather: WeatherData):
    """Demonstrate cognitive factor analysis."""
    print_section("7. COGNITIVE FACTOR ANALYSIS")
    
    engine = PersonaEngine()
    summary = engine.generate_summary(weather)
    
    print("  Deep-dive cognitive analysis:\n")
    
    for factor_name, explanation in summary.cognitive_factors.items():
        print(f"  🧠 {factor_name.replace('_', ' ').upper()}:")
        # Wrap text at reasonable length
        words = explanation.split()
        line = "     "
        for word in words:
            if len(line) + len(word) > 70:
                print(line)
                line = "     "
            line += word + " "
        print(line)
        print()


def demo_mock_api():
    """Demonstrate using Mock API for testing."""
    print_section("8. MOCK API FOR TESTING")
    
    weather_data = WeatherData(72, 70, 50, 1013, "Clear Sky", 5, 10, "01d")
    api = MockWeatherAPI(mock_data=weather_data)
    
    print("  Simulating 3 API calls:")
    for i in range(1, 4):
        result = api.fetch_weather()
        print(f"    Call {i}: Temperature = {result.temperature}°F, Call count = {api.call_count}")


def demo_multi_persona_consistency():
    """Demonstrate consistency across personas."""
    print_section("9. MULTI-PERSONA CONSISTENCY")
    
    weather = WeatherData(72, 70, 50, 1013, "Clear Sky", 5, 10, "01d")
    personas = [PersonaStyle.PHILOSOPHER, PersonaStyle.POET, PersonaStyle.SCIENTIST, PersonaStyle.MINIMALIST]
    
    print("  Same weather, different narrative perspectives:\n")
    
    moods = []
    for persona in personas:
        engine = PersonaEngine(persona=persona)
        summary = engine.generate_summary(weather)
        moods.append(summary.primary_mood)
    
    print(f"  All agree on mood component 'Clarity': {all('Clarity' in m for m in moods)}\n")
    
    print("  Mood statements by persona:")
    for persona, mood in zip(personas, moods):
        print(f"    {persona.value:15} → {mood}")


def demo_performance():
    """Demonstrate performance characteristics."""
    print_section("10. PERFORMANCE BENCHMARK")
    
    import time
    
    weather = WeatherData(72, 70, 50, 1013, "Clear Sky", 5, 10, "01d")
    
    # Benchmark narrative generation
    engine = PersonaEngine()
    
    start = time.time()
    for _ in range(100):
        summary = engine.generate_summary(weather)
    elapsed = time.time() - start
    
    print(f"  Narrative Generation (100x):")
    print(f"    Time: {elapsed:.3f} seconds")
    print(f"    Per generation: {(elapsed/100)*1000:.2f} ms")
    print(f"    Throughput: {100/elapsed:.0f} generations/second")
    
    # Benchmark theme retrieval
    start = time.time()
    for _ in range(1000):
        theme = ThemeManager.get_theme("clear")
    elapsed = time.time() - start
    
    print(f"\n  Theme Retrieval (1000x):")
    print(f"    Time: {elapsed:.3f} seconds")
    print(f"    Per retrieval: {(elapsed/1000)*1000000:.2f} microseconds")
    print(f"    Throughput: {1000/elapsed:.0f} retrievals/second")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  COGNITIVE WEATHER ORACLE - FEATURES SHOWCASE".center(78) + "║")
    print("║" + "  Demonstrating all application features and capabilities".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        # Run all demonstrations
        weather = demo_weather_data()
        demo_persona_engine(weather)
        demo_theme_manager(weather)
        demo_icon_manager(weather)
        demo_all_conditions()
        demo_extreme_conditions()
        demo_cognitive_factors(weather)
        demo_mock_api()
        demo_multi_persona_consistency()
        demo_performance()
        
        # Final summary
        print_section("SUMMARY")
        print("""
  ✓ Weather data parsing and normalization
  ✓ Cognitive narrative generation (4 personas)
  ✓ Reactive theming with accessibility validation
  ✓ Dynamic icon generation (SVG + emoji)
  ✓ Extreme condition handling
  ✓ Cognitive factor analysis
  ✓ Mock API for testing
  ✓ Multi-persona consistency
  ✓ Performance benchmarks
        
  This demonstration shows the complete application workflow
  without requiring the GUI or external API calls.
  
  To run the full GUI application:
      python main.py
  
  To run tests:
      pytest
        """)
        
        print("\n" + "=" * 80)
        print("  Demonstration complete! ✨")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
