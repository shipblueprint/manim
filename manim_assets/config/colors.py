"""
Color palette for Manim Assets.
Dark theme optimized for premium math visualizations.

Single source of truth: change COLORS dict once → all scenes update.
"""

# ── Data-driven config ──────────────────────────────────────────────
# One dict. All color values + semantic role mappings live here.
# To change the entire palette, edit only this dict.

COLORS = {
    # Raw palette values
    "bg":      "#0F0F12",   # Deep dark midnight
    "text":    "#EBE4D5",   # Crisp cream/off-white
    "accent":  "#FF6B4A",   # Vibrant technical orange
    "muted":   "#7A7570",   # Slate gray

    # Semantic role → raw value mapping
    # Change mapping here to reassign roles without touching scene code
    "background":  "{bg}",
    "primary":     "{text}",
    "secondary":   "{muted}",
    "highlight":   "{accent}",
}


# ── Dispatcher: resolves "{key}" references to final hex values ─────

def _resolve(config: dict) -> dict:
    """Resolve {ref} strings in config values to their target hex values."""
    resolved = {}
    for key, val in config.items():
        if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
            ref = val[1:-1]
            resolved[key] = config[ref]  # one-level lookup
        else:
            resolved[key] = val
    return resolved


COLORS = _resolve(COLORS)


# ── Convenience accessors (derived, not duplicated) ────────────────
# These are NOT separate constants — they point into the single dict.
# Scenes import these for readability, but the truth is always COLORS.

BG_COLOR     = COLORS["bg"]
TEXT_COLOR   = COLORS["text"]
ACCENT_COLOR = COLORS["accent"]
MUTED_COLOR  = COLORS["muted"]

# Semantic aliases (derived from role mapping, not hardcoded)
BACKGROUND = COLORS["background"]
PRIMARY    = COLORS["primary"]
SECONDARY  = COLORS["secondary"]
HIGHLIGHT  = COLORS["highlight"]
