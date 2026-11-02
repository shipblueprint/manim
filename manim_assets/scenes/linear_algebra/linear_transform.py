"""
Linear Transformations Scene - Visualize 2D linear transformations with grid deformation.
"""

from manim import (
    Scene, Text, VGroup, Line, Arrow, NumberPlane, RIGHT, UP, DOWN,
    Create, FadeIn, FadeOut, Transform,
)
from typing import List
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


def _make_grid_lines(x_range, y_range, step=1, color=MUTED_COLOR, width=0.5, opacity=0.3):
    """Create a VGroup of grid lines (vertical + horizontal)."""
    lines = VGroup()
    for x in np.arange(x_range[0], x_range[1] + step, step):
        line = Line(
            [x, y_range[0], 0], [x, y_range[1], 0],
            stroke_color=color, stroke_width=width, stroke_opacity=opacity,
        )
        lines.add(line)
    for y in np.arange(y_range[0], y_range[1] + step, step):
        line = Line(
            [x_range[0], y, 0], [x_range[1], y, 0],
            stroke_color=color, stroke_width=width, stroke_opacity=opacity,
        )
        lines.add(line)
    return lines


def _transform_grid_lines(grid, matrix):
    """Return a new VGroup of grid lines transformed by the matrix."""
    new_grid = VGroup()
    for line in grid:
        new_line = line.copy()
        start = np.array(line.get_start()[:2])
        end = np.array(line.get_end()[:2])
        new_start = matrix @ start
        new_end = matrix @ end
        new_line.put_start_and_end_on(
            [new_start[0], new_start[1], 0],
            [new_end[0], new_end[1], 0],
        )
        new_grid.add(new_line)
    return new_grid


class LinearTransformScene(Scene):
    """
    Scene: Show basis vectors and grid transforming under a matrix.
    Uses manual grid lines + Transform for reliable deformation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matrix: np.ndarray = np.array([[2, 1], [0.5, 1.5]])

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        m = self.matrix

        # Create original grid
        grid = _make_grid_lines([-4, 4], [-3, 3])

        # Axes (thicker)
        x_axis = Line([-5, 0, 0], [5, 0, 0], stroke_color=MUTED_COLOR, stroke_width=1.5)
        y_axis = Line([0, -3.5, 0], [0, 3.5, 0], stroke_color=MUTED_COLOR, stroke_width=1.5)

        # Basis vectors
        i_arrow = Arrow(
            start=[0, 0, 0], end=[1, 0, 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=4, tip_length=0.15,
        )
        j_arrow = Arrow(
            start=[0, 0, 0], end=[0, 1, 0],
            buff=0, stroke_color=TEXT_COLOR, stroke_width=4, tip_length=0.15,
        )

        i_label = Text("e1", font_size=22, color=ACCENT_COLOR)
        i_label.next_to([1.1, 0.15, 0], RIGHT, buff=0.1)
        j_label = Text("e2", font_size=22, color=TEXT_COLOR)
        j_label.next_to([0.15, 1.1, 0], UP, buff=0.1)

        # Matrix label
        mat_label = Text(
            f"A = [[{m[0,0]:.1f}, {m[0,1]:.1f}], [{m[1,0]:.1f}, {m[1,1]:.1f}]]",
            font_size=22,
            color=TEXT_COLOR,
        )
        mat_label.to_edge(UP, buff=0.6)

        # Phase 1: Show original grid and basis
        self.play(Create(grid), Create(x_axis), Create(y_axis), run_time=1.0)
        self.play(
            Create(i_arrow), Create(j_arrow),
            FadeIn(i_label), FadeIn(j_label),
            run_time=0.8,
        )
        self.wait(0.5)

        # Phase 2: Apply transformation
        new_i = m @ np.array([1, 0])
        new_j = m @ np.array([0, 1])

        # Create transformed grid
        new_grid = _transform_grid_lines(grid, m)

        # Create transformed arrows
        new_i_arrow = Arrow(
            start=[0, 0, 0], end=[new_i[0], new_i[1], 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=4, tip_length=0.15,
        )
        new_j_arrow = Arrow(
            start=[0, 0, 0], end=[new_j[0], new_j[1], 0],
            buff=0, stroke_color=TEXT_COLOR, stroke_width=4, tip_length=0.15,
        )

        new_i_label = Text(
            f"Ae1 = ({new_i[0]:.1f}, {new_i[1]:.1f})",
            font_size=16, color=ACCENT_COLOR,
        )
        new_i_label.next_to([new_i[0] * 1.1, new_i[1] * 1.1, 0], RIGHT, buff=0.1)

        new_j_label = Text(
            f"Ae2 = ({new_j[0]:.1f}, {new_j[1]:.1f})",
            font_size=16, color=TEXT_COLOR,
        )
        new_j_label.next_to([new_j[0] * 1.1, new_j[1] * 1.1, 0], UP, buff=0.1)

        # Fade out old labels
        self.play(
            FadeOut(i_label), FadeOut(j_label),
            FadeIn(mat_label),
            run_time=0.4,
        )

        # Transform grid and arrows
        self.play(
            Transform(grid, new_grid),
            Transform(i_arrow, new_i_arrow),
            Transform(j_arrow, new_j_arrow),
            run_time=2.0,
        )

        self.play(
            FadeIn(new_i_label), FadeIn(new_j_label),
            run_time=0.5,
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

    def set_matrix(self, matrix: List[List[float]]) -> None:
        self.matrix = np.array(matrix)


class RotationScene(LinearTransformScene):
    """Rotation transformation scene."""

    def __init__(self, angle: float = 45, **kwargs):
        super().__init__(**kwargs)
        import math
        theta = math.radians(angle)
        self.matrix = np.array([
            [math.cos(theta), -math.sin(theta)],
            [math.sin(theta), math.cos(theta)]
        ])


class ShearScene(LinearTransformScene):
    """Shear transformation scene."""

    def __init__(self, shear_x: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array([
            [1, shear_x],
            [0, 1]
        ])


class ScaleScene(LinearTransformScene):
    """Scale transformation scene."""

    def __init__(self, sx: float = 2.0, sy: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array([
            [sx, 0],
            [0, sy]
        ])
