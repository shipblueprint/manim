# Manim Assets — Mathematical Animation Library

[![GitHub](https://img.shields.io/badge/GitHub-shipblueprint%2Fmanimlib-blue?logo=github)](https://github.com/shipblueprint/manimlib)

A premium **Manim** (Mathematical Animation) asset library for creating high-quality math visualizations — statistics, calculus, linear algebra, geometry, machine learning, data structures, CS theory, and more.

Built with [Manim](https://github.com/ManimCommunity/manim/) (the community-maintained fork of 3Blue1Brown's animation engine).

---

## Features

- 📐 **50+ Animated Scenes** across 9 categories — ready to render and use in educational content.
- 🎨 **Unified Dark Theme** — A config-driven color palette (`config/colors.py`) ensures every scene uses consistent, premium styling. Change one dict → all scenes update.
- 🖥️ **Batch Rendering** — Render all scenes at once with `render_all.bat`, or render individual scenes with `render_scene.py`.
- 🧩 **Modular Architecture** — Each scene is an independent Python class in a well-organized package structure.
- 🌐 **Transparent Background** — Rendered with transparent background (`config.transparent = True`) for easy compositing in video editors.
- 🔧 **Cross-Platform** — Manim runs on Windows, macOS, and Linux.

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
│   │   └── colors.py           # Single-source-of-truth color palette
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
├── manim_env/                  # Python virtual environment (Manim installed)
├── media/                      # Rendered output (gitignored)
├── render_scene.py             # Render a single scene by module/class name
├── render_new.py               # Batch render the 15 "new" scenes
├── render_all.bat              # Batch render ALL scenes (50+)
└── .gitignore
```

---

## Quick Start

### Prerequisites

- **Python 3.8+**
- **Manim** (installed in the virtual environment or globally)
- **MiKTeX** (optional, for LaTeX rendering) — path is configured in the render scripts

### Render a Single Scene

```bash
python render_scene.py manim_assets.scenes.statistics.normal_distribution NormalDistributionScene statistics
```

Arguments:
1. Python module path to the scene
2. Scene class name
3. Category folder name (output is organized into subfolders)

### Render All Scenes

Simply run:

```bash
render_all.bat
```

This clears previous renders, then renders every scene in sequence, organizing output by category.

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

---

## Scene Architecture

Each scene is a Python class that inherits from `manim.Scene` and implements a `construct()` method:

```python
from manim import Scene, ...
from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR

class MyScene(Scene):
    def construct(self):
        # Your animation code here
        pass
```

### Color System

Colors are defined once in `manim_assets/config/colors.py` and resolved through a data-driven config:

| Accessor | Usage | Default Value |
|----------|-------|---------------|
| `BG_COLOR` | Background fill | `#0F0F12` |
| `TEXT_COLOR` | Primary text & objects | `#EBE4D5` |
| `ACCENT_COLOR` | Highlighted elements | `#FF6B4A` |
| `MUTED_COLOR` | Secondary/supporting elements | `#7A7570` |

To change the entire color scheme, edit only the `COLORS` dict in `colors.py`.

---

## Development

### Setting Up a Virtual Environment

```bash
python -m venv manim_env
manim_env\Scripts\activate   # Windows
# source manim_env/bin/activate  # macOS/Linux
pip install manim
```

### Adding a New Scene

1. Choose the category directory (or create a new one in `manim_assets/scenes/`).
2. Create a new Python file with your scene class.
3. Import colors from `manim_assets.config.colors`.
4. Add the scene to `render_all.bat` (or `render_new.py` for new additions).
5. Render using `render_scene.py`.

### Color Palette Architecture

The color system uses a **single-source-of-truth** pattern:
- `COLORS` dict in `colors.py` contains raw hex values and semantic role mappings.
- `_resolve()` resolves `{ref}` placeholders.
- Convenience variables (`BG_COLOR`, `TEXT_COLOR`, etc.) are derived from the dict — never duplicated.
- Scenes import convenience variables for readability, but the truth is always the dict.

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

[ISC](https://opensource.org/licenses/ISC) — see [LICENSE](LICENSE) (if applicable).

---

*Built with [Manim Community](https://www.manim.community/) — the mathematical animation engine.*
