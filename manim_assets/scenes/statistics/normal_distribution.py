"""
Normal Distribution Scene - Bell curve with shaded tails.
"""

from manim import Scene, Axes, Text, VGroup, Polygon, UP, DOWN, Create, FadeIn
import numpy as np
from math import erf, sqrt

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class NormalDistributionScene(Scene):
    """
    Scene: Show a normal distribution curve with shaded tails.
    Animates the curve drawing, then shades the tail areas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mu: float = 0.0
        self.sigma: float = 1.0
        self.tail_z: float = 1.96  # 95% confidence interval

    def _pdf(self, x: float) -> float:
        """Normal distribution PDF."""
        coeff = 1.0 / (self.sigma * np.sqrt(2 * np.pi))
        exponent = -0.5 * ((x - self.mu) / self.sigma) ** 2
        return coeff * np.exp(exponent)

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Capture params locally to avoid self reference in closures
        mu = self.mu
        sigma = self.sigma

        def pdf(x: float) -> float:
            """Normal distribution PDF (standalone closure)."""
            coeff = 1.0 / (sigma * np.sqrt(2 * np.pi))
            exponent = -0.5 * ((x - mu) / sigma) ** 2
            return coeff * np.exp(exponent)

        title = Text("Normal Distribution", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)

        mu_label = Text(
            f"mu = {self.mu}, sigma = {self.sigma}",
            font_size=18, color=MUTED_COLOR,
        )
        mu_label.next_to(title, DOWN, buff=0.2)

        self.play(FadeIn(title), FadeIn(mu_label), run_time=0.5)

        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=5,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1.5,
                "include_numbers": True,
                "font_size": 20,
                "decimal_number_config": {"color": MUTED_COLOR, "num_decimal_places": 1},
            },
            tips=False,
        )
        axes.shift(DOWN * 0.3)

        self.play(Create(axes), run_time=1.0)

        # Draw the bell curve
        curve = axes.plot(pdf, color=ACCENT_COLOR, x_range=[-4, 4], stroke_width=3)
        self.play(Create(curve), run_time=2.0)

        # Shade the tails (beyond ±tail_z)
        z = self.tail_z

        # Left tail polygon
        left_xs = np.linspace(-4, -z, 80)
        left_points = [axes.c2p(x, pdf(x)) for x in left_xs]
        left_base = [axes.c2p(x, 0) for x in reversed(left_xs)]
        left_poly = Polygon(
            *(left_points + left_base),
            stroke_width=0,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.35,
        )

        # Right tail polygon
        right_xs = np.linspace(z, 4, 80)
        right_points = [axes.c2p(x, pdf(x)) for x in right_xs]
        right_base = [axes.c2p(x, 0) for x in reversed(right_xs)]
        right_poly = Polygon(
            *(right_points + right_base),
            stroke_width=0,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.35,
        )

        self.play(Create(left_poly), Create(right_poly), run_time=1.0)

        # Shade the center (95% area)
        center_xs = np.linspace(-z, z, 120)
        center_points = [axes.c2p(x, pdf(x)) for x in center_xs]
        center_base = [axes.c2p(x, 0) for x in reversed(center_xs)]
        center_poly = Polygon(
            *(center_points + center_base),
            stroke_width=0,
            fill_color=TEXT_COLOR,
            fill_opacity=0.08,
        )
        self.play(Create(center_poly), run_time=0.8)

        # Labels for tail areas
        tail_prob = 2 * (1 - self._cdf_approx(z))
        center_prob = 1 - tail_prob

        left_label = Text(f"{tail_prob/2:.3f}", font_size=16, color=ACCENT_COLOR)
        left_label.next_to(axes.c2p(-z - 0.6, pdf(-z - 0.6)), UP, buff=0.15)

        right_label = Text(f"{tail_prob/2:.3f}", font_size=16, color=ACCENT_COLOR)
        right_label.next_to(axes.c2p(z + 0.6, pdf(z + 0.6)), UP, buff=0.15)

        center_label = Text(f"{center_prob:.3f}", font_size=20, color=TEXT_COLOR)
        center_label.move_to(axes.c2p(0, 0.2))

        self.play(FadeIn(left_label), FadeIn(right_label), FadeIn(center_label), run_time=0.6)

        # Z-score label
        z_label = Text(f"z = +/-{z:.2f}  (95% CI)", font_size=18, color=ACCENT_COLOR)
        z_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(z_label), run_time=0.5)

        self.wait(2.0)

    def _cdf_approx(self, x: float) -> float:
        """Approximate CDF using error function."""
        return 0.5 * (1 + erf(x / sqrt(2)))
