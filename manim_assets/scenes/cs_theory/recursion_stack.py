"""
Recursion Call Stack Visualization Scene.
"""

from manim import Scene, Text, VGroup, Rectangle, Arrow, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class RecursionStackScene(Scene):
    """
    Scene: Visualize recursive factorial computation.
    Shows the call stack growing as recursive calls are made,
    then unwinding as values are returned.

    factorial(5) -> factorial(4) -> ... -> factorial(1)
    Then returns: 1, 2, 6, 24, 120
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n: int = 5
        self.cell_width: float = 2.8
        self.cell_height: float = 0.55

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Recursion Call Stack — factorial(n)", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Stack grows downward from top
        stack_center_x = -1.5
        top_y = 2.2
        stack_items: list = []  # list of (rect, label, return_label)

        # Footer area for operation text (fixed position)
        footer_y_pos = None

        # === PUSH PHASE: Build the call stack ===
        for i in range(self.n, 0, -1):
            # Create stack frame
            rect = Rectangle(
                width=self.cell_width,
                height=self.cell_height,
                stroke_color=ACCENT_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.15,
            )

            call_text = f"fact({i})"
            label = Text(call_text, font_size=14, color=TEXT_COLOR)

            # Return value placeholder (shown later)
            return_label = Text("?", font_size=14, color=MUTED_COLOR)

            # Position
            frame_idx = self.n - i  # 0 for first (fact(5)), 1 for fact(4), etc.
            y = top_y - frame_idx * (self.cell_height + 0.12)

            rect.move_to([stack_center_x, y, 0])
            label.move_to([stack_center_x - 0.7, y, 0])
            return_label.move_to([stack_center_x + 0.9, y, 0])

            # Animate push
            op_text = Text(f"Call fact({i})", font_size=14, color=ACCENT_COLOR)
            op_text.to_edge(DOWN, buff=0.5)

            # Slide in from right
            rect.move_to([stack_center_x + 4, y, 0])
            label.move_to([stack_center_x - 0.7 + 4, y, 0])
            return_label.move_to([stack_center_x + 0.9 + 4, y, 0])

            self.play(
                rect.animate.move_to([stack_center_x, y, 0]),
                label.animate.move_to([stack_center_x - 0.7, y, 0]),
                return_label.animate.move_to([stack_center_x + 0.9, y, 0]),
                Create(rect),
                FadeIn(label),
                FadeIn(return_label),
                FadeIn(op_text),
                run_time=0.5,
            )

            stack_items.append((rect, label, return_label))
            self.remove(op_text)

        # Base case reached
        base_text = Text("Base case! fact(1) = 1", font_size=16, color=ACCENT_COLOR)
        base_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(base_text), run_time=0.4)
        self.wait(0.3)
        self.remove(base_text)

        # === POP PHASE: Unwind the call stack ===
        result = 1
        for i in range(len(stack_items) - 1, -1, -1):
            rect, label, return_label = stack_items[i]
            n_val = self.n - i  # fact(n_val)

            # Compute return value
            if n_val == 1:
                ret_val = 1
            else:
                ret_val = n_val * result

            # Update return value label
            new_return = Text(str(ret_val), font_size=14, color=TEXT_COLOR)
            new_return.move_to(return_label.get_center())

            # Highlight current frame
            self.play(
                rect.animate.set_fill(ACCENT_COLOR, opacity=0.3)
                .set_stroke(color=TEXT_COLOR, width=2.5),
                run_time=0.3,
            )

            # Show computation in footer
            if n_val > 1:
                comp_text = Text(
                    f"fact({n_val}) = {n_val} x {result} = {ret_val}",
                    font_size=14, color=TEXT_COLOR,
                )
            else:
                comp_text = Text(f"fact({n_val}) = {ret_val}", font_size=14, color=TEXT_COLOR)
            comp_text.to_edge(DOWN, buff=0.5)

            # Update return value
            self.play(
                FadeOut(return_label),
                FadeIn(new_return),
                FadeIn(comp_text),
                run_time=0.3,
            )
            stack_items[i] = (rect, label, new_return)

            # Pop frame (fade out)
            self.play(
                FadeOut(rect),
                FadeOut(label),
                FadeOut(new_return),
                run_time=0.3,
            )

            result = ret_val
            self.remove(comp_text)

        # Show final result
        final = Text(f"fact({self.n}) = {result}", font_size=24, color=ACCENT_COLOR)
        final.move_to([0, 0, 0])
        self.play(FadeIn(final), run_time=0.8)

        self.wait(2.0)
