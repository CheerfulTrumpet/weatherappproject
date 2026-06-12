"""
Background Renderer - Location-specific landmark backgrounds
Loads PNG assets or generates fallback backgrounds.
"""

from PIL import Image
import customtkinter as ctk
import logging
import os

logger = logging.getLogger(__name__)


class BackgroundRenderer:
    """Creates/loads location-specific backgrounds with landmarks."""
    
    LOCATION_INFO = {
        "New York": {
            "primary": "#1a3a5a",
            "secondary": "#2d5f7f",
            "accent": "#FFB800",
        },
        "London": {
            "primary": "#2a2a4a",
            "secondary": "#3a4a6a",
            "accent": "#FF6B35",
        },
        "Paris": {
            "primary": "#3a2a3a",
            "secondary": "#5a4a5a",
            "accent": "#FFD700",
        },
        "Tokyo": {
            "primary": "#1a1a3a",
            "secondary": "#2a3a5a",
            "accent": "#FF1493",
        },
        "Sydney": {
            "primary": "#1a3a4a",
            "secondary": "#2a5a7a",
            "accent": "#00CED1",
        },
        "Dubai": {
            "primary": "#3a2a1a",
            "secondary": "#5a4a2a",
            "accent": "#FFD700",
        },
        "Singapore": {
            "primary": "#1a3a3a",
            "secondary": "#2a5a5a",
            "accent": "#00FF7F",
        },
    }
    
    # Map location names to PNG filenames
    PNG_MAP = {
        "New York": "new_york.png",
        "London": "london.png",
        "Paris": "paris.png",
        "Tokyo": "tokyo.png",
        "Sydney": "sydney.png",
        "Dubai": "dubai.png",
        "Singapore": "singapore.png",
    }
    
    @classmethod
    def get_background_image(cls, location: str, width: int = 1200, height: int = 1400) -> ctk.CTkImage:
        """Load PNG background or generate fallback."""
        # First, try to load from assets directory
        asset_path = cls._get_asset_path(location)
        if asset_path and os.path.exists(asset_path):
            try:
                return cls._load_png_background(asset_path, width, height)
            except Exception as e:
                logger.warning(f"Failed to load PNG for {location}: {e}. Using generated background.")
        
        # Fall back to generated backgrounds
        if location == "New York":
            return cls._create_nyc_background(width, height)
        elif location == "London":
            return cls._create_london_background(width, height)
        elif location == "Paris":
            return cls._create_paris_background(width, height)
        elif location == "Tokyo":
            return cls._create_tokyo_background(width, height)
        elif location == "Sydney":
            return cls._create_sydney_background(width, height)
        elif location == "Dubai":
            return cls._create_dubai_background(width, height)
        elif location == "Singapore":
            return cls._create_singapore_background(width, height)
        else:
            return cls._create_default_background(width, height)
    
    @classmethod
    def _get_asset_path(cls, location: str) -> str:
        """Get path to PNG asset file."""
        if location not in cls.PNG_MAP:
            return None
        
        filename = cls.PNG_MAP[location]
        
        # Check multiple possible locations
        possible_paths = [
            os.path.join(os.path.dirname(__file__), "..", "assets", filename),
            os.path.join(os.path.dirname(__file__), "..", filename),
            os.path.join("assets", filename),
            filename,
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return None
    
    @staticmethod
    def _load_png_background(asset_path: str, width: int, height: int) -> ctk.CTkImage:
        """Load PNG and convert to CTkImage."""
        try:
            pil_img = Image.open(asset_path).convert("RGBA")
            # Resize to match window
            pil_img = pil_img.resize((width, height), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(width, height))
            logger.info(f"Loaded PNG background: {asset_path}")
            return ctk_img
        except Exception as e:
            logger.error(f"Error loading PNG: {e}")
            raise
    
    @staticmethod
    def _hex_to_rgb(hex_color: str):
        """Convert hex to RGB."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @classmethod
    def _create_nyc_background(cls, w: int, h: int) -> ctk.CTkImage:
        """NYC: Statue of Liberty + Manhattan skyline."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (26, 58, 90, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h // 2):
            ratio = y / (h // 2)
            r = int(26 + (45 - 26) * ratio)
            g = int(58 + (95 - 58) * ratio)
            b = int(90 + (120 - 90) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        for y in range(h // 2, h):
            ratio = (y - h // 2) / (h // 2)
            r = int(20 + (10 - 20) * ratio)
            g = int(50 + (30 - 50) * ratio)
            b = int(80 + (50 - 80) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        liberty_x = w * 0.2
        liberty_y = h * 0.45
        
        draw.rectangle(
            [(liberty_x - 20, liberty_y + 40), (liberty_x + 20, liberty_y + 80)],
            fill=(255, 184, 0, 60)
        )
        draw.polygon(
            [(liberty_x, liberty_y - 30), (liberty_x - 15, liberty_y + 10), (liberty_x + 15, liberty_y + 10)],
            fill=(255, 215, 0, 100)
        )
        
        buildings = [
            (w * 0.6, h * 0.35, w * 0.68, h * 0.6, 220),
            (w * 0.68, h * 0.4, w * 0.76, h * 0.6, 200),
            (w * 0.76, h * 0.3, w * 0.84, h * 0.6, 240),
            (w * 0.84, h * 0.45, w * 0.92, h * 0.6, 180),
        ]
        
        for x1, y1, x2, y2, height_val in buildings:
            draw.rectangle([(x1, y2 - height_val), (x2, y2)], fill=(30, 50, 80, 150))
            for wy in range(int(y2 - height_val), int(y2), 20):
                for wx in range(int(x1), int(x2), 15):
                    draw.rectangle([(wx + 2, wy + 2), (wx + 10, wy + 10)], fill=(255, 215, 0, 80))
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_london_background(cls, w: int, h: int) -> ctk.CTkImage:
        """London: Big Ben + Thames."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (42, 42, 74, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(42 + (60 - 42) * ratio)
            g = int(42 + (60 - 42) * ratio)
            b = int(74 + (100 - 74) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        draw.rectangle([(0, h * 0.55), (w, h)], fill=(30, 60, 90, 200))
        
        tower_x = w * 0.2
        tower_base_y = h * 0.4
        
        draw.rectangle(
            [(tower_x - 15, tower_base_y), (tower_x + 15, tower_base_y + 200)],
            fill=(80, 80, 100, 180)
        )
        draw.ellipse(
            [(tower_x - 12, tower_base_y + 150), (tower_x + 12, tower_base_y + 180)],
            fill=(255, 215, 0, 150)
        )
        draw.polygon(
            [(tower_x, tower_base_y - 40), (tower_x - 10, tower_base_y), (tower_x + 10, tower_base_y)],
            fill=(100, 100, 120, 180)
        )
        
        for i in range(4):
            bx = w * (0.35 + i * 0.15)
            draw.rectangle(
                [(bx, h * 0.35), (bx + 30, h * 0.55)],
                fill=(60, 80, 110, 160)
            )
        
        draw.line([(0, h * 0.5), (w, h * 0.5)], fill=(150, 100, 80, 120), width=15)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_paris_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Paris: Eiffel Tower."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (58, 42, 58, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(58 + (40 - 58) * ratio)
            g = int(42 + (30 - 42) * ratio)
            b = int(58 + (50 - 58) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        tower_x = w * 0.5
        tower_base = h * 0.6
        
        for leg_x in [tower_x - 40, tower_x + 40]:
            draw.polygon(
                [(leg_x - 15, tower_base), (leg_x + 15, tower_base), (leg_x + 5, tower_base - 120), (leg_x - 5, tower_base - 120)],
                fill=(200, 150, 100, 180)
            )
        
        draw.rectangle(
            [(tower_x - 8, tower_base - 120), (tower_x + 8, tower_base - 280)],
            fill=(180, 130, 80, 200)
        )
        
        draw.rectangle(
            [(tower_x - 35, tower_base - 140), (tower_x + 35, tower_base - 135)],
            fill=(200, 150, 100, 180)
        )
        
        draw.rectangle(
            [(tower_x - 25, tower_base - 200), (tower_x + 25, tower_base - 195)],
            fill=(200, 150, 100, 180)
        )
        
        draw.polygon(
            [(tower_x, tower_base - 280), (tower_x - 8, tower_base - 260), (tower_x + 8, tower_base - 260)],
            fill=(255, 215, 0, 150)
        )
        
        for i in range(6):
            bx = i * (w / 6)
            draw.rectangle(
                [(bx + 10, h * 0.45), (bx + 180, h * 0.6)],
                fill=(80, 60, 80, 140)
            )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_tokyo_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Tokyo: Mount Fuji + neon city."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (26, 26, 58, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(26 + (60 - 26) * ratio)
            g = int(26 + (40 - 26) * ratio)
            b = int(58 + (100 - 58) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        fuji_x = w * 0.7
        fuji_base = h * 0.5
        
        draw.polygon(
            [(fuji_x - 80, fuji_base), (fuji_x, fuji_base - 160), (fuji_x + 80, fuji_base)],
            fill=(60, 80, 120, 180)
        )
        draw.polygon(
            [(fuji_x - 20, fuji_base - 60), (fuji_x, fuji_base - 120), (fuji_x + 20, fuji_base - 60)],
            fill=(240, 240, 240, 150)
        )
        
        buildings_data = [
            (w * 0.05, h * 0.35, 50, 180),
            (w * 0.15, h * 0.3, 70, 220),
            (w * 0.25, h * 0.4, 60, 160),
            (w * 0.35, h * 0.25, 80, 250),
            (w * 0.45, h * 0.38, 55, 170),
        ]
        
        for bx, by, bw, bh in buildings_data:
            draw.rectangle([(bx, by), (bx + bw, by + bh)], fill=(20, 30, 60, 180))
            for wy in range(int(by), int(by + bh), 18):
                for wx in range(int(bx), int(bx + bw), 15):
                    draw.rectangle([(wx + 2, wy + 2), (wx + 10, wy + 10)], fill=(255, 105, 180, 120))
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_sydney_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Sydney: Opera House + Harbour Bridge."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (26, 58, 74, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(26 + (60 - 26) * ratio)
            g = int(58 + (100 - 58) * ratio)
            b = int(74 + (120 - 74) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        draw.rectangle([(0, h * 0.5), (w, h)], fill=(20, 80, 120, 200))
        
        opera_x = w * 0.3
        opera_y = h * 0.35
        
        shell_points = [
            [(opera_x - 30, opera_y + 80), (opera_x - 10, opera_y), (opera_x + 10, opera_y + 80)],
            [(opera_x + 10, opera_y + 80), (opera_x + 30, opera_y), (opera_x + 50, opera_y + 80)],
        ]
        
        for points in shell_points:
            draw.polygon(points, fill=(220, 220, 220, 180))
        
        bridge_y = h * 0.4
        bridge_left_x = w * 0.4
        bridge_right_x = w * 0.85
        
        arch_points = []
        for i in range(50):
            ratio = i / 50
            x = bridge_left_x + (bridge_right_x - bridge_left_x) * ratio
            y = bridge_y - 100 * (ratio * (1 - ratio)) * 4
            arch_points.append((x, y))
        
        arch_points.append((bridge_right_x, bridge_y))
        arch_points.append((bridge_left_x, bridge_y))
        
        draw.polygon(arch_points, fill=(150, 100, 100, 150))
        
        for i in range(5):
            bx = w * (0.05 + i * 0.18)
            draw.rectangle(
                [(bx, h * 0.25), (bx + 40, h * 0.45)],
                fill=(40, 80, 120, 140)
            )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_dubai_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Dubai: Burj Khalifa + desert."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (58, 42, 26, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(58 + (200 - 58) * ratio)
            g = int(42 + (150 - 42) * ratio)
            b = int(26 + (80 - 26) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        draw.ellipse([(0, h * 0.6), (w * 0.5, h)], fill=(210, 180, 100, 150))
        draw.ellipse([(w * 0.3, h * 0.65), (w, h)], fill=(190, 160, 80, 140))
        
        tower_x = w * 0.5
        tower_base = h * 0.55
        
        draw.rectangle(
            [(tower_x - 6, tower_base), (tower_x + 6, tower_base - 280)],
            fill=(220, 220, 220, 200)
        )
        
        for i in range(5):
            y_pos = tower_base - (i * 50)
            width = 30 - (i * 4)
            draw.rectangle(
                [(tower_x - width / 2, y_pos), (tower_x + width / 2, y_pos - 10)],
                fill=(230, 230, 230, 180)
            )
        
        draw.polygon(
            [(tower_x, tower_base - 280), (tower_x - 4, tower_base - 250), (tower_x + 4, tower_base - 250)],
            fill=(255, 215, 0, 150)
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_singapore_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Singapore: Marina Bay Sands."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (26, 58, 58, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(26 + (80 - 26) * ratio)
            g = int(58 + (120 - 58) * ratio)
            b = int(58 + (140 - 58) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        draw.rectangle([(0, h * 0.5), (w, h)], fill=(30, 100, 130, 200))
        
        towers = [
            (w * 0.3, h * 0.25),
            (w * 0.5, h * 0.15),
            (w * 0.7, h * 0.25),
        ]
        
        for tx, ty in towers:
            draw.rectangle([(tx - 12, ty), (tx + 12, ty + 200)], fill=(200, 200, 200, 200))
            for wy in range(int(ty), int(ty + 200), 15):
                for wx in range(int(tx - 10), int(tx + 10), 8):
                    draw.rectangle([(wx, wy), (wx + 5, wy + 8)], fill=(100, 150, 200, 100))
        
        draw.rectangle(
            [(w * 0.3 - 12, h * 0.15), (w * 0.7 + 12, h * 0.18)],
            fill=(220, 220, 220, 180)
        )
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def _create_default_background(cls, w: int, h: int) -> ctk.CTkImage:
        """Default background."""
        from PIL import ImageDraw
        img = Image.new("RGBA", (w, h), (26, 42, 58, 255))
        draw = ImageDraw.Draw(img)
        
        for y in range(h):
            ratio = y / h
            r = int(26 + (40 - 26) * ratio)
            g = int(42 + (80 - 42) * ratio)
            b = int(58 + (100 - 58) * ratio)
            draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(w, h))
    
    @classmethod
    def get_background_gradient(cls, location: str) -> str:
        """Get primary background color."""
        info = cls.LOCATION_INFO.get(location, cls.LOCATION_INFO["New York"])
        return info["primary"]