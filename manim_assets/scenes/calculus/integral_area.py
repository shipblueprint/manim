"""
Integral Area Scene - Visualize definite integrals as area under curve.
"""

from manim import Scene, Axes, Text, VGroup, Rectangle, UP, DOWN, Create, FadeIn, FadeOut
from typing import Callable, Optional
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class IntegralAreaScene(Scene):
    """
    Scene: Show area under a curve = definite integral.
    Animates Riemann sums converging to the integral value.
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
        self.x_min: float = 0.5
        self.x_max: float = 3.0

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Center axes on screen
        axes = Axes(**self.axes_config)
        axes.shift(DOWN * 0.5)

        self.play(Create(axes), run_time=1.0)

        if self.function:
            # Plot function using axes coordinate system (not FunctionGraph)
            graph = axes.plot(
                self.function,
                color=ACCENT_COLOR,
                x_range=[-1, 5],
                stroke_width=3,
            )
            self.play(Create(graph), run_time=1.5)

            # Integral notation
            integral_expr = Text(
                f"Integral from {self.x_min} to {self.x_max}",
                font_size=22,
                color=TEXT_COLOR,
            )
            integral_expr.to_edge(UP, buff=0.6)

            # Show increasing numbers of Riemann rectangles
            prev_riemann = None
            for n in [4, 10, 25]:
                if prev_riemann is not None:
                    self.play(FadeOut(prev_riemann), run_time=0.3)

                dx = (self.x_max - self.x_min) / n
                riemann = VGroup()
                for i in range(n):
                    x = self.x_min + i * dx
                    height = self.function(x + dx / 2)
                    # Use axes coordinates
                    p1 = axes.c2p(x, 0)
                    p2 = axes.c2p(x + dx, height)
                    rect = Rectangle(
                        width=p2[0] - p1[0],
                        height=p2[1] - p1[1],
                        stroke_color=MUTED_COLOR,
                        stroke_width=0.8,
                        fill_color=ACCENT_COLOR,
                        fill_opacity=0.15,
                    )
                    rect.move_to(axes.c2p(x + dx / 2, height / 2))
                    riemann.add(rect)

                n_label = Text(f"n = {n}", font_size=18, color=TEXT_COLOR)
                n_label.to_edge(UP, buff=1.5)

                self.play(Create(riemann), FadeIn(n_label), run_time=0.8)
                self.wait(0.5)

                if prev_riemann is not None:
                    self.play(FadeOut(n_label), run_time=0.2)
                prev_riemann = riemann

            # Final clean view with integral label
            self.play(FadeIn(integral_expr), run_time=0.5)

            # Calculate approximate integral
            try:
                from scipy import integrate as sci_integrate
                result, _ = sci_integrate.quad(self.function, self.x_min, self.x_max)
            except ImportError:
                # Fallback: simple numerical integration
                xs = np.linspace(self.x_min, self.x_max, 1000)
                result = np.trapz([self.function(x) for x in xs], xs)

            result_label = Text(
                f"Area = {result:.2f}",
                font_size=24,
                color=ACCENT_COLOR,
            )
            result_label.next_to(integral_expr, DOWN, buff=0.3)
            self.play(FadeIn(result_label), run_time=0.5)
            self.wait(2)

    def set_function(self, func: Callable, x_min: float = 0.5, x_max: float = 3.0) -> None:
        self.function = func
        self.x_min = x_min
        self.x_max = x_max
