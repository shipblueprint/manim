"""
Basic Shapes Scene - Display animated geometric primitives.
"""

from manim import Scene, Text, VGroup, Circle, Square, Triangle, Rectangle, RegularPolygon, UP, DOWN, LEFT, RIGHT, Create, FadeIn, Rotate
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class BasicShapesScene(Scene):
    """
    Scene: Display animated geometric primitives with labels.
    Each shape appears with an animation and a label.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Basic Shapes", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Shape definitions: (shape_object, label, position)
        shapes_data = [
            (Circle(radius=0.6, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Circle", [-3.5, 1.2, 0]),
            (Square(side_length=1.2, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Square", [-1.2, 1.2, 0]),
            (Triangle(stroke_color=ACCENT_COLOR, stroke_width=2.5), "Triangle", [1.2, 1.2, 0]),
            (RegularPolygon(n=5, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Pentagon", [3.5, 1.2, 0]),
            (RegularPolygon(n=6, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Hexagon", [-3.5, -1.5, 0]),
            (Rectangle(width=1.4, height=0.8, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Rectangle", [-1.2, -1.5, 0]),
            (RegularPolygon(n=8, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Octagon", [1.2, -1.5, 0]),
            (RegularPolygon(n=3, stroke_color=ACCENT_COLOR, stroke_width=2.5), "Equilateral", [3.5, -1.5, 0]),
        ]

        # Scale shapes to similar sizes
        for shape, label, pos in shapes_data:
            shape.scale(0.7)
            shape.move_to(pos)

        # Animate each shape appearing with label
        for shape, label_text, pos in shapes_data:
            label = Text(label_text, font_size=14, color=MUTED_COLOR)
            label.next_to(shape, DOWN, buff=0.2)

            self.play(
                Create(shape),
                FadeIn(label),
                run_time=0.4,
            )

        # Animate a rotation on the hexagon to add life
        hex_shape = shapes_data[4][0]
        self.play(Rotate(hex_shape, angle=np.radians(60)), run_time=0.6)

        self.wait(2.0)


class PolygonScene(Scene):
    """
    Scene: Display regular polygons with increasing number of sides.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Regular Polygons", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Show polygons from triangle to dodecagon
        polygons_data = [
            (3, "Triangle"),
            (4, "Square"),
            (5, "Pentagon"),
            (6, "Hexagon"),
            (8, "Octagon"),
            (12, "Dodecagon"),
        ]

        positions = [
            [-3.5, 1.2, 0], [-1.2, 1.2, 0], [1.2, 1.2, 0],
            [-3.5, -1.5, 0], [-1.2, -1.5, 0], [1.2, -1.5, 0],
        ]

        for i, (n, name) in enumerate(polygons_data):
            poly = RegularPolygon(
                n=n,
                stroke_color=ACCENT_COLOR,
                stroke_width=2.5,
            )
            poly.scale(0.6)
            poly.move_to(positions[i])

            label = Text(f"{name} (n={n})", font_size=12, color=MUTED_COLOR)
            label.next_to(poly, DOWN, buff=0.15)

            self.play(Create(poly), FadeIn(label), run_time=0.4)

        # Show circle as "infinite" polygon
        circle = Circle(
            radius=0.6,
            stroke_color=TEXT_COLOR,
            stroke_width=2.5,
        )
        circle.move_to([3.5, -0.2, 0])
        circle_label = Text("n = inf", font_size=12, color=MUTED_COLOR)
        circle_label.next_to(circle, DOWN, buff=0.15)

        self.play(Create(circle), FadeIn(circle_label), run_time=0.5)

        self.wait(2.0)
