# Manim Assets — Mathematical Animation Library

[![GitHub](https://img.shields.io/badge/GitHub-shipblueprint%2Fmanim-blue)](https://github.com/shipblueprint/manim)

A premium **Manim** (Mathematical Animation) asset library for creating high-quality math visualizations — statistics, calculus, linear algebra, geometry, machine learning, data structures, CS theory, and more.

Built with [Manim Community](https://github.com/ManimCommunity/manim/) (the community-maintained fork of 3Blue1Brown's animation engine).

---

## Features

- 📐 **50 Animated Scenes** across 9 categories — ready to render and use in educational content.
- 🎨 **Brand Theme as Data** — All colors and fonts come from `config/theme.toml`, loaded by `config/theme.py`. Change the theme file → every scene updates; scene code never hardcodes a hex value or a font name.
- 🖥️ **Batch Rendering** — Render all scenes at once with `render_all.bat`, or render individual scenes with `render_scene.py`.
- 🧩 **Modular Architecture** — Each scene is an independent Python class in a well-organized package structure.
- 🌐 **Transparent Background** — masters render with alpha (`config.transparent = True`) for easy compositing in video editors, and `flatten_previews.py` writes brand-colored, opaque copies for review.
- 🔧 **Cross-Platform** — scenes render on Windows (`manim_env` + `render_all.bat`) and on Linux/macOS (`setup.sh`).

---

## Scene Categories

| Category | Scenes | Topics |
|----------|--------|--------|
| **Architecture** | 1 | System flow diagrams |
| **Calculus** | 4 | Function graphs, derivatives, integrals, sequences/limits |
| **Linear Algebra** | 10 | Vector ops (2D/3D), matrix ops, linear transforms (rotation, shear, scale), eigenvalues |
| **Geometry** | 10 | Basic shapes, polygons, transformations (reflection, rotation), tessellations, 3D solids, platonic solids |
| **Data Structures** | 10 | Linked lists (insert, traversal), binary trees (traversal), graphs (traversal), sorting (quicksort, mergesort) |
| **Statistics / Probability** | 5 | Normal distribution, histograms, scatter/regression, Bayes trees, central limit theorem |
| **Machine Learning / AI** | 4 | Gradient descent, neural networks, decision boundaries, K-means clustering |
| **Advanced Math** | 3 | Fourier series, unit circle / sine, parametric curves |
| **CS Theory** | 3 | Hash tables, stack/queue, recursion stack |

---

## Project Structure

```
manim/
├── manim_assets/               # Python package — all scene code
│   ├── __init__.py             # Package init, exports
│   ├── pyproject.toml          # Package metadata
│   ├── config/
│   │   ├── __init__.py
│   │   ├── theme.toml          # Single source of truth: brand palette + fonts
│   │   ├── theme.py            # Loads theme.toml, registers fonts, exports tokens
│   │   └── fonts/              # playfairdisplay.ttf, inter.ttf (+ OFL licenses)
│   └── scenes/
│       ├── __init__.py
│       ├── architecture/
│       │   └── system_flow.py
│       ├── calculus/
│       │   ├── derivative_tangent.py
│       │   ├── function_graph.py
│       │   ├── integral_area.py
│       │   └── limit_sequence.py
│       ├── linear_algebra/
│       │   ├── eigen_visualization.py
│       │   ├── linear_transform.py
│       │   ├── matrix_ops.py
│       │   └── vector_operations.py
│       ├── geometry/
│       │   ├── basic_shapes.py
│       │   ├── solids_3d.py
│       │   ├── tessellations.py
│       │   └── transformations.py
│       ├── data_structures/
│       │   ├── binary_tree.py
│       │   ├── graph.py
│       │   ├── linked_list.py
│       │   └── sorting.py
│       ├── statistics/
│       │   ├── bayes_tree.py
│       │   ├── central_limit.py
│       │   ├── histogram.py
│       │   ├── normal_distribution.py
│       │   └── scatter_regression.py
│       ├── ml/
│       │   ├── decision_boundary.py
│       │   ├── gradient_descent.py
│       │   ├── kmeans.py
│       │   └── neural_network.py
│       ├── advanced_math/
│       │   ├── fourier_series.py
│       │   ├── parametric_curves.py
│       │   └── unit_circle_sine.py
│       └── cs_theory/
│           ├── hash_table.py
│           ├── recursion_stack.py
│           └── stack_queue.py
├── manim_env/                  # Windows venv (uv, Python 3.11) — gitignored
├── media/                      # Rendered output (gitignored): videos/ masters, preview/ opaque copies
├── brand-design-guidelines.html # Source of the palette and type scale in theme.toml
├── render_scene.py             # Render a single scene by module/class name
├── render_new.py               # Batch render the 15 "new" scenes
├── flatten_previews.py         # Flatten the alpha masters into media/preview/*.mp4
├── render_all.bat              # Batch render all 50 scenes (Windows)
├── setup.sh                    # Linux/macOS install: system deps + .venv + manim + smoke render
└── .gitignore
```

---

## Quick Start

### Prerequisites

- **Python 3.11+** (the theme loader uses stdlib `tomllib`)
- **Manim** — the community edition, installed in the virtual environment
- **Pango, Cairo and ffmpeg** (Linux/macOS) — `./setup.sh` installs them
- No LaTeX: every string, including axis labels, is drawn with Pango (`Text`). `theme.py` sets `NumberLine.set_default(label_constructor=Text)`, which replaces Manim's default `MathTex` digits — without it, any scene with numbered axes shells out to `latex` + `dvisvgm`.

### Render a Single Scene

```bash
python render_scene.py manim_assets.scenes.statistics.normal_distribution NormalDistributionScene statistics
```

Arguments:
1. Python module path to the scene
2. Scene class name
3. Category folder name (output is organized into subfolders)

On Linux/macOS, prefix with the venv interpreter and `PYTHONPATH`:

```bash
PYTHONPATH=. .venv/bin/python render_scene.py manim_assets.scenes.statistics.normal_distribution NormalDistributionScene statistics
```

### Render All Scenes

Windows:

```bat
render_all.bat
```

This clears previous renders, then renders all 50 scenes in sequence, organizing output by category.
There is no shell equivalent yet — on Linux/macOS, drive `render_scene.py` from the list in
`render_all.bat` or `render_new.py`.

### Render the 15 New Scenes Only

```bash
python render_new.py
```

### Output

Rendered `.mov` files are placed in:
```
media/videos/<quality>/<category>/<SceneName>.mov
```

The `render_scene.py` script moves output to the correct category subfolder automatically.

### Review Previews (opaque, brand background baked in)

The `.mov` masters carry an alpha channel, so the Espresso background they store is
transparent (`alpha = 0`) and players composite them over black. To get videos that show
the theme as-is, flatten the masters over `BG_COLOR`:

```bash
PYTHONPATH=. .venv/bin/python flatten_previews.py
```

That writes `media/preview/<category>/<SceneName>.mp4` next to — never in place of — the
masters, skipping previews that are newer than their source. Renders stay alpha-clean for
compositing; previews are what you send to someone for approval.

---

## Scene Architecture

Each scene is a Python class that inherits from `manim.Scene` and implements a `construct()` method:

```python
from manim import Scene, Text, ...
from manim_assets.config import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, HEADING_FONT

class MyScene(Scene):
    def construct(self):
        title = Text("My Scene", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        # Your animation code here
        pass
```

### Theme (colors and fonts)

Everything visual is defined once in `manim_assets/config/theme.toml` — the brand palette
(from `brand-design-guidelines.html`), the role mapping, and the two brand fonts:

| Token | Role | Value |
|-------|------|-------|
| `BG_COLOR` | `roles.background` — Espresso, per the guidelines' Videos row | `#432818` |
| `TEXT_COLOR` | `roles.foreground` — Ivory Porcelain on-screen text | `#EFE3D2` |
| `ACCENT_COLOR` | `roles.accent` — Harvest Gold curves, highlights, lower-thirds | `#BB9457` |
| `MUTED_COLOR` | `roles.muted` — Rust Clay axes, grid, secondary labels | `#99582A` |
| `HEADING_FONT` | Scene titles | `Playfair Display` |
| `BODY_FONT` | Everything else; applied globally via `Text.set_default()` | `Inter` |

`theme.toml` also keeps `deep_maroon` / `ink` in `[palette]`, and the `callout` role
(`#6F1D1B`) is meant as a keyword-pill *fill* under `TEXT_COLOR` text — Deep Maroon is too
dark to read as text on the Espresso background.

### Writing a scene that stays on-brand

The theme only reaches a scene through its imports, so these rules are what keep
`theme.toml` authoritative:

```python
from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR          # 1. never config.background_color
        title = Text("My Scene", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        axes = Axes(
            axis_config={"stroke_color": MUTED_COLOR, "include_numbers": True},
        )
        curve = axes.plot(lambda x: x ** 2, color=ACCENT_COLOR)   # 2. token, not "#BB9457"
```

1. Set `self.camera.background_color = BG_COLOR` inside `construct()`.
2. Take every color from `manim_assets.config`. No hex literals, no `color.rgb(...)`, and
   none of Manim's named colors (`BLUE`, `GREEN`, `YELLOW`, …) — they are all cool-toned and
   break the palette. Map what you would have used onto a role instead.
3. Titles get `font=HEADING_FONT` explicitly; everything else inherits `Inter` from
   `Text.set_default()`, so plain `Text(...)` is already correct.
4. Don't reach for `Tex` / `MathTex`. They bypass the bundled fonts *and* require a TeX
   distribution. Axis numbers already render through `Text` (see
   `NumberLine.set_default(label_constructor=Text)` in `theme.py`); for the rare glyph that
   LaTeX would have provided, write it out (`"mu = 0"`, `"x^2"` → `"x²"`).
5. Use `ACCENT_COLOR` for anything that should draw the eye, `MUTED_COLOR` for structure
   (axes, grids, secondary labels), `TEXT_COLOR` for reading text, and `callout` only as a
   fill behind `TEXT_COLOR` text.

`flatten_previews.py` is the check: after rendering, it flattens the masters over
`BG_COLOR`, so a preview that looks off-theme is a scene that broke rule 2.

### Rebranding

Edit `[palette]` and `[roles]` in `theme.toml`, swap the `.ttf` files in
`manim_assets/config/fonts/`, and re-render — nothing in `manim_assets/scenes/` changes:

```toml
[palette]
harvest_gold = "#BB9457"   # -> any hex; ACCENT_COLOR follows
```

A role must name a `[palette]` key; a typo raises at import time rather than silently
rendering the old color. Requires Python 3.11+ (stdlib `tomllib`, so no extra dependency).

---

## Development

### Setting Up an Environment

**Windows** (the workflow this repo is used with) — a uv-managed venv named `manim_env`, Python 3.11:

```powershell
uv venv --python 3.11 manim_env
manim_env\Scripts\activate        # PowerShell: .\manim_env\Scripts\Activate.ps1
uv pip install manim
```

**Linux / macOS** — one command installs system dependencies, creates `.venv`, installs Manim,
verifies the theme tokens resolve, and writes a low-quality smoke-render PNG:

```bash
./setup.sh              # needs sudo for the system packages
./setup.sh --skip-deps  # re-run after installing the packages yourself
./setup.sh --no-smoke   # stop once the Python environment is ready
```

`MANIM_VERSION=0.20.1 ./setup.sh` pins the version to match the Windows venv.

### Adding a New Scene

1. Choose the category directory (or create a new one in `manim_assets/scenes/`).
2. Create a new Python file with your scene class.
3. Follow the rules in [Writing a scene that stays on-brand](#writing-a-scene-that-stays-on-brand) — theme tokens only, never a raw hex value or font name.
4. Add the scene to `render_all.bat` (or `render_new.py` for new additions).
5. Render with `render_scene.py` (1080p60, transparent `.mov`), then `flatten_previews.py` for a copy you can actually review.

### Theme Architecture

The theme uses a **single-source-of-truth** pattern:
- `theme.toml` holds the raw brand `[palette]`, the `[roles]` that map a role to a palette entry, and the `[fonts]`.
- `theme.py` loads it with stdlib `tomllib`, validates that every role points at a real palette key, registers every `.ttf`/`.otf` in `config/fonts/` with Pango (`manimpango.register_font`), sets `Inter` as the default `Text` font, and routes axis labels through `Text` instead of `MathTex`.
- Tokens (`BG_COLOR`, `TEXT_COLOR`, `HEADING_FONT`, …) are derived from the file — never duplicated in Python.
- If a brand font is neither bundled in `config/fonts/` nor installed on the system, import warns once and Pango substitutes a fallback.

`config/fonts/` ships `playfairdisplay.ttf` and `inter.ttf` (variable fonts, SIL Open Font
License, from the [google/fonts](https://github.com/google/fonts) repository) together with
their `*-OFL.txt`. Rendering therefore uses the brand typefaces without a system install.

---

## Contributing

Contributions, issues, and scene requests are welcome!  
Feel free to check the [issues page](https://github.com/shipblueprint/manimlib/issues).

Ideas for new scenes:
- More calculus visualizations (Taylor series, vector fields)
- Differential equations
- Complex analysis
- Number theory
- Set theory / logic
- Cryptography basics

---

## License

ISC — no `LICENSE` file has been added to the repo yet.

The bundled typefaces (`manim_assets/config/fonts/`) are under the SIL Open Font License,
with their license texts alongside them: `playfairdisplay-OFL.txt`, `inter-OFL.txt`.

---

*Built with [Manim Community](https://www.manim.community/) — the mathematical animation engine.*
