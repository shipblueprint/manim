"""
Eigenvalue and Eigenvector Visualization Scene.
"""

from manim import Scene, Text, Arrow, VGroup, Dot, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut, Transform
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class EigenScene(Scene):
    """
    Scene: Visualize eigenvectors of a 2x2 matrix.
    Shows how eigenvectors stay on their span under transformation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.matrix = np.array([[2, 1], [1, 2]])

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        m = self.matrix

        # Title and matrix display
        title = Text("Eigenvectors", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)

        mat_text = Text(
            f"A = [[{m[0,0]}, {m[0,1]}], [{m[1,0]}, {m[1,1]}]]",
            font_size=20,
            color=MUTED_COLOR,
        )
        mat_text.next_to(title, DOWN, buff=0.3)

        self.play(FadeIn(title), FadeIn(mat_text), run_time=0.5)

        # Compute eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(m)

        # Draw original eigenvectors
        origin = np.array([0, 0, 0])

        arrows_original = VGroup()
        labels_original = VGroup()

        for i in range(2):
            ev = eigenvectors[:, i]
            color = ACCENT_COLOR if i == 0 else TEXT_COLOR
            arrow = Arrow(
                start=origin,
                end=[ev[0], ev[1], 0],
                buff=0,
                stroke_color=color,
                stroke_width=3,
                tip_length=0.15,
            )
            # Scale up for visibility
            arrow.scale(1.5)
            arrows_original.add(arrow)

            label = Text(
                f"v{i+1} (lambda={eigenvalues[i]:.1f})",
                font_size=16,
                color=color,
            )
            label.next_to(arrow.get_end(), RIGHT if i == 0 else LEFT, buff=0.15)
            labels_original.add(label)

        self.play(
            Create(arrows_original[0]), Create(arrows_original[1]),
            FadeIn(labels_original[0]), FadeIn(labels_original[1]),
            run_time=1.0,
        )
        self.wait(0.5)

        # Show transformed eigenvectors
        arrows_transformed = VGroup()
        labels_transformed = VGroup()

        for i in range(2):
            ev = eigenvectors[:, i]
            transformed = m @ ev
            color = ACCENT_COLOR if i == 0 else TEXT_COLOR
            arrow = Arrow(
                start=origin,
                end=[transformed[0], transformed[1], 0],
                buff=0,
                stroke_color=color,
                stroke_width=3,
                tip_length=0.15,
            )
            arrow.scale(1.5)
            arrows_transformed.add(arrow)

            label = Text(
                f"Av{i+1} = {eigenvalues[i]:.1f} * v{i+1}",
                font_size=16,
                color=color,
            )
            label.next_to(arrow.get_end(), RIGHT if i == 0 else LEFT, buff=0.15)
            labels_transformed.add(label)

        # Animate transformation
        self.play(
            Transform(arrows_original[0], arrows_transformed[0]),
            Transform(arrows_original[1], arrows_transformed[1]),
            run_time=1.5,
        )

        # Update labels
        self.play(
            FadeOut(labels_original[0]), FadeOut(labels_original[1]),
            FadeIn(labels_transformed[0]), FadeIn(labels_transformed[1]),
            run_time=0.5,
        )

        # Key insight
        insight = Text(
            "Eigenvectors stay on their span",
            font_size=20,
            color=ACCENT_COLOR,
        )
        insight.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(insight), run_time=0.5)

        self.wait(2.0)
