"""
Sorting Scene - Visualize sorting algorithms with animated bar charts.
"""

from manim import Scene, Text, VGroup, Rectangle, UP, DOWN, Create, FadeIn, FadeOut
from typing import List
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class SortingScene(Scene):
    """
    Scene: Visualize sorting with animated bar chart.
    Bars swap positions and highlight comparisons.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values: List[int] = [5, 3, 8, 1, 7, 2, 6, 4]
        self.bar_width: float = 0.55
        self.bar_gap: float = 0.15
        self.max_height: float = 3.0
        self.base_y: float = -1.5

    def _bar_x(self, index: int) -> float:
        """Get x position for bar at given index."""
        total_width = len(self.values) * (self.bar_width + self.bar_gap) - self.bar_gap
        start_x = -total_width / 2 + self.bar_width / 2
        return start_x + index * (self.bar_width + self.bar_gap)

    def _create_bars(self) -> List[Rectangle]:
        """Create bar representations of values."""
        bars = []
        max_val = max(self.values)

        for i, val in enumerate(self.values):
            height = (val / max_val) * self.max_height
            bar = Rectangle(
                width=self.bar_width,
                height=height,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.3,
            )
            x = self._bar_x(i)
            bar.move_to([x, self.base_y + height / 2, 0])
            bars.append(bar)

        return bars

    def _bar_y(self, value: int) -> float:
        """Get y center for a bar of given value (bottom-aligned to base_y)."""
        max_val = max(self.values)
        height = (value / max_val) * self.max_height
        return self.base_y + height / 2

    def _swap_bars(self, bars: List[Rectangle], i: int, j: int) -> None:
        """Swap two bars with animation, keeping each bar at its correct y."""
        x_i = self._bar_x(i)
        x_j = self._bar_x(j)
        y_i = self._bar_y(self.values[j])  # After swap, bar at i has values[j]
        y_j = self._bar_y(self.values[i])  # After swap, bar at j has values[i]

        self.play(
            bars[i].animate.move_to([x_j, y_j, 0]),
            bars[j].animate.move_to([x_i, y_i, 0]),
            run_time=0.3,
        )

        bars[i], bars[j] = bars[j], bars[i]
        self.values[i], self.values[j] = self.values[j], self.values[i]

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Bubble Sort", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        bars = self._create_bars()
        bars_group = VGroup(*bars)
        self.play(Create(bars_group), run_time=1.0)
        self.wait(0.3)

        # Bubble sort with animations
        n = len(self.values)
        for i in range(n):
            for j in range(0, n - i - 1):
                # Highlight comparison
                self.play(
                    bars[j].animate.set_stroke(color=TEXT_COLOR, width=3),
                    bars[j + 1].animate.set_stroke(color=TEXT_COLOR, width=3),
                    run_time=0.15,
                )

                if self.values[j] > self.values[j + 1]:
                    self._swap_bars(bars, j, j + 1)

                # Reset highlight
                self.play(
                    bars[j].animate.set_stroke(color=MUTED_COLOR, width=1.5),
                    bars[j + 1].animate.set_stroke(color=MUTED_COLOR, width=1.5),
                    run_time=0.08,
                )

            # Mark sorted element
            self.play(
                bars[n - i - 1].animate.set_fill(ACCENT_COLOR, opacity=0.7),
                run_time=0.15,
            )

        self.wait(2.0)


class QuickSortScene(SortingScene):
    """QuickSort visualization with partition highlighting."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Quick Sort", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        bars = self._create_bars()
        bars_group = VGroup(*bars)
        self.play(Create(bars_group), run_time=1.0)
        self.wait(0.3)

        self._quicksort_animate(bars, 0, len(self.values) - 1)

        for bar in bars:
            self.play(
                bar.animate.set_fill(ACCENT_COLOR, opacity=0.7),
                run_time=0.04,
            )

        self.wait(2.0)

    def _quicksort_animate(self, bars: List[Rectangle], low: int, high: int) -> None:
        if low < high:
            pivot_idx = self._partition_animate(bars, low, high)
            self._quicksort_animate(bars, low, pivot_idx - 1)
            self._quicksort_animate(bars, pivot_idx + 1, high)

    def _partition_animate(self, bars: List[Rectangle], low: int, high: int) -> int:
        pivot = self.values[high]

        self.play(
            bars[high].animate.set_stroke(color=ACCENT_COLOR, width=3),
            run_time=0.2,
        )

        i = low - 1
        for j in range(low, high):
            self.play(
                bars[j].animate.set_stroke(color=TEXT_COLOR, width=3),
                run_time=0.1,
            )

            if self.values[j] <= pivot:
                i += 1
                if i != j:
                    self._swap_bars(bars, i, j)

            self.play(
                bars[j].animate.set_stroke(color=MUTED_COLOR, width=1.5),
                run_time=0.05,
            )

        if i + 1 != high:
            self._swap_bars(bars, i + 1, high)

        self.play(
            bars[i + 1].animate.set_fill(ACCENT_COLOR, opacity=0.5),
            bars[i + 1].animate.set_stroke(color=MUTED_COLOR, width=1.5),
            run_time=0.15,
        )

        return i + 1


