"""Theme loader for Manim - loads from config/theme.toml."""
import os
from pathlib import Path

# Try to import tomllib (Python 3.11+) or toml
try:
    import tomllib
except ImportError:
    try:
        import toml as tomllib
    except ImportError:
        tomllib = None


def _load_theme():
    theme_path = Path(__file__).parent / "theme.toml"
    if tomllib and theme_path.exists():
        with open(theme_path, "rb") as f:
            if hasattr(tomllib, "load"):
                data = tomllib.load(f)
            else:
                f.seek(0)
                data = tomllib.load(f)
        return data.get("colors", {}), data.get("fonts", {})
    return {}, {}


_colors, _fonts = _load_theme()

# Core colors from brand
BG_COLOR = _colors.get("bg_dark", "#15100b")
BACKGROUND_COLOR = BG_COLOR
SURFACE_COLOR = _colors.get("bg_surface", "#231a14")
TEXT_COLOR = _colors.get("text_primary", "#F5EFE7")
TEXT_PRIMARY = TEXT_COLOR
TEXT_SECONDARY = _colors.get("text_primary", "#F5EFE7")
ACCENT_COLOR = _colors.get("text_accent", "#BB9457")
ACCENT = ACCENT_COLOR
MUTED_COLOR = _colors.get("text_accent", "#BB9457")
MUTED = MUTED_COLOR
CTA_PRIMARY = _colors.get("cta_primary", "#6F1D1B")
CTA_HOVER = _colors.get("cta_hover", "#5a1715")
WARNING_COLOR = _colors.get("text_accent", "#BB9457")
ERROR_COLOR = _colors.get("cta_primary", "#6F1D1B")
SUCCESS_COLOR = _colors.get("text_accent", "#BB9457")

# Illustration colors
ILLUSTRATION_STROKE_LIGHT = _colors.get("ILLUSTRATION_STROKE_LIGHT", "#432818")
ILLUSTRATION_SHADOW_LIGHT = _colors.get("ILLUSTRATION_SHADOW_LIGHT", "#6F1D1B")
ILLUSTRATION_STROKE_DARK = _colors.get("ILLUSTRATION_STROKE_DARK", "#EFE3D2")
ILLUSTRATION_SHADOW_DARK = _colors.get("ILLUSTRATION_SHADOW_DARK", "#432818")
ILLUSTRATION_FILL_GOLD = _colors.get("ILLUSTRATION_FILL_GOLD", "#BB9457")

# Fonts
UI_FONT = _fonts.get("UI_FONT", "Inter")
DISPLAY_FONT = _fonts.get("DISPLAY_FONT", "Playfair Display")
HEADING_FONT = _fonts.get("HEADING_FONT", "Playfair Display")
BODY_FONT = _fonts.get("BODY_FONT", "Inter")
MONO_FONT = _fonts.get("MONO_FONT", "Inter")

__all__ = [
    "BG_COLOR", "BACKGROUND_COLOR", "SURFACE_COLOR",
    "TEXT_COLOR", "TEXT_PRIMARY", "TEXT_SECONDARY",
    "ACCENT_COLOR", "ACCENT", "MUTED_COLOR", "MUTED",
    "CTA_PRIMARY", "CTA_HOVER", "WARNING_COLOR", "ERROR_COLOR", "SUCCESS_COLOR",
    "ILLUSTRATION_STROKE_LIGHT", "ILLUSTRATION_SHADOW_LIGHT",
    "ILLUSTRATION_STROKE_DARK", "ILLUSTRATION_SHADOW_DARK", "ILLUSTRATION_FILL_GOLD",
    "UI_FONT", "DISPLAY_FONT", "HEADING_FONT", "BODY_FONT", "MONO_FONT",
]
