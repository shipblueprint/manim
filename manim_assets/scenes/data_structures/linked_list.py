"""
Linked List Scene - Visualize linked list data structures.
"""

from manim import Scene, Text, VGroup, Rectangle, Arrow, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut
from typing import List, Optional
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class LinkedListScene(Scene):
    """
    Scene: Visualize a singly linked list.
    Shows nodes with data and arrows, built up step by step.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values: List[int] = [3, 7, 1, 9, 4]

    def _create_node(self, value: int, x_pos: float) -> VGroup:
        """Create a linked list node with data box and pointer box."""
        # Data box
        data_box = Rectangle(
            width=0.9, height=0.6,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
            fill_color=BG_COLOR,
            fill_opacity=1,
        )
        data_text = Text(str(value), font_size=20, color=TEXT_COLOR)
        data_text.move_to(data_box)

        # Pointer box
        ptr_box = Rectangle(
            width=0.4, height=0.6,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
            fill_color=BG_COLOR,
            fill_opacity=1,
        )
        ptr_box.next_to(data_box, RIGHT, buff=0)

        # Dot in pointer box (null pointer)
        ptr_dot = Text(".", font_size=16, color=MUTED_COLOR)
        ptr_dot.move_to(ptr_box)

        node = VGroup(data_box, data_text, ptr_box, ptr_dot)
        node.move_to([x_pos, 0, 0])
        return node

    def _create_arrow(self, start_x: float, end_x: float) -> Arrow:
        """Create an arrow between nodes."""
        return Arrow(
            start=[start_x + 0.65, 0, 0],
            end=[end_x - 0.65, 0, 0],
            buff=0,
            stroke_color=ACCENT_COLOR,
            stroke_width=2,
            tip_length=0.12,
        )

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Linked List", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        spacing = 1.8
        start_x = -(len(self.values) - 1) * spacing / 2

        nodes = []
        arrows = []

        # Build list step by step
        for i, val in enumerate(self.values):
            x = start_x + i * spacing
            node = self._create_node(val, x)
            nodes.append(node)

            self.play(Create(node), run_time=0.4)

            # Draw arrow from previous node
            if i > 0:
                prev_x = start_x + (i - 1) * spacing
                arrow = self._create_arrow(prev_x, x)
                arrows.append(arrow)
                self.play(Create(arrow), run_time=0.3)

        # Head label
        head_label = Text("HEAD", font_size=16, color=ACCENT_COLOR)
        head_label.next_to(nodes[0], UP, buff=0.3)
        self.play(FadeIn(head_label), run_time=0.3)

        # Null label at end
        null_label = Text("NULL", font_size=14, color=MUTED_COLOR)
        null_label.next_to(nodes[-1], RIGHT, buff=0.3)
        self.play(FadeIn(null_label), run_time=0.3)

        self.wait(2.0)


class LinkedListTraversalScene(LinkedListScene):
    """
    Scene: Animate traversal through a linked list.
    Highlights each node as it's visited.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Linked List Traversal", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        spacing = 1.8
        start_x = -(len(self.values) - 1) * spacing / 2

        nodes = []
        arrows = []

        # Build list
        for i, val in enumerate(self.values):
            x = start_x + i * spacing
            node = self._create_node(val, x)
            nodes.append(node)
            self.add(node)

            if i > 0:
                prev_x = start_x + (i - 1) * spacing
                arrow = self._create_arrow(prev_x, x)
                arrows.append(arrow)
                self.add(arrow)

        # Head label
        head_label = Text("HEAD", font_size=16, color=ACCENT_COLOR)
        head_label.next_to(nodes[0], UP, buff=0.3)
        self.add(head_label)

        null_label = Text("NULL", font_size=14, color=MUTED_COLOR)
        null_label.next_to(nodes[-1], RIGHT, buff=0.3)
        self.add(null_label)

        self.wait(0.5)

        # Traverse with highlighting
        visited_label = None
        for i, node in enumerate(nodes):
            # Highlight current node
            data_box = node[0]  # The data box rectangle
            self.play(
                data_box.animate.set_stroke(color=ACCENT_COLOR, width=3),
                run_time=0.3,
            )

            # Update visited counter - single label that updates
            if visited_label is not None:
                self.remove(visited_label)

            visited_label = Text(
                f"Step {i + 1}/{len(self.values)}: value = {self.values[i]}",
                font_size=18,
                color=ACCENT_COLOR,
            )
            visited_label.to_edge(DOWN, buff=0.6)
            self.add(visited_label)

            self.wait(0.4)

            # Dim highlight (keep stroke but reduce)
            self.play(
                data_box.animate.set_stroke(color=ACCENT_COLOR, width=2),
                run_time=0.1,
            )

        # Final result
        if visited_label is not None:
            self.remove(visited_label)

        final_label = Text(
            f"Traversal complete: {len(self.values)} nodes visited",
            font_size=20,
            color=ACCENT_COLOR,
        )
        final_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(final_label), run_time=0.5)

        self.wait(2.0)


class LinkedListInsertScene(LinkedListScene):
    """
    Scene: Animate insertion into a linked list.
    Shows a new node being inserted at a specific position.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Linked List Insertion", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Start with a shorter list
        self.values = [3, 7, 9]
        insert_value = 5
        insert_pos = 2  # Insert between 7 and 9

        spacing = 1.8
        start_x = -(len(self.values) - 1) * spacing / 2

        nodes = []
        arrows = []

        # Build initial list
        for i, val in enumerate(self.values):
            x = start_x + i * spacing
            node = self._create_node(val, x)
            nodes.append(node)
            self.play(Create(node), run_time=0.4)

            if i > 0:
                prev_x = start_x + (i - 1) * spacing
                arrow = self._create_arrow(prev_x, x)
                arrows.append(arrow)
                self.play(Create(arrow), run_time=0.3)

        head_label = Text("HEAD", font_size=16, color=ACCENT_COLOR)
        head_label.next_to(nodes[0], UP, buff=0.3)
        self.add(head_label)
        self.wait(0.5)

        # Show insertion point
        insert_label = Text(
            f"Insert {insert_value} at position {insert_pos}",
            font_size=18,
            color=ACCENT_COLOR,
        )
        insert_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(insert_label), run_time=0.4)

        # Highlight the arrow that will be broken
        if insert_pos > 0 and insert_pos - 1 < len(arrows):
            self.play(
                arrows[insert_pos - 1].animate.set_stroke(color=TEXT_COLOR, width=3),
                run_time=0.3,
            )

        # Create new node (appears above insertion point)
        new_x = start_x + insert_pos * spacing
        new_node = self._create_node(insert_value, new_x)
        new_node.shift(UP * 1.5)
        self.play(Create(new_node), run_time=0.4)

        # Move new node down into position
        self.play(
            new_node.animate.shift(DOWN * 1.5),
            run_time=0.5,
        )

        # Remove old arrow and draw new arrows
        if insert_pos > 0 and insert_pos - 1 < len(arrows):
            self.play(FadeOut(arrows[insert_pos - 1]), run_time=0.2)

        # Arrow from previous to new node
        prev_x = start_x + (insert_pos - 1) * spacing
        arrow_to_new = self._create_arrow(prev_x, new_x)
        self.play(Create(arrow_to_new), run_time=0.3)

        # Arrow from new to next node
        if insert_pos < len(self.values):
            next_x = start_x + insert_pos * spacing
            # Shift remaining nodes right
            # (simplified: just draw arrow)
            arrow_from_new = self._create_arrow(new_x, start_x + (insert_pos + 1) * spacing)
            self.play(Create(arrow_from_new), run_time=0.3)

        self.wait(2.0)
