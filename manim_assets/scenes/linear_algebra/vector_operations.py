"""
Vector Operations Scene - Visualize 2D and 3D vectors and operations.
"""

from manim import Scene, Text, Arrow, VGroup, Dot, UP, DOWN, LEFT, RIGHT, Create, FadeIn, Transform
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class Vector2DScene(Scene):
    """
    Scene: Show 2D vectors with components and magnitude.
    Animates vector construction from origin.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("2D Vectors", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Axes
        from manim import Line
        x_axis = Line([-5, 0, 0], [5, 0, 0], stroke_color=MUTED_COLOR, stroke_width=1)
        y_axis = Line([0, -3, 0], [0, 3, 0], stroke_color=MUTED_COLOR, stroke_width=1)
        self.play(Create(x_axis), Create(y_axis), run_time=0.5)

        # Vector v1
        v1 = np.array([3, 1])
        arrow1 = Arrow(
            start=[0, 0, 0], end=[v1[0], v1[1], 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=3, tip_length=0.15,
        )
        label1 = Text(f"v1 = ({v1[0]}, {v1[1]})", font_size=18, color=ACCENT_COLOR)
        label1.next_to([v1[0], v1[1], 0], RIGHT, buff=0.15)

        # Vector v2
        v2 = np.array([1, 2])
        arrow2 = Arrow(
            start=[0, 0, 0], end=[v2[0], v2[1], 0],
            buff=0, stroke_color=TEXT_COLOR, stroke_width=3, tip_length=0.15,
        )
        label2 = Text(f"v2 = ({v2[0]}, {v2[1]})", font_size=18, color=TEXT_COLOR)
        label2.next_to([v2[0], v2[1], 0], LEFT, buff=0.15)

        # Show component lines for v1
        comp_x = Line([0, 0, 0], [v1[0], 0, 0], stroke_color=MUTED_COLOR, stroke_width=1, stroke_opacity=0.5)
        comp_y = Line([v1[0], 0, 0], [v1[0], v1[1], 0], stroke_color=MUTED_COLOR, stroke_width=1, stroke_opacity=0.5)

        self.play(Create(arrow1), FadeIn(label1), run_time=0.8)
        self.play(Create(comp_x), Create(comp_y), run_time=0.4)

        # Magnitude
        mag = np.linalg.norm(v1)
        mag_label = Text(f"|v1| = {mag:.2f}", font_size=18, color=ACCENT_COLOR)
        mag_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(mag_label), run_time=0.4)

        # Show second vector
        self.play(Create(arrow2), FadeIn(label2), run_time=0.8)

        self.wait(2.0)


class Vector3DScene(Scene):
    """
    Scene: Show 3D vectors in a 3D coordinate system.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("3D Vectors", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Use ThreeDScene-like setup with simple projection
        # Draw 3D axes as projected lines
        from manim import Line
        origin = np.array([0, 0, 0])

        # Isometric-ish projection
        proj = lambda v: np.array([v[0] - v[2] * 0.5, v[1] + v[2] * 0.5, 0])

        # Axes
        x_end = proj(np.array([4, 0, 0]))
        y_end = proj(np.array([0, 4, 0]))
        z_end = proj(np.array([0, 0, 4]))

        x_axis = Line([0, 0, 0], x_end, stroke_color=MUTED_COLOR, stroke_width=1)
        y_axis = Line([0, 0, 0], y_end, stroke_color=MUTED_COLOR, stroke_width=1)
        z_axis = Line([0, 0, 0], z_end, stroke_color=MUTED_COLOR, stroke_width=1)

        x_label = Text("x", font_size=16, color=MUTED_COLOR)
        x_label.next_to(x_end, RIGHT, buff=0.1)
        y_label = Text("y", font_size=16, color=MUTED_COLOR)
        y_label.next_to(y_end, UP, buff=0.1)
        z_label = Text("z", font_size=16, color=MUTED_COLOR)
        z_label.next_to(z_end, LEFT, buff=0.1)

        self.play(Create(x_axis), Create(y_axis), Create(z_axis),
                  FadeIn(x_label), FadeIn(y_label), FadeIn(z_label), run_time=0.8)

        # 3D vectors
        v1 = np.array([2, 1, 1])
        v2 = np.array([1, 2, 2])

        v1_proj = proj(v1)
        v2_proj = proj(v2)

        arrow1 = Arrow(
            start=[0, 0, 0], end=v1_proj,
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=3, tip_length=0.15,
        )
        arrow2 = Arrow(
            start=[0, 0, 0], end=v2_proj,
            buff=0, stroke_color=TEXT_COLOR, stroke_width=3, tip_length=0.15,
        )

        label1 = Text(f"v1 = ({v1[0]},{v1[1]},{v1[2]})", font_size=16, color=ACCENT_COLOR)
        label1.next_to(v1_proj, RIGHT, buff=0.1)
        label2 = Text(f"v2 = ({v2[0]},{v2[1]},{v2[2]})", font_size=16, color=TEXT_COLOR)
        label2.next_to(v2_proj, LEFT, buff=0.1)

        self.play(Create(arrow1), FadeIn(label1), run_time=0.8)
        self.play(Create(arrow2), FadeIn(label2), run_time=0.8)

        # Dot product
        dot = np.dot(v1, v2)
        dot_label = Text(f"v1 . v2 = {dot}", font_size=20, color=ACCENT_COLOR)
        dot_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(dot_label), run_time=0.5)

        self.wait(2.0)


