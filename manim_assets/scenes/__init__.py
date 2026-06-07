"""Scenes package for Manim Assets."""

from .architecture import SystemFlowScene
from .calculus import FunctionGraphScene, DerivativeTangentScene, IntegralAreaScene, LimitSequenceScene
from .data_structures import SortingScene, QuickSortScene, MergeSortScene, BinaryTreeScene, GraphScene, LinkedListScene
from .geometry import BasicShapesScene, ReflectionScene, RotationCenterScene, TransformScene, TessellationScene, Solids3DScene
from .linear_algebra import Vector2DScene, Vector3DScene, VectorOperationsScene, MatrixOpsScene, LinearTransformScene, RotationScene, ShearScene, ScaleScene, EigenScene
from .statistics import NormalDistributionScene, HistogramScene, ScatterRegressionScene, BayesTreeScene, CentralLimitTheoremScene
from .ml import GradientDescentScene, NeuralNetworkScene, DecisionBoundaryScene, KMeansScene
from .advanced_math import FourierSeriesScene, UnitCircleSineScene, ParametricCurvesScene
from .cs_theory import HashTableScene, StackQueueScene, RecursionStackScene

__all__ = [
    # Architecture
    "SystemFlowScene",
    # Calculus
    "FunctionGraphScene",
    "DerivativeTangentScene",
    "IntegralAreaScene",
    "LimitSequenceScene",
    # Data Structures
    "SortingScene",
    "QuickSortScene",
    "MergeSortScene",
    "BinaryTreeScene",
    "GraphScene",
    "LinkedListScene",
    # Geometry
    "BasicShapesScene",
    "ReflectionScene",
    "RotationCenterScene",
    "TransformScene",
    "TessellationScene",
    "Solids3DScene",
    # Linear Algebra
    "Vector2DScene",
    "Vector3DScene",
    "VectorOperationsScene",
    "MatrixOpsScene",
    "LinearTransformScene",
    "RotationScene",
    "ShearScene",
    "ScaleScene",
    "EigenScene",
    # Statistics / Probability
    "NormalDistributionScene",
    "HistogramScene",
    "ScatterRegressionScene",
    "BayesTreeScene",
    "CentralLimitTheoremScene",
    # Machine Learning / AI
    "GradientDescentScene",
    "NeuralNetworkScene",
    "DecisionBoundaryScene",
    "KMeansScene",
    # Advanced Math
    "FourierSeriesScene",
    "UnitCircleSineScene",
    "ParametricCurvesScene",
    # CS Theory
    "HashTableScene",
    "StackQueueScene",
    "RecursionStackScene",
]
