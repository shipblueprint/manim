"""Render all 15 new scenes organized by category."""
import os
import subprocess
import sys

# Add MiKTeX to PATH
os.environ['PATH'] = os.environ.get('PATH', '') + r';C:\Users\lee\AppData\Local\Programs\MiKTeX\miktex\bin\x64'

PYTHON = os.path.join(os.path.dirname(__file__), "manim_env", "Scripts", "python.exe")
RENDER = os.path.join(os.path.dirname(__file__), "render_scene.py")

# (module, class, category_folder)
SCENES = [
    # Statistics / Probability
    ("manim_assets.scenes.statistics.normal_distribution", "NormalDistributionScene", "statistics"),
    ("manim_assets.scenes.statistics.histogram", "HistogramScene", "statistics"),
    ("manim_assets.scenes.statistics.scatter_regression", "ScatterRegressionScene", "statistics"),
    ("manim_assets.scenes.statistics.bayes_tree", "BayesTreeScene", "statistics"),
    ("manim_assets.scenes.statistics.central_limit", "CentralLimitTheoremScene", "statistics"),
    # Machine Learning / AI
    ("manim_assets.scenes.ml.gradient_descent", "GradientDescentScene", "ml"),
    ("manim_assets.scenes.ml.neural_network", "NeuralNetworkScene", "ml"),
    ("manim_assets.scenes.ml.decision_boundary", "DecisionBoundaryScene", "ml"),
    ("manim_assets.scenes.ml.kmeans", "KMeansScene", "ml"),
    # Advanced Math
    ("manim_assets.scenes.advanced_math.fourier_series", "FourierSeriesScene", "advanced_math"),
    ("manim_assets.scenes.advanced_math.unit_circle_sine", "UnitCircleSineScene", "advanced_math"),
    ("manim_assets.scenes.advanced_math.parametric_curves", "ParametricCurvesScene", "advanced_math"),
    # CS Theory
    ("manim_assets.scenes.cs_theory.hash_table", "HashTableScene", "cs_theory"),
    ("manim_assets.scenes.cs_theory.stack_queue", "StackQueueScene", "cs_theory"),
    ("manim_assets.scenes.cs_theory.recursion_stack", "RecursionStackScene", "cs_theory"),
]

failed = []
for mod, cls, cat in SCENES:
    label = f"{cat}/{mod.split('.')[-1]}.{cls}"
    print(f"\n=== Rendering {label} ===")
    result = subprocess.run(
        [PYTHON, RENDER, mod, cls, cat],
        cwd=os.path.dirname(__file__),
    )
    if result.returncode != 0:
        failed.append(label)
        print(f"  FAILED: {label}")
    else:
        print(f"  OK: {label}")

print("\n" + "=" * 50)
if failed:
    print(f"FAILED ({len(failed)}):")
    for f in failed:
        print(f"  - {f}")
else:
    print("All 15 new scenes rendered successfully!")
