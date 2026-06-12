"""
Professional Weather Dashboard - Complete Version with Working Backgrounds
==========================================================================
Features:
- Real-time data visualization
- Custom landmark backgrounds (visible through content)
- Professional charts and display
- Comprehensive cognitive analysis
"""

import customtkinter as ctk
from typing import Optional, Callable
import logging
from datetime import datetime
import tkinter as tk

from .weather_api import WeatherData
from .persona_engine import CognitiveSummary
from .theme_manager import ThemeManager, ColorScheme
from .icon_manager import IconAssetManager
from .background_renderer import BackgroundRenderer

logger = logging.getLogger(__name__)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class WeatherGUI:
    """Professional weather dashboard with landmark backgrounds."""
    
    def __init__(
        self,
        root: ctk.CTk,
        weather_fetcher: Callable,
        narrative_generator: Callable,
        location_name: str = "New York",
        on_location_change: Optional[Callable] = None
    ):
        self.root = root
        self.weather_fetcher = weather_fetcher
        self.narrative_generator = narrative_generator
        self.location_name = location_name
        self.on_location_change = on_location_change
        
        self.current_weather: Optional[WeatherData] = None
        self.current_theme: Optional[ColorScheme] = None
        self.bg_image = None
        self.bg_photo = None
        
        self.locations = {
            "New York": "40.7128,-74.0060",
            "London": "51.5074,-0.1278",
            "Paris": "48.8566,2.3522",
            "Tokyo": "35.6762,139.6503",
            "Sydney": "-33.8688,151.2093",
            "Dubai": "25.2048,55.2708",
            "Singapore": "1.3521,103.8198",
        }
        
        self._configure_window()
        self._create_background()
        self._create_ui()
        logger.info("Professional GUI initialized")
    
    def _configure_window(self):
        """Configure main window."""
        self.root.title("Cognitive Weather Oracle - Professional Dashboard")
        self.root.geometry("1200x1400")
        self.root.minsize(900, 1000)
        self.root.configure(fg_color="#0a0e27")
    
    def _create_background(self):
        """Create background using Canvas for proper display."""
        # Create a Canvas that covers the entire window
        self.bg_canvas = tk.Canvas(
            self.root,
            bg="#0a0e27",
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.bg_canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Load initial background image
        self._update_background(self.location_name)
        
        # Bind resize event to redraw background
        self.root.bind("<Configure>", self._on_window_resize)
    
    def _on_window_resize(self, event=None):
        """Handle window resize to redraw background."""
        if hasattr(self, 'bg_canvas'):
            try:
                self.bg_canvas.delete("all")
                if self.bg_photo:
                    self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW)
            except Exception as e:
                logger.debug(f"Resize event: {e}")
    
    def _create_ui(self):
        """Create professional dashboard UI."""
        
        self._create_header()
        
        main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent"
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._create_primary_display(main_frame)
        self._create_metrics_row(main_frame)
        self._create_cognitive_section(main_frame)
        self._create_narrative_section(main_frame)
        self._create_action_section(main_frame)
        self._create_footer(main_frame)
    
    def _create_header(self):
        """Create top header with title and location selector."""
        header = ctk.CTkFrame(
            self.root,
            fg_color="#0a0e27",
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        
        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(fill="x", padx=20, pady=(20, 10))
        
        title_frame = ctk.CTkFrame(inner, fg_color="transparent")
        title_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            title_frame,
            text="Cognitive Weather Oracle",
            font=("Helvetica", 32, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Professional Weather Intelligence Dashboard",
            font=("Helvetica", 12),
            text_color="#CCCCCC"
        )
        subtitle.pack(anchor="w")
        
        right_frame = ctk.CTkFrame(inner, fg_color="transparent")
        right_frame.pack(side="right")
        
        self.location_dropdown = ctk.CTkComboBox(
            right_frame,
            values=list(self.locations.keys()),
            command=self._on_location_change,
            font=("Helvetica", 12, "bold"),
            fg_color="#1a2b4a",
            button_color="#2a5f8f",
            text_color="#FFFFFF",
            width=150,
            height=40
        )
        self.location_dropdown.set(self.location_name)
        self.location_dropdown.pack()
    
    def _create_primary_display(self, parent):
        """Create main weather display card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=("#1a2b4a", "#0a1528"),
            corner_radius=20,
            border_width=2,
            border_color="#2a5f8f"
        )
        card.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        left = ctk.CTkFrame(content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)
        
        self.location_display = ctk.CTkLabel(
            left,
            text=self.location_name,
            font=("Helvetica", 16),
            text_color="#FFFF00"
        )
        self.location_display.pack(anchor="w")
        
        self.temperature_label = ctk.CTkLabel(
            left,
            text="--°",
            font=("Helvetica", 90, "bold"),
            text_color="#FFFFFF"
        )
        self.temperature_label.pack(anchor="w")
        
        self.condition_label = ctk.CTkLabel(
            left,
            text="Loading weather data...",
            font=("Helvetica", 18),
            text_color="#FFFF00"
        )
        self.condition_label.pack(anchor="w", pady=(5, 0))
        
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True, padx=(30, 0))
        
        self.weather_emoji = ctk.CTkLabel(
            right,
            text="☀️",
            font=("Helvetica", 100),
            text_color="#FFFFFF"
        )
        self.weather_emoji.pack()
        
        self.feels_like_label = ctk.CTkLabel(
            right,
            text="Feels like --°F",
            font=("Helvetica", 14),
            text_color="#FFFF00"
        )
        self.feels_like_label.pack()
    
    def _create_metrics_row(self, parent):
        """Create metrics display row."""
        metrics_frame = ctk.CTkFrame(parent, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 20))
        
        metrics_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        metrics = [
            ("💧 Humidity", "humidity_value", "%"),
            ("💨 Wind Speed", "wind_value", "mph"),
            ("🔷 Pressure", "pressure_value", "hPa"),
            ("☁️ Cloud Cover", "clouds_value", "%")
        ]
        
        for col, (label, attr, unit) in enumerate(metrics):
            self._create_metric_card(metrics_frame, col, label, attr, unit)
    
    def _create_metric_card(self, parent, col, label, attr, unit):
        """Create individual metric card."""
        card = ctk.CTkFrame(
            parent,
            fg_color=("#1a2b4a", "#0a1528"),
            corner_radius=15,
            border_width=2,
            border_color="#2a5f8f"
        )
        card.grid(row=0, column=col, sticky="ew", padx=8)
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=("Helvetica", 11),
            text_color="#FFFF00"
        )
        label_widget.pack(pady=(12, 5))
        
        value_widget = ctk.CTkLabel(
            card,
            text="--",
            font=("Helvetica", 22, "bold"),
            text_color="#FFFFFF"
        )
        value_widget.pack(pady=(5, 12))
        
        unit_label = ctk.CTkLabel(
            card,
            text=unit,
            font=("Helvetica", 10),
            text_color="#CCCCCC"
        )
        unit_label.pack(pady=(0, 12))
        
        setattr(self, attr, value_widget)
    
    def _create_cognitive_section(self, parent):
        """Create cognitive mood and factors section."""
        section_title = ctk.CTkLabel(
            parent,
            text="🧠 Cognitive State Analysis",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        )
        section_title.pack(anchor="w", pady=(20, 10))
        
        mood_card = ctk.CTkFrame(
            parent,
            fg_color=("#2a3f5a", "#0a1528"),
            corner_radius=15,
            border_width=2,
            border_color="#3a6f9f"
        )
        mood_card.pack(fill="x", pady=(0, 15))
        
        self.mood_label = ctk.CTkLabel(
            mood_card,
            text="Cognitive State: --",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        )
        self.mood_label.pack(padx=20, pady=15)
        
        factors_title = ctk.CTkLabel(
            parent,
            text="Environmental Factors:",
            font=("Helvetica", 13, "bold"),
            text_color="#FFFFFF"
        )
        factors_title.pack(anchor="w", pady=(15, 10))
        
        self.factors_textbox = ctk.CTkTextbox(
            parent,
            font=("Helvetica", 11),
            height=120,
            wrap="word",
            fg_color=("#1a2b4a", "#0a1528"),
            text_color="#FFFFFF",
            border_color="#2a5f8f",
            border_width=2,
            corner_radius=12
        )
        self.factors_textbox.pack(fill="x", pady=(0, 20))
        self.factors_textbox.configure(state="disabled")
    
    def _create_narrative_section(self, parent):
        """Create narrative display section."""
        title = ctk.CTkLabel(
            parent,
            text="✨ Atmospheric Narrative",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w", pady=(0, 10))
        
        self.narrative_textbox = ctk.CTkTextbox(
            parent,
            font=("Helvetica", 12),
            height=150,
            wrap="word",
            fg_color=("#1a2b4a", "#0a1528"),
            text_color="#FFFFFF",
            border_color="#2a5f8f",
            border_width=2,
            corner_radius=12
        )
        self.narrative_textbox.pack(fill="x", pady=(0, 20))
        self.narrative_textbox.configure(state="disabled")
    
    def _create_action_section(self, parent):
        """Create insights and recommendations section."""
        insights_title = ctk.CTkLabel(
            parent,
            text="💡 Key Insights",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        )
        insights_title.pack(anchor="w", pady=(0, 10))
        
        self.insights_textbox = ctk.CTkTextbox(
            parent,
            font=("Helvetica", 11),
            height=140,
            wrap="word",
            fg_color=("#1a2b4a", "#0a1528"),
            text_color="#FFFFFF",
            border_color="#2a5f8f",
            border_width=2,
            corner_radius=12
        )
        self.insights_textbox.pack(fill="x", pady=(0, 20))
        self.insights_textbox.configure(state="disabled")
        
        rec_title = ctk.CTkLabel(
            parent,
            text="🎯 Optimal Activities",
            font=("Helvetica", 16, "bold"),
            text_color="#FFFFFF"
        )
        rec_title.pack(anchor="w", pady=(0, 10))
        
        self.recommendations_textbox = ctk.CTkTextbox(
            parent,
            font=("Helvetica", 11),
            height=130,
            wrap="word",
            fg_color=("#1a2b4a", "#0a1528"),
            text_color="#FFFFFF",
            border_color="#2a5f8f",
            border_width=2,
            corner_radius=12
        )
        self.recommendations_textbox.pack(fill="x", pady=(0, 20))
        self.recommendations_textbox.configure(state="disabled")
    
    def _create_footer(self, parent):
        """Create footer with buttons."""
        footer = ctk.CTkFrame(parent, fg_color="transparent")
        footer.pack(fill="x", pady=(20, 0))
        
        self.refresh_button = ctk.CTkButton(
            footer,
            text="🔄  Refresh Data",
            font=("Helvetica", 13, "bold"),
            command=self.update_weather,
            fg_color="#2d7f3d",
            hover_color="#1f5f2d",
            text_color="white",
            height=45,
            corner_radius=12
        )
        self.refresh_button.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.last_update_label = ctk.CTkLabel(
            footer,
            text="",
            font=("Helvetica", 10),
            text_color="#FFFF00"
        )
        self.last_update_label.pack(side="left", padx=10)
        
        self.error_label = ctk.CTkLabel(
            footer,
            text="",
            font=("Helvetica", 10),
            text_color="#FF6B6B"
        )
        self.error_label.pack(side="left", padx=10)
    
    def _on_location_change(self, location_name: str):
        """Handle location change."""
        logger.info(f"Location changed to: {location_name}")
        if self.on_location_change:
            self.on_location_change(location_name)
    
    def update_location_display(self, location_name: str):
        """Update location display and background."""
        self.location_name = location_name
        self.location_display.configure(text=location_name)
        self._update_background(location_name)
    
    def _update_background(self, location: str):
        """Update background with landmark image."""
        try:
            self.bg_image = BackgroundRenderer.get_background_image(location)
            # Convert CTkImage to PhotoImage for Canvas display
            if self.bg_image:
                self.bg_photo = self.bg_image._light_image  # Get the PIL image
                # Redraw canvas with new image
                if hasattr(self, 'bg_canvas'):
                    self.bg_canvas.delete("all")
                    from PIL import ImageTk
                    photo = ImageTk.PhotoImage(self.bg_photo)
                    self.bg_canvas.image = photo  # Keep reference
                    self.bg_canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            logger.debug(f"Updated background for {location}")
        except Exception as e:
            logger.warning(f"Background update error: {e}")
    
    def update_weather(self):
        """Fetch and update all weather data."""
        logger.info("Updating weather data...")
        
        try:
            self._show_error("")
            self.refresh_button.configure(text="⏳  Loading...", state="disabled")
            self.root.update()
            
            weather = self.weather_fetcher()
            
            if weather is None:
                self._show_error("Unable to fetch weather data.")
                self.refresh_button.configure(text="🔄  Refresh Data", state="normal")
                return
            
            summary = self.narrative_generator(weather)
            self._display_weather(weather, summary)
            
            self.refresh_button.configure(text="🔄  Refresh Data", state="normal")
            self.last_update_label.configure(
                text=f"Updated: {datetime.now().strftime('%I:%M %p')}"
            )
            
            logger.info(f"Weather update successful: {weather.description}")
        
        except Exception as e:
            logger.error(f"Error: {e}")
            self._show_error(f"Error: {str(e)}")
            self.refresh_button.configure(text="🔄  Refresh Data", state="normal")
    
    def _display_weather(self, weather: WeatherData, summary: CognitiveSummary):
        """Display all weather data on UI."""
        self.temperature_label.configure(text=f"{weather.temperature:.0f}°")
        self.feels_like_label.configure(text=f"Feels like {weather.feels_like:.0f}°F")
        self.condition_label.configure(text=weather.description)
        
        emoji = IconAssetManager.get_emoji(weather.weather_condition)
        self.weather_emoji.configure(text=emoji)
        
        self.humidity_value.configure(text=f"{weather.humidity}")
        self.wind_value.configure(text=f"{weather.wind_speed:.1f}")
        self.pressure_value.configure(text=f"{weather.pressure}")
        self.clouds_value.configure(text=f"{weather.cloudiness}")
        
        self.mood_label.configure(text=f"Cognitive State: {summary.primary_mood}")
        
        factors_text = self._format_factors(summary.cognitive_factors)
        self.factors_textbox.configure(state="normal")
        self.factors_textbox.delete("1.0", "end")
        self.factors_textbox.insert("1.0", factors_text)
        self.factors_textbox.configure(state="disabled")
        
        self.narrative_textbox.configure(state="normal")
        self.narrative_textbox.delete("1.0", "end")
        self.narrative_textbox.insert("1.0", summary.narrative_summary)
        self.narrative_textbox.configure(state="disabled")
        
        insights_text = "\n\n".join(summary.key_insights)
        self.insights_textbox.configure(state="normal")
        self.insights_textbox.delete("1.0", "end")
        self.insights_textbox.insert("1.0", insights_text)
        self.insights_textbox.configure(state="disabled")
        
        self.recommendations_textbox.configure(state="normal")
        self.recommendations_textbox.delete("1.0", "end")
        self.recommendations_textbox.insert("1.0", summary.actionable_sentiment)
        self.recommendations_textbox.configure(state="disabled")
        
        self._apply_theme(weather.weather_condition)
    
    def _format_factors(self, factors: dict) -> str:
        """Format cognitive factors for display."""
        lines = []
        for key, value in factors.items():
            label = " ".join(word.capitalize() for word in key.split("_"))
            lines.append(f"{label}:\n{value}")
        return "\n\n".join(lines)
    
    def _apply_theme(self, condition: str):
        """Apply color theme based on weather."""
        theme = ThemeManager.get_theme(condition)
        self.current_theme = theme
        
        self.temperature_label.configure(text_color="#FFFFFF")
        self.condition_label.configure(text_color="#FFFF00")
        self.mood_label.configure(text_color="#FFFFFF")
        
        self.refresh_button.configure(
            fg_color=theme.accent,
            hover_color=self._darken_color(theme.accent, 0.7)
        )
    
    def _show_error(self, message: str):
        """Display error message."""
        self.error_label.configure(text=message)
    
    @staticmethod
    def _darken_color(hex_color: str, factor: float = 0.8) -> str:
        """Darken a hex color."""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def schedule_auto_refresh(self, interval_ms: int = 600000):
        """Schedule automatic refresh."""
        def refresh():
            try:
                self.update_weather()
            except Exception as e:
                logger.error(f"Auto-refresh error: {e}")
            self.root.after(interval_ms, refresh)
        
        logger.info(f"Auto-refresh scheduled every {interval_ms}ms")
        self.root.after(interval_ms, refresh)
    
    def run(self):
        """Run the GUI."""
        logger.info("Starting GUI event loop...")
        self.root.mainloop()