"""
Hash Table Scene - With collision resolution (chaining).
"""

from manim import Scene, Text, VGroup, Rectangle, Line, Arrow, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class HashTableScene(Scene):
    """
    Scene: Visualize a hash table with chaining for collision resolution.
    Insert keys and show how they hash to buckets, with linked lists for collisions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_size: int = 7
        self.keys: list = [15, 22, 8, 29, 4, 36, 13]
        self.cell_width: float = 1.2
        self.cell_height: float = 0.55

    def _hash(self, key: int) -> int:
        """Simple hash function: key % table_size."""
        return key % self.table_size

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Hash Table — Chaining", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Draw hash table (array of buckets)
        start_x = -3.5
        start_y = 2.0

        buckets = []
        bucket_labels = []
        for i in range(self.table_size):
            rect = Rectangle(
                width=self.cell_width,
                height=self.cell_height,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=BG_COLOR,
                fill_opacity=1.0,
            )
            y = start_y - i * (self.cell_height + 0.08)
            rect.move_to([start_x, y, 0])
            buckets.append(rect)

            # Index label
            idx_label = Text(str(i), font_size=14, color=MUTED_COLOR)
            idx_label.next_to(rect, LEFT, buff=0.2)
            bucket_labels.append(idx_label)

        self.play(
            Create(VGroup(*buckets)),
            FadeIn(VGroup(*bucket_labels)),
            run_time=0.8,
        )

        # Show hash function
        hash_func_text = Text("h(k) = k mod 7", font_size=16, color=ACCENT_COLOR)
        hash_func_text.to_edge(UP, buff=1.2)
        self.play(FadeIn(hash_func_text), run_time=0.3)

        # Insert keys one by one
        chain_nodes = {}  # bucket_index -> list of (rect, label) tuples

        for key in self.keys:
            bucket_idx = self._hash(key)

            # Show key being hashed
            key_text = Text(f"Insert {key} -> h({key}) = {bucket_idx}", font_size=14, color=TEXT_COLOR)
            key_text.to_edge(DOWN, buff=0.5)
            self.add(key_text)

            # Highlight the target bucket
            self.play(
                buckets[bucket_idx].animate.set_stroke(color=ACCENT_COLOR, width=2.5),
                run_time=0.3,
            )

            # Create chain node
            node_rect = Rectangle(
                width=self.cell_width * 0.85,
                height=self.cell_height * 0.8,
                stroke_color=ACCENT_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=0.15,
            )
            node_label = Text(str(key), font_size=13, color=TEXT_COLOR)

            if bucket_idx not in chain_nodes:
                chain_nodes[bucket_idx] = []
                # First node: place inside bucket
                node_rect.move_to(buckets[bucket_idx].get_center())
                node_label.move_to(node_rect.get_center())
                chain_nodes[bucket_idx].append((node_rect, node_label))
            else:
                # Collision! Add to chain
                chain_nodes[bucket_idx].append((node_rect, node_label))
                # Position chain nodes
                self._reposition_chain(bucket_idx, buckets[bucket_idx], chain_nodes[bucket_idx])

            self.play(Create(node_rect), FadeIn(node_label), run_time=0.4)

            # Reset bucket highlight
            self.play(
                buckets[bucket_idx].animate.set_stroke(color=MUTED_COLOR, width=1.5),
                run_time=0.2,
            )

            self.remove(key_text)

        # Show collision info
        collisions = sum(1 for v in chain_nodes.values() if len(v) > 1)
        info = Text(
            f"Collisions: {collisions} bucket(s) with chaining",
            font_size=16, color=ACCENT_COLOR,
        )
        info.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(info), run_time=0.5)

        self.wait(2.0)

    def _reposition_chain(self, bucket_idx: int, bucket_rect: Rectangle, nodes: list) -> None:
        """Reposition all chain nodes for a bucket (horizontal chain to the right)."""
        for i, (rect, label) in enumerate(nodes):
            if i == 0:
                # First node stays in bucket
                rect.move_to(bucket_rect.get_center())
                label.move_to(rect.get_center())
            else:
                # Subsequent nodes chain to the right
                prev_rect = nodes[i - 1][0]
                x = prev_rect.get_right()[0] + self.cell_width * 0.85 / 2 + 0.15 + self.cell_width * 0.85 / 2
                y = prev_rect.get_center()[1]
                rect.move_to([x, y, 0])
                label.move_to(rect.get_center())
