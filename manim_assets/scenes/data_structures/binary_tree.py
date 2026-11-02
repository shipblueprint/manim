"""
Binary Tree Scene - Visualize binary tree structures and traversals.
"""

from manim import Scene, Text, VGroup, Circle, Line, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut
from typing import List, Optional, Dict
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class BinaryTreeScene(Scene):
    """
    Scene: Visualize a binary tree with nodes and edges.
    Animates tree construction node by node.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.values: List[Optional[int]] = [8, 4, 12, 2, 6, 10, 14]

    def _calculate_positions(self) -> Dict[int, np.ndarray]:
        """Calculate node positions for a balanced binary tree layout."""
        positions = {}
        if not self.values:
            return positions

        depth = 0
        index = 0
        while index < len(self.values):
            level_size = 2 ** depth
            spacing = 6.0 / (2 ** depth + 1)
            start_x = -3.0 + spacing

            for i in range(level_size):
                if index >= len(self.values):
                    break
                if self.values[index] is not None:
                    x = start_x + i * spacing * 2
                    y = 1.5 - depth * 1.2
                    positions[index] = np.array([x, y, 0])
                index += 1
            depth += 1

        return positions

    def _create_node(self, value: int) -> VGroup:
        """Create a tree node (circle with value text)."""
        circle = Circle(
            radius=0.35,
            stroke_color=MUTED_COLOR,
            stroke_width=2,
            fill_color=BG_COLOR,
            fill_opacity=1,
        )
        text = Text(str(value), font_size=20, color=TEXT_COLOR)
        text.move_to(circle.get_center())
        return VGroup(circle, text)

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Binary Search Tree", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        positions = self._calculate_positions()
        nodes = {}
        edges = []

        # Create edges first (so they appear behind nodes)
        for i, val in enumerate(self.values):
            if val is None or i not in positions:
                continue
            left = 2 * i + 1
            if left < len(self.values) and self.values[left] is not None and left in positions:
                edge = Line(
                    positions[i], positions[left],
                    stroke_color=MUTED_COLOR,
                    stroke_width=1.5,
                )
                edges.append(edge)
            right = 2 * i + 2
            if right < len(self.values) and self.values[right] is not None and right in positions:
                edge = Line(
                    positions[i], positions[right],
                    stroke_color=MUTED_COLOR,
                    stroke_width=1.5,
                )
                edges.append(edge)

        # Animate edges
        for edge in edges:
            self.play(Create(edge), run_time=0.2)

        # Animate nodes appearing one by one
        for i, val in enumerate(self.values):
            if val is not None and i in positions:
                node = self._create_node(val)
                node.move_to(positions[i])
                nodes[i] = node
                self.play(Create(node), run_time=0.3)

        self.wait(2.0)


class BinaryTreeTraversalScene(BinaryTreeScene):
    """
    Scene: Animate tree traversal with node highlighting.
    Shows the traversal order by highlighting nodes one by one.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.traversal_type: str = "inorder"

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        traversal_labels = {
            "inorder": "Inorder: Left -> Root -> Right",
            "preorder": "Preorder: Root -> Left -> Right",
            "postorder": "Postorder: Left -> Right -> Root",
        }

        title = Text(
            traversal_labels.get(self.traversal_type, "Traversal"),
            font_size=22,
            color=TEXT_COLOR,
            font=HEADING_FONT,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        positions = self._calculate_positions()
        nodes = {}

        # Create all nodes and edges
        edges = []
        for i, val in enumerate(self.values):
            if val is None or i not in positions:
                continue
            left = 2 * i + 1
            if left < len(self.values) and self.values[left] is not None and left in positions:
                edges.append(Line(positions[i], positions[left], stroke_color=MUTED_COLOR, stroke_width=1.5))
            right = 2 * i + 2
            if right < len(self.values) and self.values[right] is not None and right in positions:
                edges.append(Line(positions[i], positions[right], stroke_color=MUTED_COLOR, stroke_width=1.5))

        # Show tree with animation
        for edge in edges:
            self.play(Create(edge), run_time=0.15)
        for i, val in enumerate(self.values):
            if val is not None and i in positions:
                node = self._create_node(val)
                node.move_to(positions[i])
                nodes[i] = node
                self.play(Create(node), run_time=0.2)

        self.wait(0.5)

        # Get traversal order
        order = self._get_traversal_order()

        # Animate traversal - highlight each node in order
        visited_parts = []
        visited_label = None

        for step, idx in enumerate(order):
            if idx in nodes:
                node = nodes[idx]
                circle = node[0]  # The circle component

                # Highlight node with strong fill
                self.play(
                    circle.animate.set_stroke(color=ACCENT_COLOR, width=3.5),
                    circle.animate.set_fill(color=ACCENT_COLOR, opacity=0.35),
                    run_time=0.3,
                )

                # Build visited string incrementally
                visited_parts.append(str(self.values[idx]))
                visited_str = " -> ".join(visited_parts)

                # Remove old label
                if visited_label is not None:
                    self.remove(visited_label)

                visited_label = Text(
                    f"Visited: {visited_str}",
                    font_size=18,
                    color=ACCENT_COLOR,
                )
                visited_label.to_edge(DOWN, buff=0.6)
                self.add(visited_label)
                self.wait(0.4)

        # Show final traversal result
        if visited_label is not None:
            self.remove(visited_label)

        final_str = " -> ".join(visited_parts)
        final_label = Text(
            f"Result: {final_str}",
            font_size=20,
            color=ACCENT_COLOR,
        )
        final_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(final_label), run_time=0.5)

        self.wait(2.0)

    def _get_traversal_order(self) -> List[int]:
        """Get the traversal order as list of indices."""
        order = []
        if self.traversal_type == "inorder":
            self._inorder(0, order)
        elif self.traversal_type == "preorder":
            self._preorder(0, order)
        elif self.traversal_type == "postorder":
            self._postorder(0, order)
        return order

    def _inorder(self, idx: int, order: List[int]) -> None:
        if idx < len(self.values) and self.values[idx] is not None:
            self._inorder(2 * idx + 1, order)
            order.append(idx)
            self._inorder(2 * idx + 2, order)

    def _preorder(self, idx: int, order: List[int]) -> None:
        if idx < len(self.values) and self.values[idx] is not None:
            order.append(idx)
            self._preorder(2 * idx + 1, order)
            self._preorder(2 * idx + 2, order)

    def _postorder(self, idx: int, order: List[int]) -> None:
        if idx < len(self.values) and self.values[idx] is not None:
            self._postorder(2 * idx + 1, order)
            self._postorder(2 * idx + 2, order)
            order.append(idx)
