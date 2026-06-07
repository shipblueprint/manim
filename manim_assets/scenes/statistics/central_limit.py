"""
Central Limit Theorem Scene - Distributions converging to normal.
"""

from manim import Scene, Axes, Text, VGroup, Polygon, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class CentralLimitTheoremScene(Scene):
    """
    Scene: Show how sample means from a uniform distribution
    converge to a normal distribution as sample size increases.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(42)
        self.n_samples: int = 5000
        self.sample_sizes: list = [1, 2, 5, 30]
        self.n_bins: int = 30

    def _sample_means(self, sample_size: int) -> np.ndarray:
        """Generate sample means from uniform [0, 1] distribution."""
        means = []
        for _ in range(self.n_samples):
            sample = np.random.uniform(0, 1, sample_size)
            means.append(np.mean(sample))
        return np.array(means)

    def _make_histogram_poly(
        self, axes: Axes, data: np.ndarray, x_range: tuple, color: object
    ) -> VGroup:
        """Create histogram polygons from data using axes coordinates."""
        counts, edges = np.histogram(data, bins=self.n_bins, range=x_range)
        max_count = max(counts) if max(counts) > 0 else 1
        # Normalize to density-like scale for display
        y_scale = 4.0 / max_count

        polys = VGroup()
        for i in range(len(counts)):
            if counts[i] == 0:
                continue
            x0, x1 = edges[i], edges[i + 1]
            h = counts[i] * y_scale
            p1 = axes.c2p(x0, 0)
            p2 = axes.c2p(x1, 0)
            p3 = axes.c2p(x1, h)
            p4 = axes.c2p(x0, h)
            poly = Polygon(
                p1, p4, p3, p2,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.35,
            )
            polys.add(poly)
        return polys

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Central Limit Theorem", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        subtitle = Text(
            "Sample means from Uniform[0,1] converge to Normal",
            font_size=16, color=MUTED_COLOR,
        )
        subtitle.next_to(title, DOWN, buff=0.15)
        self.play(FadeIn(subtitle), run_time=0.3)

        # Layout: 2x2 grid of mini histograms
        positions = [UP * 1.2 + LEFT * 3.2, UP * 1.2 + RIGHT * 3.2,
                     DOWN * 1.5 + LEFT * 3.2, DOWN * 1.5 + RIGHT * 3.2]

        for idx, n in enumerate(self.sample_sizes):
            means = self._sample_means(n)
            x_range = (0, 1)

            axes = Axes(
                x_range=[0, 1, 0.5],
                y_range=[0, 5, 1],
                x_length=4.5,
                y_length=2.8,
                axis_config={
                    "stroke_color": MUTED_COLOR,
                    "stroke_width": 1,
                    "include_numbers": False,
                    "font_size": 14,
                },
                tips=False,
            )
            axes.move_to(positions[idx])

            n_label = Text(f"n = {n}", font_size=16, color=ACCENT_COLOR)
            n_label.next_to(axes, UP, buff=0.1)

            hist = self._make_histogram_poly(axes, means, x_range, ACCENT_COLOR)

            # Overlay theoretical normal curve for n > 1
            overlay_curve = None
            if n > 1:
                mu = 0.5  # Mean of Uniform[0,1]
                sigma_pop = 1.0 / np.sqrt(12)  # Std of Uniform[0,1]
                sigma_mean = sigma_pop / np.sqrt(n)

                def normal_pdf(x, mu=mu, sig=sigma_mean):
                    coeff = 1.0 / (sig * np.sqrt(2 * np.pi))
                    return coeff * np.exp(-0.5 * ((x - mu) / sig) ** 2)

                # Scale the PDF to match histogram height
                counts, _ = np.histogram(means, bins=self.n_bins, range=x_range)
                max_count = max(counts) if max(counts) > 0 else 1
                y_scale = 4.0 / max_count
                bin_width = 1.0 / self.n_bins
                # Capture n_samples locally to avoid self reference in closure
                n_samples = self.n_samples

                def scaled_pdf(x, _normal=normal_pdf, _ys=y_scale, _ns=n_samples, _bw=bin_width):
                    return _normal(x) * _ys * _ns * _bw

                overlay_curve = axes.plot(
                    scaled_pdf, color=TEXT_COLOR, x_range=[0, 1], stroke_width=2
                )

            anims = [Create(axes), FadeIn(n_label), Create(hist)]
            if overlay_curve:
                anims.append(Create(overlay_curve))

            self.play(*anims, run_time=1.2)

        # Final formula
        formula = Text(
            "X_bar ~ N(mu, sigma^2/n) as n -> inf",
            font_size=18, color=TEXT_COLOR,
        )
        formula.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(formula), run_time=0.5)

        self.wait(2.0)
