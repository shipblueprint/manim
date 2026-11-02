"""
Function Graph Scene - Plot functions on coordinate axes with animated drawing.
"""

from manim import (
    Scene, Axes, Text, VGroup, Dot, Line,
    RIGHT, LEFT, UP, DOWN, UR, Create, FadeIn, FadeOut, TracedPath, linear,
)
from typing import Callable, Optional
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class FunctionGraphScene(Scene):
    """
    Scene: Animate a function being plotted on coordinate axes.
    Shows axes drawing, then the curve traces itself with a moving dot.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.axes_config = {
            "x_range": [-4, 4, 1],
            "y_range": [-4, 5, 1],
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
        self.function: Optional[Callable] = lambda x: 0.5 * x**2 - 2
        self.graph_color = ACCENT_COLOR

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Create axes
        axes = Axes(**self.axes_config)

        # Axis labels
        x_label = Text("x", font_size=24, color=TEXT_COLOR)
        x_label.next_to(axes.x_axis.get_right(), DOWN, buff=0.3)
        y_label = Text("y", font_size=24, color=TEXT_COLOR)
        y_label.next_to(axes.y_axis.get_top(), LEFT, buff=0.3)

        # Animate axes appearing
        self.play(Create(axes), run_time=1.2)
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.4)
        self.wait(0.3)

        if self.function:
            # Create the graph using axes coordinate system
            graph = axes.plot(
                self.function,
                color=self.graph_color,
                x_range=self.axes_config["x_range"][:2],
                stroke_width=3,
            )

            # Trace the curve progressively with a moving dot
            tracer = Dot(axes.c2p(-4, self.function(-4)), color=TEXT_COLOR, radius=0.08)

            self.play(FadeIn(tracer), run_time=0.3)
            self.play(
                Create(graph),
                tracer.animate.move_to(axes.c2p(4, self.function(4))),
                run_time=2.5,
                rate_func=linear,
            )
            self.play(FadeOut(tracer), run_time=0.2)
            self.wait(0.5)

            # Show key points - vertex for parabola
            x_min = 0
            y_min = self.function(x_min)
            vertex = Dot(
                axes.c2p(x_min, y_min),
                color=TEXT_COLOR,
                radius=0.06,
            )
            vertex_label = Text(
                f"({x_min}, {y_min:.1f})",
                font_size=18,
                color=TEXT_COLOR,
            )
            vertex_label.next_to(vertex, DOWN, buff=0.3)

            self.play(FadeIn(vertex), FadeIn(vertex_label), run_time=0.5)

            # Show function expression
            func_label = Text("f(x) = 0.5x^2 - 2", font_size=22, color=ACCENT_COLOR)
            func_label.to_edge(UP, buff=0.6)
            self.play(FadeIn(func_label), run_time=0.4)

            # Animate a tangent line at x=2
            h = 0.0001
            f = self.function
            deriv = (f(2 + h) - f(2)) / h
            f_at_2 = f(2)
            dx = 1.5
            tangent_start = axes.c2p(2 - dx, f_at_2 - deriv * dx)
            tangent_end = axes.c2p(2 + dx, f_at_2 + deriv * dx)
            tangent = Line(tangent_start, tangent_end, stroke_color=MUTED_COLOR, stroke_width=2)

            point_dot = Dot(axes.c2p(2, f_at_2), color=TEXT_COLOR, radius=0.06)
            slope_label = Text(
                f"f'(2) = {deriv:.1f}",
                font_size=18,
                color=ACCENT_COLOR,
            )
            slope_label.next_to(point_dot, UR, buff=0.2)

            self.play(
                Create(tangent),
                FadeIn(point_dot),
                FadeIn(slope_label),
                run_time=0.8,
            )

            self.wait(2.0)
