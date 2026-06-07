"""
System Flow Scene - Visualize data flow through a system architecture.
"""

from manim import Scene, Text, VGroup, Rectangle, Arrow, Dot, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, ORIGIN

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class SystemFlowScene(Scene):
    """
    Scene: Show data flow through a client-gateway-database architecture.
    Animates each component appearing and data flowing between them.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("System Architecture", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Component positions - aligned on same y-level
        y_level = 0.5
        positions = {
            "client": [-4.5, y_level, 0],
            "gateway": [-0.5, y_level, 0],
            "service_a": [3.5, y_level + 1.5, 0],
            "service_b": [3.5, y_level - 1.5, 0],
            "db": [3.5, y_level, 0],
        }

        # Create component boxes
        components = {}
        for name, pos in positions.items():
            label_text = name.replace("_", " ").title()
            box = Rectangle(
                width=2.0, height=0.8,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=BG_COLOR,
                fill_opacity=1,
            )
            box.move_to(pos)
            label = Text(label_text, font_size=16, color=TEXT_COLOR)
            label.move_to(pos)
            components[name] = VGroup(box, label)

        # Animate components appearing
        for name, comp in components.items():
            self.play(Create(comp), run_time=0.4)

        # Arrows between components
        arrow_specs = [
            ("client", "gateway", "Request"),
            ("gateway", "service_a", "Route A"),
            ("gateway", "service_b", "Route B"),
            ("service_a", "db", "Query"),
            ("service_b", "db", "Query"),
        ]

        arrows = []
        for src_name, dst_name, label_text in arrow_specs:
            src = components[src_name]
            dst = components[dst_name]

            src_pos = positions[src_name]
            dst_pos = positions[dst_name]

            # Calculate arrow start/end (edge of boxes)
            dx = dst_pos[0] - src_pos[0]
            dy = dst_pos[1] - src_pos[1]
            length = (dx**2 + dy**2) ** 0.5

            # Normalize and offset from box edges
            if abs(dx) > abs(dy):
                # Horizontal-ish arrow
                start_x = src_pos[0] + 1.0 * (1 if dx > 0 else -1)
                end_x = dst_pos[0] - 1.0 * (1 if dx > 0 else -1)
                start = [start_x, src_pos[1], 0]
                end = [end_x, dst_pos[1], 0]
            else:
                # Vertical-ish arrow
                start = [src_pos[0], src_pos[1] + 0.4 * (1 if dy > 0 else -1), 0]
                end = [dst_pos[0], dst_pos[1] - 0.4 * (1 if dy > 0 else -1), 0]

            arrow = Arrow(
                start=start, end=end,
                buff=0,
                stroke_color=ACCENT_COLOR,
                stroke_width=2,
                tip_length=0.12,
            )

            # Label on arrow
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            label = Text(label_text, font_size=12, color=MUTED_COLOR)
            label.move_to([mid_x, mid_y + 0.25, 0])

            self.play(Create(arrow), FadeIn(label), run_time=0.4)
            arrows.append((arrow, label))

        # Animate a data packet flowing through
        packet = Dot(positions["client"], color=ACCENT_COLOR, radius=0.08)

        # Client -> Gateway
        self.play(
            packet.animate.move_to(positions["gateway"]),
            run_time=0.6,
        )
        # Gateway -> Service A
        self.play(
            packet.animate.move_to(positions["service_a"]),
            run_time=0.6,
        )
        # Service A -> DB
        self.play(
            packet.animate.move_to(positions["db"]),
            run_time=0.6,
        )

        # Response back
        self.play(
            packet.animate.move_to(positions["gateway"]),
            run_time=0.6,
        )
        self.play(
            packet.animate.move_to(positions["client"]),
            run_time=0.6,
        )
        self.play(FadeOut(packet), run_time=0.2)

        self.wait(2.0)
