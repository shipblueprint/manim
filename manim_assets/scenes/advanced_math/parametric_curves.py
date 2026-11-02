"""
Parametric Curves Scene - Lissajous and Spirograph.
"""

from manim import Scene, Axes, Text, VGroup, UP, DOWN, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class ParametricCurvesScene(Scene):
    """
    Scene: Animate Lissajous curves and a spirograph pattern.
    Lissajous: x = A*sin(a*t + delta), y = B*sin(b*t)
    Spirograph: x = (R-r)*cos(t) + d*cos((R-r)/r * t),
                y = (R-r)*sin(t) - d*sin((R-r)/r * t)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Lissajous parameters
        self.liss_a: int = 3
        self.liss_b: int = 4
        self.liss_delta: float = np.pi / 2
        self.liss_scale: float = 2.0

        # Spirograph parameters
        self.spir_R: float = 3.0
        self.spir_r: float = 1.0
        self.spir_d: float = 1.5
        self.spir_scale: float = 0.6

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Parametric Curves", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        # --- Lissajous curve (left side) ---
        liss_center = [-3.2, -0.3, 0]

        liss_label = Text(
            f"Lissajous  a={self.liss_a}, b={self.liss_b}",
            font_size=16, color=ACCENT_COLOR,
        )
        liss_label.move_to([liss_center[0], liss_center[1] + 2.8, 0])
        self.add(liss_label)

        # Generate Lissajous points
        t_vals = np.linspace(0, 2 * np.pi, 500)
        liss_points = []
        for t in t_vals:
            x = self.liss_scale * np.sin(self.liss_a * t + self.liss_delta)
            y = self.liss_scale * np.sin(self.liss_b * t)
            liss_points.append([liss_center[0] + x, liss_center[1] + y, 0])

        # Animate drawing
        from manim import VMobject
        liss_curve = VMobject(stroke_color=ACCENT_COLOR, stroke_width=2.5)
        liss_curve.set_points_as_corners(liss_points)

        # Draw progressively
        step = 10
        for i in range(step, len(liss_points) + 1, step):
            partial = VMobject(stroke_color=ACCENT_COLOR, stroke_width=2.5)
            partial.set_points_as_corners(liss_points[:i])
            self.add(partial)
            self.wait(0.01)

        self.wait(0.5)

        # --- Spirograph (right side) ---
        spir_center = [3.2, -0.3, 0]

        spir_label = Text(
            f"Spirograph  R={self.spir_R}, r={self.spir_r}, d={self.spir_d}",
            font_size=16, color=TEXT_COLOR,
        )
        spir_label.move_to([spir_center[0], spir_center[1] + 2.8, 0])
        self.add(spir_label)

        # Generate spirograph points
        # Number of rotations for the pattern to close
        from math import gcd
        g = gcd(int(self.spir_R), int(self.spir_r))
        n_rotations = int(self.spir_r) // g
        t_spir = np.linspace(0, 2 * np.pi * n_rotations, 2000)

        spir_points = []
        for t in t_spir:
            R, r, d = self.spir_R, self.spir_r, self.spir_d
            x = (R - r) * np.cos(t) + d * np.cos((R - r) / r * t)
            y = (R - r) * np.sin(t) - d * np.sin((R - r) / r * t)
            spir_points.append([
                spir_center[0] + x * self.spir_scale,
                spir_center[1] + y * self.spir_scale,
                0,
            ])

        # Animate drawing
        spir_curve = VMobject(stroke_color=TEXT_COLOR, stroke_width=1.5)
        step = 20
        for i in range(step, len(spir_points) + 1, step):
            partial = VMobject(stroke_color=TEXT_COLOR, stroke_width=1.5)
            partial.set_points_as_corners(spir_points[:i])
            self.add(partial)
            self.wait(0.005)

        # Show parametric equations
        eq_liss = Text(
            "x = sin(3t + pi/2),  y = sin(4t)",
            font_size=14, color=ACCENT_COLOR,
        )
        eq_liss.to_edge(DOWN, buff=0.8)

        eq_spir = Text(
            "x = (R-r)cos(t) + d*cos((R-r)t/r)",
            font_size=14, color=TEXT_COLOR,
        )
        eq_spir.next_to(eq_liss, UP, buff=0.15)

        self.play(FadeIn(eq_liss), FadeIn(eq_spir), run_time=0.5)

        self.wait(2.0)