class VectorOperationsScene(Scene):
    """
    Scene: Show vector addition with parallelogram rule.
    Animates the parallelogram construction.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Vector Addition (Parallelogram Rule)", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Axes
        from manim import Line
        x_axis = Line([-5, 0, 0], [5, 0, 0], stroke_color=MUTED_COLOR, stroke_width=1)
        y_axis = Line([0, -3, 0], [0, 3, 0], stroke_color=MUTED_COLOR, stroke_width=1)
        self.play(Create(x_axis), Create(y_axis), run_time=0.5)

        # Two vectors
        v1 = np.array([3, 0.5])
        v2 = np.array([1, 2])
        v_sum = v1 + v2

        # Draw v1
        arrow1 = Arrow(
            start=[0, 0, 0], end=[v1[0], v1[1], 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=3, tip_length=0.15,
        )
        label1 = Text("v1", font_size=18, color=ACCENT_COLOR)
        label1.next_to([v1[0] / 2, v1[1] / 2, 0], DOWN, buff=0.15)

        self.play(Create(arrow1), FadeIn(label1), run_time=0.8)

        # Draw v2
        arrow2 = Arrow(
            start=[0, 0, 0], end=[v2[0], v2[1], 0],
            buff=0, stroke_color=TEXT_COLOR, stroke_width=3, tip_length=0.15,
        )
        label2 = Text("v2", font_size=18, color=TEXT_COLOR)
        label2.next_to([v2[0] / 2, v2[1] / 2, 0], LEFT, buff=0.15)

        self.play(Create(arrow2), FadeIn(label2), run_time=0.8)

        # Parallelogram: v2 translated to tip of v1, v1 translated to tip of v2
        arrow_v2_shifted = Arrow(
            start=[v1[0], v1[1], 0], end=[v_sum[0], v_sum[1], 0],
            buff=0, stroke_color=TEXT_COLOR, stroke_width=2, stroke_opacity=0.5, tip_length=0.12,
        )
        arrow_v1_shifted = Arrow(
            start=[v2[0], v2[1], 0], end=[v_sum[0], v_sum[1], 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=2, stroke_opacity=0.5, tip_length=0.12,
        )

        self.play(Create(arrow_v2_shifted), Create(arrow_v1_shifted), run_time=0.8)

        # Result vector
        arrow_sum = Arrow(
            start=[0, 0, 0], end=[v_sum[0], v_sum[1], 0],
            buff=0, stroke_color=ACCENT_COLOR, stroke_width=4, tip_length=0.18,
        )
        sum_label = Text(
            f"v1 + v2 = ({v_sum[0]}, {v_sum[1]})",
            font_size=18,
            color=ACCENT_COLOR,
        )
        sum_label.to_edge(DOWN, buff=0.6)

        self.play(Create(arrow_sum), FadeIn(sum_label), run_time=0.8)

        self.wait(2.0)