class MergeSortScene(SortingScene):
    """MergeSort visualization — bars physically move to merged positions."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Merge Sort", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        bars = self._create_bars()
        bars_group = VGroup(*bars)
        self.play(Create(bars_group), run_time=1.0)
        self.wait(0.3)

        self._mergesort_animate(bars, 0, len(self.values) - 1)

        for bar in bars:
            self.play(
                bar.animate.set_fill(ACCENT_COLOR, opacity=0.7),
                run_time=0.04,
            )

        self.wait(2.0)

    def _mergesort_animate(self, bars: List[Rectangle], left: int, right: int) -> None:
        if left < right:
            mid = (left + right) // 2

            # Highlight left half
            highlights = []
            for k in range(left, mid + 1):
                highlights.append(bars[k].animate.set_stroke(color=TEXT_COLOR, width=2.5))
            self.play(*highlights, run_time=0.2)
            self.wait(0.1)

            resets = []
            for k in range(left, mid + 1):
                resets.append(bars[k].animate.set_stroke(color=MUTED_COLOR, width=1.5))
            self.play(*resets, run_time=0.15)

            self._mergesort_animate(bars, left, mid)

            # Highlight right half
            highlights = []
            for k in range(mid + 1, right + 1):
                highlights.append(bars[k].animate.set_stroke(color=ACCENT_COLOR, width=2.5))
            self.play(*highlights, run_time=0.2)
            self.wait(0.1)

            resets = []
            for k in range(mid + 1, right + 1):
                resets.append(bars[k].animate.set_stroke(color=MUTED_COLOR, width=1.5))
            self.play(*resets, run_time=0.15)

            self._mergesort_animate(bars, mid + 1, right)
            self._merge_animate(bars, left, mid, right)

    def _merge_animate(self, bars: List[Rectangle], left: int, mid: int, right: int) -> None:
        """Merge two sorted halves — physically move bars to correct positions."""
        left_arr = self.values[left:mid + 1]
        right_arr = self.values[mid + 1:right + 1]

        # Compute merged order of values
        merged = []
        i = j = 0
        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] <= right_arr[j]:
                merged.append(left_arr[i])
                i += 1
            else:
                merged.append(right_arr[j])
                j += 1
        merged.extend(left_arr[i:])
        merged.extend(right_arr[j:])

        # Build a map: for each position in [left..right], which bar index
        # currently holds the value that should go there?
        # We need to rearrange bars[left..right] to match merged order.
        # Strategy: find which existing bar has the value for each merged position,
        # then animate all bars to their new x-positions simultaneously.

        # Track which bar indices are in the range [left..right]
        # and their current values
        available = list(range(left, right + 1))  # indices into bars list

        # For each merged position, find the bar that currently holds that value
        new_bar_order = []  # bar indices in merged order
        used = set()
        for val in merged:
            for idx in available:
                if idx not in used and self.values[idx] == val:
                    new_bar_order.append(idx)
                    used.add(idx)
                    break

        # Highlight bars being merged
        merge_highlights = []
        for idx in new_bar_order:
            merge_highlights.append(bars[idx].animate.set_stroke(color=TEXT_COLOR, width=2.5))
        self.play(*merge_highlights, run_time=0.2)

        # Animate all bars to their new positions simultaneously
        move_anims = []
        for new_pos, bar_idx in enumerate(new_bar_order):
            target_x = self._bar_x(left + new_pos)
            target_y = self._bar_y(self.values[bar_idx])
            move_anims.append(bars[bar_idx].animate.move_to([target_x, target_y, 0]))

        self.play(*move_anims, run_time=0.4)

        # Update values and bars list to reflect new order
        old_bars_slice = [bars[i] for i in range(left, right + 1)]
        for new_pos, bar_idx in enumerate(new_bar_order):
            self.values[left + new_pos] = merged[new_pos]
            # We need to rebuild bars[left..right] in new order
        for new_pos, old_bar_idx in enumerate(new_bar_order):
            old_bars_slice[new_pos] = bars[old_bar_idx]
        for new_pos, bar in enumerate(old_bars_slice):
            bars[left + new_pos] = bar

        # Reset stroke and flash fill to show merge complete
        reset_anims = []
        for k in range(left, right + 1):
            reset_anims.append(bars[k].animate.set_stroke(color=MUTED_COLOR, width=1.5))
            reset_anims.append(bars[k].animate.set_fill(ACCENT_COLOR, opacity=0.5))
        self.play(*reset_anims, run_time=0.2)

        # Brief pause then reset fill
        reset_fill = []
        for k in range(left, right + 1):
            reset_fill.append(bars[k].animate.set_fill(ACCENT_COLOR, opacity=0.3))
        self.play(*reset_fill, run_time=0.15)
