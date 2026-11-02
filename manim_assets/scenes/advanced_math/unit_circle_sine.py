"""
Unit Circle Spinning Out Sine/Cosine Waves Scene.
"""

from manim import Scene, Axes, Circle, Text, VGroup, Dot, Line, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class UnitCircleSineScene(Scene):
    """
    Scene: A point rotates around the unit circle while its
    projection traces out sine and cosine waves to the right.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.radius: float = 1.5
        self.n_rotations: float = 2.0
        self.wave_x_range: float = 8.0  # Width of wave display

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Unit Circle -> Sine & Cosine", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.4)
        self.play(FadeIn(title), run_time=0.5)

        # Unit circle on the left
        circle_center = [-4.0, -0.3, 0]
        unit_circle = Circle(
            radius=self.radius,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
        )
        unit_circle.move_to(circle_center)

        # Axes for circle
        h_line = Line(
            [circle_center[0] - self.radius - 0.3, circle_center[1], 0],
            [circle_center[0] + self.radius + 0.3, circle_center[1], 0],
            stroke_color=MUTED_COLOR, stroke_width=1,
        )
        v_line = Line(
            [circle_center[0], circle_center[1] - self.radius - 0.3, 0],
            [circle_center[0], circle_center[1] + self.radius + 0.3, 0],
            stroke_color=MUTED_COLOR, stroke_width=1,
        )

        self.play(Create(unit_circle), Create(h_line), Create(v_line), run_time=0.8)

        # Wave axes on the right
        wave_start_x = circle_center[0] + self.radius + 0.8
        wave_y = circle_center[1]
        wave_axes = Axes(
            x_range=[0, self.wave_x_range, 1],
            y_range=[-1.8, 1.8, 0.5],
            x_length=self.wave_x_range * 0.95,
            y_length=self.radius * 2 + 0.6,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1,
                "include_numbers": False,
            },
            tips=False,
        )
        wave_axes.move_to([wave_start_x + self.wave_x_range * 0.47, wave_y, 0])

        self.play(Create(wave_axes), run_time=0.6)

        # Labels
        sin_label = Text("sin", font_size=14, color=ACCENT_COLOR)
        sin_label.next_to(wave_axes.y_axis, UP, buff=0.1)
        cos_label = Text("cos", font_size=14, color=TEXT_COLOR)
        cos_label.next_to(sin_label, RIGHT, buff=0.5)
        self.add(sin_label, cos_label)

        # Rotating point on circle
        point_on_circle = Dot(
            point=[circle_center[0] + self.radius, circle_center[1], 0],
            radius=0.08,
            color=ACCENT_COLOR,
        )
        self.add(point_on_circle)

        # Radius line from center to point
        radius_line = Line(
            circle_center,
            [circle_center[0] + self.radius, circle_center[1], 0],
            stroke_color=TEXT_COLOR, stroke_width=1.5,
        )
        self.add(radius_line)

        # Horizontal projection line (cosine)
        cos_proj_line = Line(
            [circle_center[0], circle_center[1], 0],
            [circle_center[0] + self.radius, circle_center[1], 0],
            stroke_color=TEXT_COLOR, stroke_width=1, stroke_opacity=0.5,
        )
        self.add(cos_proj_line)

        # Vertical projection line (sine)
        sin_proj_line = Line(
            [circle_center[0] + self.radius, circle_center[1], 0],
            [circle_center[0] + self.radius, circle_center[1], 0],
            stroke_color=ACCENT_COLOR, stroke_width=1, stroke_opacity=0.5,
        )
        self.add(sin_proj_line)

        # Trace paths for sine and cosine waves
        sin_points = []
        cos_points = []

        # Precompute wave positions
        n_frames = 200
        angles = np.linspace(0, self.n_rotations * 2 * np.pi, n_frames)

        # Map angle to wave x position
        wave_x_scale = self.wave_x_range / (self.n_rotations * 2 * np.pi)

        for angle in angles:
            # Point on circle
            px = circle_center[0] + self.radius * np.cos(angle)
            py = circle_center[1] + self.radius * np.sin(angle)

            # Wave x position
            wave_x = wave_start_x + angle * wave_x_scale

            # Sine wave point (y = sin(angle))
            sin_screen = wave_axes.c2p(angle * wave_x_scale, np.sin(angle))

            # Cosine wave point (y = cos(angle))
            cos_screen = wave_axes.c2p(angle * wave_x_scale, np.cos(angle))

            sin_points.append(sin_screen)
            cos_points.append(cos_screen)

        # Create wave curves
        from manim import VMobject
        sin_curve = VMobject(stroke_color=ACCENT_COLOR, stroke_width=2.5)
        cos_curve = VMobject(stroke_color=TEXT_COLOR, stroke_width=2, stroke_opacity=0.6)

        # Animate frame by frame
        step = 4  # Process every 4th frame for speed
        for i in range(0, n_frames, step):
            angle = angles[i]
            px = circle_center[0] + self.radius * np.cos(angle)
            py = circle_center[1] + self.radius * np.sin(angle)

            # Update point position
            point_on_circle.move_to([px, py, 0])

            # Update radius line
            radius_line.put_start_and_end_on(circle_center, [px, py, 0])

            # Update projection lines
            cos_proj_line.put_start_and_end_on(
                [circle_center[0], py, 0], [px, py, 0]
            )
            # Guard against zero-length line (start == end at angle 0/pi)
            sin_start = [px, circle_center[1], 0]
            sin_end = [px, py, 0]
            if np.allclose(sin_start, sin_end):
                sin_proj_line.put_start_and_end_on(sin_start, [sin_end[0], sin_end[1] + 0.001, sin_end[2]])
            else:
                sin_proj_line.put_start_and_end_on(sin_start, sin_end)

            # Update wave curves
            if i >= step:
                sin_curve.set_points_as_corners(sin_points[:i + 1])
                cos_curve.set_points_as_corners(cos_points[:i + 1])

            # Connecting line from circle point to wave
            wave_x = wave_start_x + angle * wave_x_scale
            connect_line = Line(
                [px, py, 0],
                [wave_x, py, 0],
                stroke_color=ACCENT_COLOR,
                stroke_width=0.8,
                stroke_opacity=0.3,
            )

            self.add(connect_line)
            self.add(sin_curve, cos_curve)
            self.wait(0.02)
            self.remove(connect_line)

        # Keep final curves
        self.add(sin_curve, cos_curve)

        self.wait(2.0)
