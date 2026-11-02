"""
Scatter Plot with Regression Line Scene.
"""

from manim import Scene, Axes, Text, VGroup, Dot, Line, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class ScatterRegressionScene(Scene):
    """
    Scene: Show scatter plot of data points, then animate
    the least-squares regression line fitting through them.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(7)
        self.n_points: int = 30
        # Generate correlated data: y = 0.8x + 1.5 + noise
        self.x_data = np.linspace(0.5, 5.5, self.n_points)
        self.y_data = 0.8 * self.x_data + 1.5 + np.random.normal(0, 0.6, self.n_points)

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Scatter Plot with Regression Line", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 7, 1],
            x_length=9,
            y_length=5,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1.5,
                "include_numbers": True,
                "font_size": 22,
                "decimal_number_config": {"color": MUTED_COLOR, "num_decimal_places": 0},
            },
            tips=False,
        )
        axes.shift(DOWN * 0.2)

        x_label = Text("x", font_size=20, color=MUTED_COLOR)
        x_label.next_to(axes.x_axis, DOWN, buff=0.4)
        y_label = Text("y", font_size=20, color=MUTED_COLOR)
        y_label.next_to(axes.y_axis, LEFT, buff=0.4)

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.0)

        # Plot scatter points one by one
        dots = VGroup()
        for x_val, y_val in zip(self.x_data, self.y_data):
            dot = Dot(
                point=axes.c2p(x_val, y_val),
                radius=0.06,
                color=ACCENT_COLOR,
            )
            dots.add(dot)

        self.play(FadeIn(dots), run_time=1.5)

        # Compute least-squares regression
        x_mean = np.mean(self.x_data)
        y_mean = np.mean(self.y_data)
        ss_xy = np.sum((self.x_data - x_mean) * (self.y_data - y_mean))
        ss_xx = np.sum((self.x_data - x_mean) ** 2)
        slope = ss_xy / ss_xx
        intercept = y_mean - slope * x_mean

        # Draw regression line
        x_start, x_end = 0, 6
        y_start = slope * x_start + intercept
        y_end = slope * x_end + intercept

        reg_line = Line(
            start=axes.c2p(x_start, y_start),
            end=axes.c2p(x_end, y_end),
            color=TEXT_COLOR,
            stroke_width=2.5,
        )
        self.play(Create(reg_line), run_time=1.5)

        # Show equation and R^2
        y_pred = slope * self.x_data + intercept
        ss_res = np.sum((self.y_data - y_pred) ** 2)
        ss_tot = np.sum((self.y_data - y_mean) ** 2)
        r_squared = 1 - ss_res / ss_tot

        eq_text = Text(
            f"y = {slope:.2f}x + {intercept:.2f}",
            font_size=18, color=TEXT_COLOR,
        )
        eq_text.to_edge(DOWN, buff=1.0)

        r2_text = Text(
            f"R^2 = {r_squared:.3f}",
            font_size=18, color=ACCENT_COLOR,
        )
        r2_text.next_to(eq_text, RIGHT, buff=0.5)

        self.play(FadeIn(eq_text), FadeIn(r2_text), run_time=0.6)

        self.wait(2.0)
