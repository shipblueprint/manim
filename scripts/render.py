#!/usr/bin/env python3
"""Unified renderer for all manim scenes (Linux only)."""
import sys
import os
import importlib
import subprocess
import argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Scene registry: (module_path, class_name, category)
SCENES = [
    # Architecture
    ("manim_assets.scenes.architecture.system_flow", "SystemFlowScene", "architecture"),
    # Calculus
    ("manim_assets.scenes.calculus.function_graph", "FunctionGraphScene", "calculus"),
    ("manim_assets.scenes.calculus.derivative_tangent", "DerivativeTangentScene", "calculus"),
    ("manim_assets.scenes.calculus.integral_area", "IntegralAreaScene", "calculus"),
    ("manim_assets.scenes.calculus.limit_sequence", "LimitSequenceScene", "calculus"),
    # Linear Algebra
    ("manim_assets.scenes.linear_algebra.vector_operations", "VectorOperationsScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.vector_operations", "Vector2DScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.vector_operations", "Vector3DScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.matrix_ops", "MatrixOpsScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.matrix_ops", "MatrixTransformScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.linear_transform", "LinearTransformScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.linear_transform", "RotationScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.linear_transform", "ShearScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.linear_transform", "ScaleScene", "linear_algebra"),
    ("manim_assets.scenes.linear_algebra.eigen_visualization", "EigenScene", "linear_algebra"),
    # Geometry
    ("manim_assets.scenes.geometry.basic_shapes", "BasicShapesScene", "geometry"),
    ("manim_assets.scenes.geometry.basic_shapes", "PolygonScene", "geometry"),
    ("manim_assets.scenes.geometry.transformations", "TransformScene", "geometry"),
    ("manim_assets.scenes.geometry.transformations", "ReflectionScene", "geometry"),
    ("manim_assets.scenes.geometry.transformations", "RotationCenterScene", "geometry"),
    ("manim_assets.scenes.geometry.tessellations", "TessellationScene", "geometry"),
    ("manim_assets.scenes.geometry.tessellations", "SymmetryGroupScene", "geometry"),
    ("manim_assets.scenes.geometry.solids_3d", "Solids3DScene", "geometry"),
    ("manim_assets.scenes.geometry.solids_3d", "PolyhedronScene", "geometry"),
    ("manim_assets.scenes.geometry.solids_3d", "PlatonicSolidsScene", "geometry"),
    # Data Structures
    ("manim_assets.scenes.data_structures.linked_list", "LinkedListScene", "data_structures"),
    ("manim_assets.scenes.data_structures.linked_list", "LinkedListInsertScene", "data_structures"),
    ("manim_assets.scenes.data_structures.linked_list", "LinkedListTraversalScene", "data_structures"),
    ("manim_assets.scenes.data_structures.binary_tree", "BinaryTreeScene", "data_structures"),
    ("manim_assets.scenes.data_structures.binary_tree", "BinaryTreeTraversalScene", "data_structures"),
    ("manim_assets.scenes.data_structures.graph", "GraphScene", "data_structures"),
    ("manim_assets.scenes.data_structures.graph", "GraphTraversalScene", "data_structures"),
    ("manim_assets.scenes.data_structures.sorting", "SortingScene", "data_structures"),
    ("manim_assets.scenes.data_structures.sorting", "QuickSortScene", "data_structures"),
    ("manim_assets.scenes.data_structures.sorting", "MergeSortScene", "data_structures"),
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


def render_scene(mod_name, cls_name, category=None, quality="low_quality"):
    from manim import config
    config.transparent = True
    config.pixel_width = 854
    config.pixel_height = 480
    if quality == "medium_quality":
        config.pixel_width = 1280
        config.pixel_height = 720
    elif quality == "high_quality":
        config.pixel_width = 1920
        config.pixel_height = 1080

    mod = importlib.import_module(mod_name)
    cls = getattr(mod, cls_name)
    scene = cls()
    scene.render()

    if category:
        import shutil
        media_dir = os.path.join(ROOT, "media", "videos")
        src_file = None
        if os.path.isdir(media_dir):
            for quality_dir in os.listdir(media_dir):
                candidate = os.path.join(media_dir, quality_dir, f"{cls_name}.mov")
                if os.path.exists(candidate):
                    src_file = candidate
                    break
        if src_file:
            quality_dir = os.path.dirname(src_file)
            dst_dir = os.path.join(quality_dir, category)
            os.makedirs(dst_dir, exist_ok=True)
            dst_file = os.path.join(dst_dir, f"{cls_name}.mov")
            shutil.move(src_file, dst_file)
            print(f"Moved to: {dst_file}")


def main():
    parser = argparse.ArgumentParser(description="Render manim scenes")
    parser.add_argument("--scene", help="Scene class name")
    parser.add_argument("--category", help="Only render scenes in category")
    parser.add_argument("--all", action="store_true", help="Render all scenes")
    parser.add_argument("--quality", default="low_quality", choices=["low_quality", "medium_quality", "high_quality"])
    parser.add_argument("--clear", action="store_true", help="Clear media/videos before rendering")
    args = parser.parse_args()

    if args.clear and os.path.exists(os.path.join(ROOT, "media", "videos")):
        import shutil
        shutil.rmtree(os.path.join(ROOT, "media", "videos"))

    if args.scene:
        for mod, cls, cat in SCENES:
            if cls == args.scene:
                render_scene(mod, cls, cat, args.quality)
                return
        print(f"Scene {args.scene} not found", file=sys.stderr)
        sys.exit(1)
    elif args.category:
        for mod, cls, cat in SCENES:
            if cat == args.category:
                print(f"\n=== {cat}/{cls} ===")
                render_scene(mod, cls, cat, args.quality)
        return
    elif args.all:
        failed = []
        for mod, cls, cat in SCENES:
            print(f"\n=== {cat}/{cls} ===")
            try:
                render_scene(mod, cls, cat, args.quality)
            except Exception as e:
                failed.append(f"{cat}/{cls}: {e}")
                print(f"FAILED: {e}", file=sys.stderr)
        if failed:
            print(f"\nFailed ({len(failed)}):", file=sys.stderr)
            for f in failed:
                print(f"  - {f}", file=sys.stderr)
            sys.exit(1)
        print("\nAll scenes rendered successfully!")
        return
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
