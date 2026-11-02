"""
Graph Scene - Visualize graph data structures and traversals.
"""

from manim import Scene, Text, VGroup, Circle, Line, Dot, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut
from typing import List, Dict, Tuple
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class GraphScene(Scene):
    """
    Scene: Visualize an undirected graph with nodes and edges.
    Animates graph construction.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adjacency = {
            0: [1, 3],
            1: [0, 2, 4],
            2: [1, 5],
            3: [0, 4],
            4: [1, 3, 5],
            5: [2, 4],
        }
        self.positions = {
            0: [-2.5, 1.5, 0],
            1: [0, 1.5, 0],
            2: [2.5, 1.5, 0],
            3: [-2.5, -1, 0],
            4: [0, -1, 0],
            5: [2.5, -1, 0],
        }

    def _create_node(self, value: int, pos) -> VGroup:
        """Create a graph node."""
        circle = Circle(
            radius=0.4,
            stroke_color=MUTED_COLOR,
            stroke_width=2,
            fill_color=BG_COLOR,
            fill_opacity=1,
        )
        circle.move_to(pos)
        text = Text(str(value), font_size=20, color=TEXT_COLOR)
        text.move_to(pos)
        return VGroup(circle, text)

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Graph", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Draw edges first
        edges_drawn = set()
        for node, neighbors in self.adjacency.items():
            for neighbor in neighbors:
                edge_key = tuple(sorted([node, neighbor]))
                if edge_key not in edges_drawn:
                    edge = Line(
                        self.positions[node],
                        self.positions[neighbor],
                        stroke_color=MUTED_COLOR,
                        stroke_width=1.5,
                    )
                    self.play(Create(edge), run_time=0.2)
                    edges_drawn.add(edge_key)

        # Draw nodes
        for node_id, pos in self.positions.items():
            node = self._create_node(node_id, pos)
            self.play(Create(node), run_time=0.3)

        self.wait(2.0)


class GraphTraversalScene(GraphScene):
    """
    Scene: Animate BFS/DFS traversal of a graph.
    Highlights visited nodes with step numbers that don't overlap.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.traversal_type: str = "bfs"
        self.start_node: int = 0

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text(
            f"{'BFS' if self.traversal_type == 'bfs' else 'DFS'} Traversal",
            font_size=24,
            color=TEXT_COLOR,
            font=HEADING_FONT,
        )
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Draw all edges
        edges_drawn = set()
        edge_mobjects = {}
        for node, neighbors in self.adjacency.items():
            for neighbor in neighbors:
                edge_key = tuple(sorted([node, neighbor]))
                if edge_key not in edges_drawn:
                    edge = Line(
                        self.positions[node],
                        self.positions[neighbor],
                        stroke_color=MUTED_COLOR,
                        stroke_width=1.5,
                    )
                    self.add(edge)
                    edge_mobjects[edge_key] = edge
                    edges_drawn.add(edge_key)

        # Draw all nodes
        nodes = {}
        for node_id, pos in self.positions.items():
            node = self._create_node(node_id, pos)
            self.add(node)
            nodes[node_id] = node

        self.wait(0.5)

        # Get traversal order
        order = self._bfs_order() if self.traversal_type == "bfs" else self._dfs_order()

        # Animate traversal with step numbers positioned to avoid overlap
        visited_label = None
        for step, node_id in enumerate(order):
            node = nodes[node_id]
            circle = node[0]

            # Highlight node
            self.play(
                circle.animate.set_stroke(color=ACCENT_COLOR, width=3.5),
                circle.animate.set_fill(color=ACCENT_COLOR, opacity=0.3),
                run_time=0.3,
            )

            # Step number - position above the node with offset to avoid overlap
            step_label = Text(
                str(step + 1),
                font_size=14,
                color=ACCENT_COLOR,
            )
            step_label.next_to(circle, UP, buff=0.15)
            self.add(step_label)

            # Update visited list at bottom
            if visited_label is not None:
                self.remove(visited_label)

            visited_parts = [str(order[i]) for i in range(step + 1)]
            visited_label = Text(
                f"Visited: {', '.join(visited_parts)}",
                font_size=18,
                color=ACCENT_COLOR,
            )
            visited_label.to_edge(DOWN, buff=0.6)
            self.add(visited_label)

            self.wait(0.4)

        # Final result
        if visited_label is not None:
            self.remove(visited_label)

        final_parts = [str(n) for n in order]
        final_label = Text(
            f"Order: {', '.join(final_parts)}",
            font_size=20,
            color=ACCENT_COLOR,
        )
        final_label.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(final_label), run_time=0.5)

        self.wait(2.0)

    def _bfs_order(self) -> List[int]:
        """BFS traversal order."""
        from collections import deque
        visited = set()
        queue = deque([self.start_node])
        order = []

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            for neighbor in sorted(self.adjacency.get(node, [])):
                if neighbor not in visited:
                    queue.append(neighbor)

        return order

    def _dfs_order(self) -> List[int]:
        """DFS traversal order."""
        visited = set()
        order = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            order.append(node)
            for neighbor in sorted(self.adjacency.get(node, [])):
                dfs(neighbor)

        dfs(self.start_node)
        return order
