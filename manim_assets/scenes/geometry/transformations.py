"""
Transformations Scene - Visualize geometric transformations.
"""

from manim import Scene, Text, VGroup, Square, Polygon, Arrow, Dot, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, Transform, Rotate, ORIGIN
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class ReflectionScene(Scene):
    """
    Scene: Show reflection of a shape across a line.
    Clearly shows the mirror line and the before/after shape.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.axis = "y"  # Reflect across y-axis

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Reflection across Y-axis", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Mirror line (y-axis)
        from manim import DashedLine
        mirror_line = DashedLine(
            [0, -3, 0], [0, 3, 0],
            stroke_color=MUTED_COLOR,
            stroke_width=2,
            dash_length=0.2,
        )
        mirror_label = Text("mirror", font_size=14, color=MUTED_COLOR)
        mirror_label.next_to(mirror_line.get_top(), RIGHT, buff=0.15)

        self.play(Create(mirror_line), FadeIn(mirror_label), run_time=0.5)

        # Original shape (an L-shape on the right)
        original = Polygon(
            [1, -1, 0], [1, 1, 0], [2, 1, 0], [2, 0, 0], [1.5, 0, 0], [1.5, -1, 0],
            stroke_color=ACCENT_COLOR,
            stroke_width=2.5,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.15,
        )

        # Reflected shape (on the left)
        reflected = Polygon(
            [-1, -1, 0], [-1, 1, 0], [-2, 1, 0], [-2, 0, 0], [-1.5, 0, 0], [-1.5, -1, 0],
            stroke_color=TEXT_COLOR,
            stroke_width=2.5,
            fill_color=TEXT_COLOR,
            fill_opacity=0.1,
        )

        # Show original
        orig_label = Text("Original", font_size=16, color=ACCENT_COLOR)
        orig_label.next_to(original, DOWN, buff=0.3)
        self.play(Create(original), FadeIn(orig_label), run_time=0.8)
        self.wait(0.3)

        # Show reflection
        refl_label = Text("Reflected", font_size=16, color=TEXT_COLOR)
        refl_label.next_to(reflected, DOWN, buff=0.3)
        self.play(Create(reflected), FadeIn(refl_label), run_time=0.8)

        # Draw connecting arrows between corresponding points
        arrows = VGroup()
        for orig_pt, refl_pt in [
            ([1, 1, 0], [-1, 1, 0]),
            ([2, 1, 0], [-2, 1, 0]),
            ([1, -1, 0], [-1, -1, 0]),
        ]:
            arrow = Arrow(
                start=orig_pt, end=refl_pt,
                buff=0.1,
                stroke_color=MUTED_COLOR,
                stroke_width=1,
                tip_length=0.1,
            )
            arrows.add(arrow)

        self.play(Create(arrows), run_time=0.5)

        self.wait(2.0)


class RotationCenterScene(Scene):
    """
    Scene: Show rotation of a shape around a center point.
    Animates the rotation step by step.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Rotation around Center", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Center point
        center = Dot(ORIGIN, color=TEXT_COLOR, radius=0.08)
        center_label = Text("center", font_size=14, color=TEXT_COLOR)
        center_label.next_to(center, DOWN_LEFT, buff=0.15)

        # Original shape
        square = Square(
            side_length=1.5,
            stroke_color=ACCENT_COLOR,
            stroke_width=2.5,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.15,
        )

        self.play(Create(center), FadeIn(center_label), Create(square), run_time=0.8)
        self.wait(0.3)

        # Rotate in steps with labels
        total_angle = 360
        step = 90
        for angle in range(step, total_angle + step, step):
            step_label = Text(
                f"Rotated {angle} deg",
                font_size=18,
                color=ACCENT_COLOR,
            )
            step_label.to_edge(DOWN, buff=0.6)

            self.play(
                Rotate(square, angle=np.radians(step), about_point=ORIGIN),
                FadeIn(step_label),
                run_time=0.8,
            )
            self.wait(0.2)
            self.play(FadeOut(step_label), run_time=0.1)

        # Final
        final_label = Text("Full rotation = 360 deg", font_size=20, color=ACCENT_COLOR)
        final_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(final_label), run_time=0.5)

        self.wait(2.0)


class TransformScene(Scene):
    """
    Scene: Show multiple transformations applied to a shape.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Geometric Transformations", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Original shape
        square = Square(
            side_length=1.2,
            stroke_color=ACCENT_COLOR,
            stroke_width=2.5,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.15,
        )
        square.shift(LEFT * 3)

        orig_label = Text("Original", font_size=16, color=ACCENT_COLOR)
        orig_label.next_to(square, DOWN, buff=0.3)

        self.play(Create(square), FadeIn(orig_label), run_time=0.6)

        # Translate
        translated = square.copy()
        translated.shift(RIGHT * 2)
        trans_label = Text("Translated", font_size=16, color=TEXT_COLOR)
        trans_label.next_to(translated, DOWN, buff=0.3)

        self.play(
            Transform(square.copy(), translated),
            FadeIn(trans_label),
            run_time=0.8,
        )

        # Rotate
        rotated = square.copy()
        rotated.shift(RIGHT * 2)
        rotated.rotate(np.radians(45))
        rot_label = Text("Rotated", font_size=16, color=TEXT_COLOR)
        rot_label.next_to(rotated, DOWN, buff=0.3)

        self.play(
            Transform(translated.copy(), rotated),
            FadeIn(rot_label),
            run_time=0.8,
        )

        # Scale
        scaled = square.copy()
        scaled.shift(RIGHT * 2)
        scaled.scale(1.5)
        scale_label = Text("Scaled", font_size=16, color=TEXT_COLOR)
        scale_label.next_to(scaled, DOWN, buff=0.3)

        self.play(
            Transform(rotated.copy(), scaled),
            FadeIn(scale_label),
            run_time=0.8,
        )

        self.wait(2.0)
