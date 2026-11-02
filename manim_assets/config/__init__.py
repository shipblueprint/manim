"""Configuration package for Manim Assets.

`theme.toml` is the single source of truth; `theme.py` resolves it into the
tokens scenes import.
"""

from .theme import (
    ACCENT_COLOR,
    BG_COLOR,
    BODY_FONT,
    COLORS,
    HEADING_FONT,
    MUTED_COLOR,
    TEXT_COLOR,
)

__all__ = [
    "ACCENT_COLOR",
    "BG_COLOR",
    "BODY_FONT",
    "COLORS",
    "HEADING_FONT",
    "MUTED_COLOR",
    "TEXT_COLOR",
]
