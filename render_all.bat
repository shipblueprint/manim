@echo off
set PATH=%PATH%;C:\Users\lee\AppData\Local\Programs\MiKTeX\miktex\bin\x64
call manim_env\Scripts\activate.bat

echo Clearing old renders and cache...
if exist media\videos rmdir /s /q media\videos
if exist media\Tex rmdir /s /q media\Tex

echo === Architecture ===
python render_scene.py manim_assets.scenes.architecture.system_flow SystemFlowScene architecture

echo === Calculus ===
python render_scene.py manim_assets.scenes.calculus.function_graph FunctionGraphScene calculus
python render_scene.py manim_assets.scenes.calculus.derivative_tangent DerivativeTangentScene calculus
python render_scene.py manim_assets.scenes.calculus.integral_area IntegralAreaScene calculus
python render_scene.py manim_assets.scenes.calculus.limit_sequence LimitSequenceScene calculus

echo === Linear Algebra ===
python render_scene.py manim_assets.scenes.linear_algebra.vector_operations VectorOperationsScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.vector_operations Vector2DScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.vector_operations Vector3DScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.matrix_ops MatrixOpsScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.matrix_ops MatrixTransformScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.linear_transform LinearTransformScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.linear_transform RotationScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.linear_transform ShearScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.linear_transform ScaleScene linear_algebra
python render_scene.py manim_assets.scenes.linear_algebra.eigen_visualization EigenScene linear_algebra

echo === Geometry ===
python render_scene.py manim_assets.scenes.geometry.basic_shapes BasicShapesScene geometry
python render_scene.py manim_assets.scenes.geometry.basic_shapes PolygonScene geometry
python render_scene.py manim_assets.scenes.geometry.transformations TransformScene geometry
python render_scene.py manim_assets.scenes.geometry.transformations ReflectionScene geometry
python render_scene.py manim_assets.scenes.geometry.transformations RotationCenterScene geometry
python render_scene.py manim_assets.scenes.geometry.tessellations TessellationScene geometry
python render_scene.py manim_assets.scenes.geometry.tessellations SymmetryGroupScene geometry
python render_scene.py manim_assets.scenes.geometry.solids_3d Solids3DScene geometry
python render_scene.py manim_assets.scenes.geometry.solids_3d PolyhedronScene geometry
python render_scene.py manim_assets.scenes.geometry.solids_3d PlatonicSolidsScene geometry

echo === Data Structures ===
python render_scene.py manim_assets.scenes.data_structures.linked_list LinkedListScene data_structures
python render_scene.py manim_assets.scenes.data_structures.linked_list LinkedListInsertScene data_structures
python render_scene.py manim_assets.scenes.data_structures.linked_list LinkedListTraversalScene data_structures
python render_scene.py manim_assets.scenes.data_structures.binary_tree BinaryTreeScene data_structures
python render_scene.py manim_assets.scenes.data_structures.binary_tree BinaryTreeTraversalScene data_structures
python render_scene.py manim_assets.scenes.data_structures.graph GraphScene data_structures
python render_scene.py manim_assets.scenes.data_structures.graph GraphTraversalScene data_structures
python render_scene.py manim_assets.scenes.data_structures.sorting SortingScene data_structures
python render_scene.py manim_assets.scenes.data_structures.sorting QuickSortScene data_structures
python render_scene.py manim_assets.scenes.data_structures.sorting MergeSortScene data_structures

echo === Statistics / Probability ===
python render_scene.py manim_assets.scenes.statistics.normal_distribution NormalDistributionScene statistics
python render_scene.py manim_assets.scenes.statistics.histogram HistogramScene statistics
python render_scene.py manim_assets.scenes.statistics.scatter_regression ScatterRegressionScene statistics
python render_scene.py manim_assets.scenes.statistics.bayes_tree BayesTreeScene statistics
python render_scene.py manim_assets.scenes.statistics.central_limit CentralLimitTheoremScene statistics

echo === Machine Learning / AI ===
python render_scene.py manim_assets.scenes.ml.gradient_descent GradientDescentScene ml
python render_scene.py manim_assets.scenes.ml.neural_network NeuralNetworkScene ml
python render_scene.py manim_assets.scenes.ml.decision_boundary DecisionBoundaryScene ml
python render_scene.py manim_assets.scenes.ml.kmeans KMeansScene ml

echo === Advanced Math ===
python render_scene.py manim_assets.scenes.advanced_math.fourier_series FourierSeriesScene advanced_math
python render_scene.py manim_assets.scenes.advanced_math.unit_circle_sine UnitCircleSineScene advanced_math
python render_scene.py manim_assets.scenes.advanced_math.parametric_curves ParametricCurvesScene advanced_math

echo === CS Theory ===
python render_scene.py manim_assets.scenes.cs_theory.hash_table HashTableScene cs_theory
python render_scene.py manim_assets.scenes.cs_theory.stack_queue StackQueueScene cs_theory
python render_scene.py manim_assets.scenes.cs_theory.recursion_stack RecursionStackScene cs_theory

echo === DONE ===
pause
