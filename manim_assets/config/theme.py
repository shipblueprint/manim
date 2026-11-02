"""Brand theme: the single source of truth for colors and fonts.

Values live in ``theme.toml``; this module only loads them, registers any font
files bundled in ``fonts/``, and exposes resolved tokens for scenes.
"""

from __future__ import annotations

import tomllib
import warnings
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).resolve().parent
THEME_PATH = CONFIG_DIR / "theme.toml"


def _load_theme(path: Path) -> tuple[dict[str, str], dict[str, str], dict[str, Any]]:
    with path.open("rb") as handle:
        theme = tomllib.load(handle)
    palette, roles, fonts = theme["palette"], theme["roles"], theme["fonts"]

    unknown = sorted({ref for ref in roles.values() if ref not in palette})
    if unknown:
        raise KeyError(
            f"{path}: [roles] {', '.join(unknown)} is not a key in [palette]"
        )
    return palette, {role: palette[ref] for role, ref in roles.items()}, fonts


PALETTE, ROLES, FONTS = _load_theme(THEME_PATH)
COLORS = {**PALETTE, **ROLES}

# Roles scenes consume
BG_COLOR = ROLES["background"]
TEXT_COLOR = ROLES["foreground"]
ACCENT_COLOR = ROLES["accent"]
MUTED_COLOR = ROLES["muted"]

# Type
HEADING_FONT = FONTS["heading"]
BODY_FONT = FONTS["body"]


def _register_bundled_fonts() -> None:
    """Make the brand fonts usable without a system-wide install."""
    import manimpango

    fonts_dir = CONFIG_DIR / FONTS.get("fonts_dir", "fonts")
    if not fonts_dir.is_dir():
        return
    for font_file in sorted(fonts_dir.iterdir()):
        if font_file.suffix.lower() in {".ttf", ".otf"}:
            manimpango.register_font(str(font_file))


def _apply_text_defaults() -> None:
    from manim import DecimalNumber, NumberLine, Text

    _register_bundled_fonts()
    Text.set_default(font=BODY_FONT)
    # Axis labels reach the renderer through NumberLine.label_constructor, which
    # defaults to MathTex and therefore to a TeX distribution. Text-based labels
    # keep the brand font and let the library render anywhere.
    NumberLine.set_default(label_constructor=Text)
    DecimalNumber.set_default(mob_class=Text)

    missing = [name for name in (HEADING_FONT, BODY_FONT) if name not in Text.font_list()]
    if missing:
        warnings.warn(
            f"brand fonts not available: {', '.join(missing)}. "
            f"Drop their .ttf/.otf files in {CONFIG_DIR / FONTS.get('fonts_dir', 'fonts')} "
            "or install them; Pango will substitute a fallback.",
            stacklevel=2,
        )


_apply_text_defaults()
