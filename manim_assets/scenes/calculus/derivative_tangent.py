"""
Derivative and Tangent Line Scene - Visualize derivatives as slopes.
"""

from manim import Scene, Axes, Line, Text, VGroup, Dot, RIGHT, UP, DOWN, Create, FadeIn
from typing import Callable, Optional
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class DerivativeTangentScene(Scene):
    """
    Scene: Show a function with its tangent line at a point.
    Animates the tangent line appearing and shows the derivative value.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.axes_config = {
            "x_range": [-1, 5, 1],
            "y_range": [-2, 6, 1],
            "x_length": 10,
            "y_length": 7,
            "axis_config": {
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1.5,
                "include_numbers": True,
                "font_size": 24,
                "decimal_number_config": {"color": MUTED_COLOR, "num_decimal_places": 0},
            },
            "tips": False,
        }
        self.function: Optional[Callable] = lambda x: 0.3 * x**2
        self.point_x: float = 2.0

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Create axes centered on screen
        axes = Axes(**self.axes_config)
        axes.shift(DOWN * 0.5)

        self.play(Create(axes), run_time=1.0)

        if self.function:
            # Plot function using axes coordinate system (not FunctionGraph)
            graph = axes.plot(
                self.function,
                color=ACCENT_COLOR,
                x_range=self.axes_config["x_range"][:2],
                stroke_width=3,
            )
            self.play(Create(graph), run_time=2.0)

            # Calculate tangent line
            h = 0.0001
            f = self.function
            derivative_at_point = (f(self.point_x + h) - f(self.point_x)) / h
            f_at_point = f(self.point_x)

            # Point on curve
            point = axes.c2p(self.point_x, f_at_point)

            # Tangent line: y - f(a) = f'(a)(x - a)
            dx = 2.5
            tangent_start = axes.c2p(self.point_x - dx, f_at_point - derivative_at_point * dx)
            tangent_end = axes.c2p(self.point_x + dx, f_at_point + derivative_at_point * dx)

            tangent_line = Line(
                tangent_start, tangent_end,
                color=MUTED_COLOR,
                stroke_width=2.5,
            )

            # Point dot
            dot = Dot(point, color=TEXT_COLOR, radius=0.08)

            # Labels
            point_label = Text(
                f"({self.point_x}, {f_at_point:.1f})",
                font_size=18,
                color=TEXT_COLOR,
            )
            point_label.next_to(dot, UP, buff=0.2)

            slope_label = Text(
                f"f'({self.point_x}) = {derivative_at_point:.1f}",
                font_size=22,
                color=ACCENT_COLOR,
            )
            slope_label.to_edge(UP, buff=0.6)

            # Animate step by step
            self.wait(0.5)

            # Show the point on the curve
            self.play(Create(dot), run_time=0.4)
            self.play(FadeIn(point_label), run_time=0.3)
            self.wait(0.5)

            # Draw tangent line
            self.play(Create(tangent_line), run_time=1.0)
            self.wait(0.3)

            # Show derivative value
            self.play(FadeIn(slope_label), run_time=0.5)

            # Pulse the tangent line to emphasize
            self.play(
                tangent_line.animate.set_stroke(color=ACCENT_COLOR, width=4),
                run_time=0.3,
            )
            self.play(
                tangent_line.animate.set_stroke(color=MUTED_COLOR, width=2.5),
                run_time=0.3,
            )

            self.wait(2.0)

    def set_function(self, func: Callable, point_x: float = 2.0) -> None:
        self.function = func
        self.point_x = point_x
