"""
Matrix Operations Scene - Visualize matrix multiplication and transformations.
"""

from manim import Scene, Text, VGroup, Rectangle, Square, Arrow, Polygon, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, Transform
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class MatrixOpsScene(Scene):
    """
    Scene: Show matrix multiplication transforming a unit square.
    Visualizes how a 2x2 matrix stretches/rotates/shears a shape.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array([[2, 1], [0.5, 1.5]])

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        m = self.matrix

        # Title
        title = Text("Matrix Transformation", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)

        # Matrix display - positioned top-left
        mat_label = Text(
            f"A = [[{m[0,0]:.1f}, {m[0,1]:.1f}], [{m[1,0]:.1f}, {m[1,1]:.1f}]]",
            font_size=20,
            color=MUTED_COLOR,
        )
        mat_label.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(title), FadeIn(mat_label), run_time=0.5)

        # Unit square
        square = Square(
            side_length=1,
            stroke_color=TEXT_COLOR,
            stroke_width=2,
            fill_color=TEXT_COLOR,
            fill_opacity=0.1,
        )
        square.shift(LEFT * 2)

        # Label the square
        sq_label = Text("Unit Square", font_size=16, color=TEXT_COLOR)
        sq_label.next_to(square, DOWN, buff=0.3)

        self.play(Create(square), FadeIn(sq_label), run_time=0.8)
        self.wait(0.3)

        # Compute transformed vertices
        corners = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        transformed = np.array([m @ c for c in corners])

        # Create transformed polygon
        from manim import Polygon
        transformed_shape = Polygon(
            *[np.append(t, 0) for t in transformed],
            stroke_color=ACCENT_COLOR,
            stroke_width=2,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.15,
        )
        transformed_shape.shift(LEFT * 2)

        # Arrow between shapes
        arrow = Arrow(
            start=RIGHT * 0.5,
            end=RIGHT * 1.5,
            stroke_color=MUTED_COLOR,
            stroke_width=2,
        )
        arrow.next_to(square, RIGHT, buff=0.3)

        # Transform label
        transform_label = Text("x A", font_size=18, color=ACCENT_COLOR)
        transform_label.next_to(arrow, UP, buff=0.15)

        self.play(Create(arrow), FadeIn(transform_label), run_time=0.5)

        # Animate the transformation
        self.play(
            Transform(square, transformed_shape),
            run_time=1.5,
        )

        # Update label
        new_label = Text("Transformed", font_size=16, color=ACCENT_COLOR)
        new_label.next_to(square, DOWN, buff=0.3)
        self.play(
            FadeOut(sq_label),
            FadeIn(new_label),
            run_time=0.3,
        )

        # Show determinant
        det = np.linalg.det(m)
        det_label = Text(
            f"det(A) = {det:.2f}",
            font_size=20,
            color=ACCENT_COLOR,
        )
        det_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(det_label), run_time=0.5)

        self.wait(2.0)


class MatrixTransformScene(MatrixOpsScene):
    """Matrix transform scene with a different default matrix."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array([[1.5, -0.5], [0.5, 1]])
