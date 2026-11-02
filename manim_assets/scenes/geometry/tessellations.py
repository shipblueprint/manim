"""
Tessellation Scene - Visualize repeating tiling patterns.
"""

from manim import Scene, Text, VGroup, RegularPolygon, Polygon, Square, UP, DOWN, Create, FadeIn, FadeOut
from typing import List
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class TessellationScene(Scene):
    """
    Scene: Show tessellation patterns with animated tile placement.
    Builds up a tiling pattern tile by tile.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape_type = "hexagon"
        self.grid_size = 3

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        if self.shape_type == "hexagon":
            self._create_hexagon_tessellation()
        elif self.shape_type == "triangle":
            self._create_triangle_tessellation()
        elif self.shape_type == "square":
            self._create_square_tessellation()

    def _create_hexagon_tessellation(self) -> None:
        """Create hexagonal tessellation."""
        title = Text("Hexagonal Tessellation", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        tiles = VGroup()
        size = 0.55
        cols = 7
        rows = 5

        for row in range(rows):
            for col in range(cols):
                x = col * size * 1.75 - (cols * size * 1.75) / 2
                y = row * size * 1.5 - (rows * size * 1.5) / 2
                if row % 2 == 1:
                    x += size * 0.875

                hex_tile = RegularPolygon(
                    n=6,
                    stroke_color=MUTED_COLOR,
                    stroke_width=1.5,
                    fill_opacity=0.08,
                    fill_color=ACCENT_COLOR,
                )
                hex_tile.scale(size / 0.7)
                hex_tile.move_to([x, y, 0])
                tiles.add(hex_tile)

        # Animate tiles appearing in batches
        batch_size = 5
        for i in range(0, len(tiles), batch_size):
            batch = VGroup(*tiles[i:i + batch_size])
            self.play(
                Create(batch),
                run_time=0.25,
            )

        # Color a few tiles to show the pattern
        highlight_indices = [0, 3, 7, 12, 18, 24, 30]
        for idx in highlight_indices:
            if idx < len(tiles):
                self.play(
                    tiles[idx].animate.set_fill(ACCENT_COLOR, opacity=0.25),
                    tiles[idx].animate.set_stroke(color=ACCENT_COLOR, width=2),
                    run_time=0.2,
                )

        self.wait(2.0)

    def _create_square_tessellation(self) -> None:
        """Create square tessellation."""
        title = Text("Square Tessellation", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        tiles = VGroup()
        size = 0.8
        cols = 9
        rows = 6

        for row in range(rows):
            for col in range(cols):
                x = col * size - (cols * size) / 2 + size / 2
                y = row * size - (rows * size) / 2 + size / 2

                sq = Square(
                    side_length=size * 0.95,
                    stroke_color=MUTED_COLOR,
                    stroke_width=1,
                    fill_opacity=0.05,
                    fill_color=ACCENT_COLOR,
                )
                sq.move_to([x, y, 0])
                tiles.add(sq)

        batch_size = 7
        for i in range(0, len(tiles), batch_size):
            batch = VGroup(*tiles[i:i + batch_size])
            self.play(Create(batch), run_time=0.2)

        # Checkerboard pattern
        for idx, tile in enumerate(tiles):
            row = idx // cols
            col = idx % cols
            if (row + col) % 2 == 0:
                self.play(
                    tile.animate.set_fill(ACCENT_COLOR, opacity=0.2),
                    tile.animate.set_stroke(color=ACCENT_COLOR, width=1.5),
                    run_time=0.03,
                )

        self.wait(2.0)

    def _create_triangle_tessellation(self) -> None:
        """Create triangle tessellation."""
        title = Text("Triangle Tessellation", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        tiles = VGroup()
        size = 0.7
        cols = 8
        rows = 5

        for row in range(rows):
            for col in range(cols):
                x = col * size - (cols * size) / 2
                y = row * size * 0.87 - (rows * size * 0.87) / 2

                # Upward triangle
                tri_up = Polygon(
                    [x, y, 0],
                    [x + size, y, 0],
                    [x + size / 2, y + size * 0.87, 0],
                    stroke_color=MUTED_COLOR,
                    stroke_width=1,
                    fill_opacity=0.05,
                    fill_color=ACCENT_COLOR,
                )
                tiles.add(tri_up)

                # Downward triangle
                tri_down = Polygon(
                    [x + size / 2, y, 0],
                    [x + size * 1.5, y, 0],
                    [x + size, y + size * 0.87, 0],
                    stroke_color=MUTED_COLOR,
                    stroke_width=1,
                    fill_opacity=0.05,
                    fill_color=TEXT_COLOR,
                )
                tiles.add(tri_down)

        batch_size = 8
        for i in range(0, len(tiles), batch_size):
            batch = VGroup(*tiles[i:i + batch_size])
            self.play(Create(batch), run_time=0.2)

        # Highlight alternating triangles
        for idx, tile in enumerate(tiles):
            if idx % 3 == 0:
                self.play(
                    tile.animate.set_fill(ACCENT_COLOR, opacity=0.2),
                    tile.animate.set_stroke(color=ACCENT_COLOR, width=1.5),
                    run_time=0.03,
                )

        self.wait(2.0)


class SymmetryGroupScene(Scene):
    """
    Scene: Show rotational symmetry of regular polygons.
    Demonstrates how many times a polygon maps onto itself during rotation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.n_sides = 6

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text(
            f"{self.n_sides}-fold Rotational Symmetry",
            font_size=24,
            color=TEXT_COLOR,
            font=HEADING_FONT,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Draw the polygon
        from manim import Dot, Rotate, ORIGIN
        poly = RegularPolygon(
            n=self.n_sides,
            stroke_color=ACCENT_COLOR,
            stroke_width=2.5,
        )
        poly.scale(1.5)

        # Mark one vertex to track rotation
        vertices = poly.get_vertices()
        marker = Dot(
            vertices[0],
            color=TEXT_COLOR,
            radius=0.08,
        )

        self.play(Create(poly), Create(marker), run_time=0.8)
        self.wait(0.3)

        # Rotate step by step
        angle_step = 2 * np.pi / self.n_sides
        for i in range(self.n_sides):
            step_label = Text(
                f"Rotation {i + 1}/{self.n_sides}: {int(360 / self.n_sides * (i + 1))} deg",
                font_size=18,
                color=ACCENT_COLOR,
            )
            step_label.to_edge(DOWN, buff=0.6)

            self.play(
                Rotate(poly, angle=angle_step, about_point=ORIGIN),
                Rotate(marker, angle=angle_step, about_point=ORIGIN),
                FadeIn(step_label),
                run_time=0.8,
            )
            self.wait(0.2)
            self.play(FadeOut(step_label), run_time=0.1)

        # Final symmetry label
        final = Text(
            f"Symmetry order = {self.n_sides}",
            font_size=22,
            color=ACCENT_COLOR,
        )
        final.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(final), run_time=0.5)

        self.wait(2.0)
