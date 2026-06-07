"""
Limit Sequence Scene - Visualize limits of sequences.
"""

from manim import Scene, Text, VGroup, Line, Circle, Dot, UP, DOWN, RIGHT, LEFT, Create, FadeIn
from typing import Callable, Optional
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class LimitSequenceScene(Scene):
    """
    Scene: Show a sequence converging to a limit.
    Animates terms appearing one by one, approaching the limit value.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limit_value: float = 0
        self.sequence_func: Optional[Callable[[int], float]] = lambda n: 1.0 / n
        self.start_n: int = 1
        self.end_n: int = 12

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # Create horizontal line at limit
        limit_line = Line(
            start=[-5, self.limit_value, 0],
            end=[5, self.limit_value, 0],
            stroke_color=MUTED_COLOR,
            stroke_width=1,
            stroke_opacity=0.5,
        )

        # Limit label
        limit_label = Text(
            f"L = {self.limit_value}",
            font_size=22,
            color=TEXT_COLOR,
        )
        limit_label.next_to(limit_line, LEFT, buff=0.3)

        self.play(Create(limit_line), FadeIn(limit_label), run_time=0.5)

        if self.sequence_func:
            # Generate sequence points
            points = []
            for n in range(self.start_n, self.end_n + 1):
                y_val = self.sequence_func(n)
                points.append((n, y_val))

            # Animate each term appearing
            dots = VGroup()
            for i, (n, y_val) in enumerate(points):
                x_pos = -4 + i * 0.7
                y_pos = y_val * 3  # Scale for visibility

                dot = Dot(
                    [x_pos, y_pos, 0],
                    color=ACCENT_COLOR,
                    radius=0.06,
                )
                dots.add(dot)

                # Term label (only show a few to avoid clutter)
                if i < 6 or i == len(points) - 1:
                    n_label = Text(f"n={n}", font_size=12, color=MUTED_COLOR)
                    n_label.next_to(dot, DOWN, buff=0.15)

                    term_label = Text(f"{y_val:.3f}", font_size=14, color=TEXT_COLOR)
                    term_label.next_to(dot, UP, buff=0.1)

                    self.play(
                        Create(dot),
                        FadeIn(n_label),
                        FadeIn(term_label),
                        run_time=0.4,
                    )
                else:
                    self.play(Create(dot), run_time=0.2)

                self.wait(0.1)

            # Convergence annotation
            converge_text = Text(
                f"lim a(n) = {self.limit_value}  as n -> inf",
                font_size=22,
                color=ACCENT_COLOR,
            )
            converge_text.to_edge(DOWN, buff=0.8)
            self.play(FadeIn(converge_text), run_time=0.6)

            # Highlight convergence with a bracket
            self.wait(2)

    def set_sequence(
        self,
        seq_func: Callable[[int], float],
        limit: float,
        start_n: int = 1,
        end_n: int = 12,
    ) -> None:
        self.sequence_func = seq_func
        self.limit_value = limit
        self.start_n = start_n
        self.end_n = end_n
