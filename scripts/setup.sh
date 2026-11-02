#!/usr/bin/env bash
# Set up a render environment for Manim Assets on Linux or macOS.
#
#   ./setup.sh              install system deps, create .venv, install manim, smoke render
#   ./setup.sh --skip-deps  do not install system packages; stops unless pkg-config already
#                           finds pangocairo/cairo (e.g. you installed them yourself)
#   ./setup.sh --no-smoke   stop after the Python environment is ready
#
# The Windows workflow (manim_env + render_all.bat) does not use this script.
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$(pwd)"
VENV=".venv"

SKIP_DEPS=0
NO_SMOKE=0
for arg in "$@"; do
  case "$arg" in
    --skip-deps) SKIP_DEPS=1 ;;
    --no-smoke)  NO_SMOKE=1 ;;
    -h|--help)   sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

log() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die() { printf '\033[31m%s\033[0m\n' "$*" >&2; exit 1; }

# Running this whole script as root would make .venv root-owned; the system-package
# step calls sudo on its own.
if [ "$(id -u)" = 0 ] && [ -z "${SETUP_ALLOW_ROOT:-}" ]; then
  die "Do not run ./setup.sh under sudo. Run it as your normal user — it invokes sudo itself for the system packages. (Override: SETUP_ALLOW_ROOT=1 sudo ./setup.sh)"
fi

# ── System dependencies ────────────────────────────────────────────────
# pycairo and manimpango compile against Pango/Cairo headers; manim shells out to ffmpeg.
# The ffmpeg *development* package is deliberately not requested: on some distros it
# conflicts with the ffmpeg build already installed, and manim only needs the binary.
log "Checking system dependencies"
missing=()
pkg-config --exists pangocairo 2>/dev/null || missing+=("pangocairo")
pkg-config --exists cairo      2>/dev/null || missing+=("cairo")
command -v ffmpeg >/dev/null   || missing+=("ffmpeg")

if [ ${#missing[@]} -gt 0 ]; then
  log "Missing: ${missing[*]}"

  if command -v brew >/dev/null; then
    INSTALL_CMD=(brew install)
    DEPS="pkg-config cairo pango libjpeg-turbo ffmpeg"
  elif command -v dnf >/dev/null; then
    INSTALL_CMD=(dnf install -y)
    DEPS="gcc gcc-c++ make pkg-config pango-devel cairo-devel fontconfig-devel python3-devel"
  elif command -v apt-get >/dev/null; then
    INSTALL_CMD=(apt-get install -y)
    DEPS="build-essential pkg-config libpango1.0-dev libcairo2-dev libgdk-pixbuf-2.0-dev libjpeg-dev ffmpeg python3 python3-venv fontconfig"
    APT_UPDATE=1
  elif command -v pacman >/dev/null; then
    INSTALL_CMD=(pacman -Sy --noconfirm)
    DEPS="base-devel pkgconf pango cairo gdk-pixbuf2 libjpeg-turbo ffmpeg python fontconfig"
  else
    die "No supported package manager found. Install Pango, Cairo and ffmpeg manually, then re-run with --skip-deps."
  fi

  # dnf/pacman abort on names that are unavailable or already installed.
  if command -v rpm >/dev/null; then
    wanted=()
    for pkg in $DEPS; do
      rpm -q "$pkg" >/dev/null 2>&1 || wanted+=("$pkg")
    done
    DEPS="${wanted[*]:-}"
  fi
  REMEDIATION="sudo sh -c '${INSTALL_CMD[*]} $DEPS'"

  if [ "$SKIP_DEPS" = 1 ]; then
    # The headers are what manimpango/pycairo compile against; skipping the install
    # does not make the build any less fatal, so stop here instead of burning a failed build.
    echo "--skip-deps given, but pkg-config still cannot find them, and 'Installing manim' would fail."
    echo "Install them first:"
    echo "  $REMEDIATION"
    echo "(or export PKG_CONFIG_PATH to where they live, then re-run)"
    exit 1
  elif [ -z "$DEPS" ]; then
    echo "nothing left to install, continuing"
  elif [ "${INSTALL_CMD[0]}" = "brew" ]; then
    "${INSTALL_CMD[@]}" $DEPS
  elif [ "${APT_UPDATE:-0}" = 1 ]; then
    sudo sh -c "apt-get update && ${INSTALL_CMD[*]} $DEPS"
  elif [ "$(id -u)" = 0 ]; then
    sh -c "${INSTALL_CMD[*]} $DEPS"
  elif sudo -n true 2>/dev/null || [ -t 0 ]; then
    sudo sh -c "${INSTALL_CMD[*]} $DEPS"
  else
    die "System packages need root and this shell cannot prompt for a password. Run:
  ! $REMEDIATION
then re-run ./setup.sh"
  fi
else
  echo "all present"
fi

# ── Virtual environment ────────────────────────────────────────────────
# theme.py parses theme.toml with stdlib tomllib, so Python 3.11+ is required.
log "Python environment"
if [ -x "$VENV/bin/python" ]; then
  echo "reusing $VENV ($("$VENV/bin/python" -V 2>&1))"
  if command -v uv >/dev/null; then
    PIP() { uv pip install --python "$VENV/bin/python" "$@"; }
  else
    PIP() { "$VENV/bin/python" -m pip install "$@"; }
  fi
elif command -v uv >/dev/null; then
  uv venv --python 3.11 "$VENV"
  PIP() { uv pip install --python "$VENV/bin/python" "$@"; }
else
  python3 - <<'EOF' || die "Python 3.11+ is required (stdlib tomllib). Install it or use uv."
import sys
sys.exit(0 if sys.version_info >= (3, 11) else 1)
EOF
  python3 -m venv "$VENV"
  PIP() { "$VENV/bin/python" -m pip install "$@"; }
fi

log "Installing manim ${MANIM_VERSION:+$MANIM_VERSION}"
if [ -n "${MANIM_VERSION:-}" ]; then
  PIP "manim==$MANIM_VERSION"
else
  PIP manim
fi

# ── Verify the theme resolves ──────────────────────────────────────────
log "Verifying theme.toml tokens and brand fonts"
PYTHONPATH="$ROOT" "$VENV/bin/python" - <<'EOF'
from manim import Text
from manim_assets.config import (ACCENT_COLOR, BG_COLOR, BODY_FONT, HEADING_FONT,
                                 MUTED_COLOR, TEXT_COLOR)

available = set(Text.font_list())
print(f"  background {BG_COLOR}  text {TEXT_COLOR}  accent {ACCENT_COLOR}  muted {MUTED_COLOR}")
for name in (HEADING_FONT, BODY_FONT):
    status = "ok" if name in available else "MISSING - Pango will substitute a fallback"
    print(f"  font {name}: {status}")
EOF

# ── Smoke render ───────────────────────────────────────────────────────
if [ "$NO_SMOKE" = 0 ]; then
  log "Smoke render (low quality PNG)"
  PYTHONPATH="$ROOT" "$VENV/bin/manim" -s -q l --format=png \
    manim_assets/scenes/calculus/function_graph.py FunctionGraphScene
  echo "  Look at the PNG under media/images/... to confirm the brand colors and fonts."
fi

log "Done"
cat <<EOF
Render a scene:
  PYTHONPATH=$ROOT $VENV/bin/python render_scene.py <module> <Class> <category>
Render everything (Windows batch script, needs a Windows shell):
  render_all.bat
EOF
