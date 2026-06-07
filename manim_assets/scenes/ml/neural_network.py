"""
Neural Network Scene - Animated activation flow through layers.
"""

from manim import Scene, Text, VGroup, Circle, Line, Rectangle, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class NeuralNetworkScene(Scene):
    """
    Scene: Show a neural network with animated activation flow.
    Data flows from input layer through hidden layers to output.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layer_sizes: list = [4, 6, 5, 3]  # input, hidden1, hidden2, output
        self.layer_labels: list = ["Input", "Hidden 1", "Hidden 2", "Output"]
        self.node_radius: float = 0.18
        self.layer_spacing: float = 2.8
        self.node_spacing: float = 0.7

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Neural Network — Activation Flow", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Compute positions for each layer
        total_width = (len(self.layer_sizes) - 1) * self.layer_spacing
        start_x = -total_width / 2

        all_nodes = []
        all_edges = []

        for layer_idx, size in enumerate(self.layer_sizes):
            x = start_x + layer_idx * self.layer_spacing
            total_height = (size - 1) * self.node_spacing
            start_y = total_height / 2

            layer_nodes = []
            for node_idx in range(size):
                y = start_y - node_idx * self.node_spacing
                circle = Circle(
                    radius=self.node_radius,
                    stroke_color=MUTED_COLOR,
                    stroke_width=1.5,
                    fill_color=BG_COLOR,
                    fill_opacity=1.0,
                )
                circle.move_to([x, y, 0])
                layer_nodes.append(circle)

            all_nodes.append(layer_nodes)

            # Layer label
            label = Text(self.layer_labels[layer_idx], font_size=14, color=MUTED_COLOR)
            label.next_to(VGroup(*layer_nodes), DOWN, buff=0.4)
            self.add(label)

        # Draw all edges (connections between layers)
        for layer_idx in range(len(self.layer_sizes) - 1):
            for src in all_nodes[layer_idx]:
                for dst in all_nodes[layer_idx + 1]:
                    edge = Line(
                        start=src.get_right(),
                        end=dst.get_left(),
                        stroke_color=MUTED_COLOR,
                        stroke_width=0.5,
                        stroke_opacity=0.3,
                    )
                    all_edges.append((layer_idx, edge))
                    self.add(edge)

        # Draw all nodes on top of edges
        for layer in all_nodes:
            for node in layer:
                self.add(node)

        self.wait(0.5)

        # Animate activation flow layer by layer
        for layer_idx in range(len(self.layer_sizes)):
            # Light up current layer nodes
            node_anims = []
            for node in all_nodes[layer_idx]:
                node_anims.append(
                    node.animate.set_fill(ACCENT_COLOR, opacity=0.6)
                    .set_stroke(color=ACCENT_COLOR, width=2.5)
                )
            self.play(*node_anims, run_time=0.4)

            # Light up edges going to next layer
            if layer_idx < len(self.layer_sizes) - 1:
                edge_anims = []
                for edge_layer, edge in all_edges:
                    if edge_layer == layer_idx:
                        edge_anims.append(
                            edge.animate.set_stroke(ACCENT_COLOR, width=1.5, opacity=0.7)
                        )
                self.play(*edge_anims, run_time=0.3)

            # Dim previous layer (except keep it slightly visible)
            if layer_idx > 0:
                dim_anims = []
                for node in all_nodes[layer_idx - 1]:
                    dim_anims.append(
                        node.animate.set_fill(ACCENT_COLOR, opacity=0.2)
                        .set_stroke(color=MUTED_COLOR, width=1.5)
                    )
                for edge_layer, edge in all_edges:
                    if edge_layer == layer_idx - 1:
                        dim_anims.append(
                            edge.animate.set_stroke(MUTED_COLOR, width=0.5, opacity=0.2)
                        )
                self.play(*dim_anims, run_time=0.2)

        # Final: light up output layer
        self.wait(0.5)

        # Show activation function labels
        act_label = Text("ReLU / Sigmoid activations", font_size=16, color=ACCENT_COLOR)
        act_label.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(act_label), run_time=0.5)

        self.wait(2.0)
