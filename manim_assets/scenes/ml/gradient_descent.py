"""
Gradient Descent Scene - Ball rolling down a 3D loss surface.
"""

from manim import Scene, Axes, Text, VGroup, Dot, Line, UP, DOWN, LEFT, Create, FadeIn
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class GradientDescentScene(Scene):
    """
    Scene: Visualize gradient descent on a 2D loss surface.
    Shows contour plot with a ball following the gradient path.
    Loss function: L(w1, w2) = w1^2 + 2*w2^2
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lr: float = 0.15
        self.start_point: list = [2.5, 2.0]
        self.n_steps: int = 12

    def _loss(self, w1: float, w2: float) -> float:
        """Loss function: L = w1^2 + 2*w2^2."""
        return w1 ** 2 + 2 * w2 ** 2

    def _grad(self, w1: float, w2: float) -> tuple:
        """Gradient of loss function."""
        return (2 * w1, 4 * w2)

    def _descent_path(self) -> list:
        """Compute gradient descent path."""
        path = [self.start_point[:]]
        w1, w2 = self.start_point
        for _ in range(self.n_steps):
            g1, g2 = self._grad(w1, w2)
            w1 = w1 - self.lr * g1
            w2 = w2 - self.lr * g2
            path.append([w1, w2])
        return path

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Gradient Descent", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Create axes for contour plot
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=8,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1.5,
                "include_numbers": True,
                "font_size": 18,
                "decimal_number_config": {"color": MUTED_COLOR, "num_decimal_places": 0},
            },
            tips=False,
        )
        axes.shift(DOWN * 0.2)

        w1_label = Text("w1", font_size=16, color=MUTED_COLOR)
        w1_label.next_to(axes.x_axis, DOWN, buff=0.2)
        w2_label = Text("w2", font_size=16, color=MUTED_COLOR)
        w2_label.next_to(axes.y_axis, LEFT, buff=0.2)

        self.play(Create(axes), FadeIn(w1_label), FadeIn(w2_label), run_time=1.0)

        # Draw contour lines
        contour_levels = [0.5, 1, 2, 4, 8, 14]
        for level in contour_levels:
            # w1^2 + 2*w2^2 = level => ellipse
            # w1 = sqrt(level) * cos(t), w2 = sqrt(level/2) * sin(t)
            t_vals = np.linspace(0, 2 * np.pi, 100)
            points = []
            for t in t_vals:
                w1 = np.sqrt(level) * np.cos(t)
                w2 = np.sqrt(level / 2) * np.sin(t)
                if -3 <= w1 <= 3 and -3 <= w2 <= 3:
                    points.append(axes.c2p(w1, w2))

            if len(points) > 2:
                contour_line = Line(
                    start=points[0],
                    end=points[-1],
                    stroke_color=MUTED_COLOR,
                    stroke_width=0.8,
                    stroke_opacity=0.4,
                )
                # Use a proper path through all points
                from manim import VMobject
                contour = VMobject(
                    stroke_color=MUTED_COLOR,
                    stroke_width=0.8,
                    stroke_opacity=0.4,
                    fill_opacity=0,
                )
                contour.set_points_as_corners(points + [points[0]])
                self.add(contour)

        self.wait(0.3)

        # Compute and animate gradient descent path
        path = self._descent_path()

        # Draw path line segments and ball
        ball = Dot(
            point=axes.c2p(path[0][0], path[0][1]),
            radius=0.12,
            color=ACCENT_COLOR,
        )
        self.play(FadeIn(ball), run_time=0.3)

        for i in range(1, len(path)):
            start_pt = axes.c2p(path[i - 1][0], path[i - 1][1])
            end_pt = axes.c2p(path[i][0], path[i][1])

            step_line = Line(
                start=start_pt, end=end_pt,
                stroke_color=ACCENT_COLOR,
                stroke_width=2,
            )
            self.play(
                Create(step_line),
                ball.animate.move_to(end_pt),
                run_time=0.3,
            )

        # Show final result
        final_w1, final_w2 = path[-1]
        final_loss = self._loss(final_w1, final_w2)

        result_text = Text(
            f"Final: w1={final_w1:.3f}, w2={final_w2:.3f}, L={final_loss:.4f}",
            font_size=16, color=TEXT_COLOR,
        )
        result_text.to_edge(DOWN, buff=0.5)

        lr_text = Text(
            f"Learning rate = {self.lr}",
            font_size=14, color=MUTED_COLOR,
        )
        lr_text.next_to(result_text, UP, buff=0.15)

        self.play(FadeIn(lr_text), FadeIn(result_text), run_time=0.5)

        self.wait(2.0)
