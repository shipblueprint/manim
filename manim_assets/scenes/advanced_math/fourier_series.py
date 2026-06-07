"""
Fourier Series Scene - Square wave approximation building up harmonics.
"""

from manim import Scene, Axes, Text, VGroup, UP, DOWN, Create, FadeIn, FadeOut
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class FourierSeriesScene(Scene):
    """
    Scene: Build up a square wave by adding Fourier harmonics.
    Square wave = (4/pi) * sum_{k=1,3,5,...} (1/k) * sin(k*x)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_harmonics: int = 7  # Number of odd harmonics to add
        self.x_range: tuple = (-2 * np.pi, 2 * np.pi)

    def _square_wave_approx(self, x: float, n_harmonics: int) -> float:
        """Compute Fourier approximation of square wave with n_harmonics odd terms."""
        result = 0.0
        for k in range(n_harmonics):
            n = 2 * k + 1  # Odd harmonics: 1, 3, 5, 7, ...
            result += (1.0 / n) * np.sin(n * x)
        return (4.0 / np.pi) * result

    def _ideal_square(self, x: float) -> float:
        """Ideal square wave for reference."""
        return 1.0 if (x % (2 * np.pi)) < np.pi else -1.0

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Standalone functions (avoid self reference in closures for deepcopy)
        def ideal_square(x: float) -> float:
            return 1.0 if (x % (2 * np.pi)) < np.pi else -1.0

        def square_wave_approx(x: float, n_harmonics: int) -> float:
            result = 0.0
            for k in range(n_harmonics):
                n = 2 * k + 1
                result += (1.0 / n) * np.sin(n * x)
            return (4.0 / np.pi) * result

        title = Text("Fourier Series — Square Wave", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Create axes
        axes = Axes(
            x_range=[-2 * np.pi, 2 * np.pi, np.pi],
            y_range=[-1.8, 1.8, 0.5],
            x_length=11,
            y_length=4.5,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1.5,
                "include_numbers": False,
                "font_size": 18,
            },
            tips=False,
        )
        axes.shift(DOWN * 0.3)

        # Custom tick labels for pi
        pi_labels = VGroup()
        for val, label_text in [(-2 * np.pi, "-2pi"), (-np.pi, "-pi"), (0, "0"), (np.pi, "pi"), (2 * np.pi, "2pi")]:
            pos = axes.c2p(val, 0)
            lbl = Text(label_text, font_size=14, color=MUTED_COLOR)
            lbl.next_to(pos, DOWN, buff=0.15)
            pi_labels.add(lbl)

        self.play(Create(axes), FadeIn(pi_labels), run_time=1.0)

        # Draw ideal square wave (reference)
        square_wave = axes.plot(
            ideal_square,
            color=MUTED_COLOR,
            x_range=self.x_range,
            stroke_width=1.5,
            stroke_opacity=0.3,
        )
        self.play(Create(square_wave), run_time=0.8)

        # Build up harmonics one by one
        current_curve = None
        footer_label = None
        for n in range(1, self.max_harmonics + 1):
            # Plot approximation with n harmonics
            approx_curve = axes.plot(
                lambda x, nn=n: square_wave_approx(x, nn),
                color=ACCENT_COLOR,
                x_range=self.x_range,
                stroke_width=2.5,
            )

            # Harmonic label — replace previous one
            harmonics_str = ", ".join([str(2 * k + 1) for k in range(n)])
            n_label = Text(
                f"Harmonics: {harmonics_str}",
                font_size=14, color=TEXT_COLOR,
            )
            n_label.to_edge(DOWN, buff=0.5)

            if footer_label is not None:
                self.remove(footer_label)

            if current_curve is not None:
                self.play(
                    current_curve.animate.become(approx_curve),
                    FadeIn(n_label),
                    run_time=1.0,
                )
            else:
                self.play(Create(approx_curve), FadeIn(n_label), run_time=1.0)

            current_curve = approx_curve
            footer_label = n_label
            self.wait(0.3)

        # Final formula — replace harmonic label
        formula = Text(
            "f(x) = (4/pi) * [sin(x) + sin(3x)/3 + sin(5x)/5 + ...]",
            font_size=16, color=ACCENT_COLOR,
        )
        formula.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(footer_label), FadeIn(formula), run_time=0.5)

        self.wait(2.0)
