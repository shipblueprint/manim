"""
Histogram Scene - Bins animating from data points.
"""

from manim import Scene, NumberLine, Text, VGroup, Rectangle, Dot, UP, DOWN, Create, FadeIn, FadeOut
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class HistogramScene(Scene):
    """
    Scene: Show data points on a number line, then animate them
    rising into histogram bins.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(42)
        self.data: list = list(np.random.normal(loc=5.0, scale=1.5, size=60))
        self.num_bins: int = 10
        self.bin_width: float = 0.8
        self.bar_gap: float = 0.05

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Histogram from Data Points", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Compute bins
        data_min = min(self.data)
        data_max = max(self.data)
        bin_edges = np.linspace(data_min, data_max, self.num_bins + 1)
        bin_counts = np.zeros(self.num_bins, dtype=int)
        for val in self.data:
            idx = min(int((val - data_min) / (data_max - data_min) * self.num_bins), self.num_bins - 1)
            bin_counts[idx] += 1

        max_count = max(bin_counts)

        # Create number line at bottom
        number_line = NumberLine(
            x_range=[data_min - 0.5, data_max + 0.5, 1],
            length=11,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
            include_numbers=True,
            font_size=18,
        )
        number_line_config = {"decimal_number_config": {"color": MUTED_COLOR}}
        number_line.shift(DOWN * 2.5)
        self.play(Create(number_line), run_time=0.8)

        # Show data points as dots on the number line
        dots = VGroup()
        for val in self.data:
            x_pos = number_line.n2p(val)[0]
            dot = Dot(
                point=[x_pos, number_line.get_center()[1] + 0.15, 0],
                radius=0.03,
                color=ACCENT_COLOR,
            )
            dots.add(dot)

        self.play(FadeIn(dots), run_time=1.0)
        self.wait(0.5)

        # Build histogram bars
        total_bar_width = self.num_bins * (self.bin_width + self.bar_gap) - self.bar_gap
        start_x = -total_bar_width / 2 + self.bin_width / 2
        base_y = number_line.get_center()[1] + 0.4
        max_height = 3.5

        bars = VGroup()
        for i in range(self.num_bins):
            height = (bin_counts[i] / max_count) * max_height if max_count > 0 else 0
            x = start_x + i * (self.bin_width + self.bar_gap)
            bar = Rectangle(
                width=self.bin_width,
                height=0.01,
                stroke_color=ACCENT_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.3,
            )
            bar.move_to([x, base_y, 0])
            bars.add(bar)

        # Animate dots fading out and bars rising
        self.play(FadeOut(dots), run_time=0.5)

        bar_anims = []
        for i, bar in enumerate(bars):
            height = (bin_counts[i] / max_count) * max_height if max_count > 0 else 0
            target_y = base_y + height / 2
            bar_anims.append(
                bar.animate.stretch_to_fit_height(max(height, 0.01)).move_to(
                    [bar.get_center()[0], target_y, 0]
                )
            )

        self.play(*bar_anims, run_time=1.5)

        # Add count labels on top of each bar
        count_labels = VGroup()
        for i, bar in enumerate(bars):
            if bin_counts[i] > 0:
                label = Text(str(bin_counts[i]), font_size=14, color=TEXT_COLOR)
                label.next_to(bar, UP, buff=0.1)
                count_labels.add(label)

        self.play(FadeIn(count_labels), run_time=0.5)

        # Add axis labels
        x_label = Text("Value", font_size=18, color=MUTED_COLOR)
        x_label.next_to(number_line, DOWN, buff=0.3)
        y_label = Text("Frequency", font_size=18, color=MUTED_COLOR)
        y_label.move_to([start_x - 0.8, base_y + max_height / 2, 0])
        self.play(FadeIn(x_label), FadeIn(y_label), run_time=0.4)

        self.wait(2.0)
