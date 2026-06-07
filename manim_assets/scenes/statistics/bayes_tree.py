"""
Bayes Theorem Probability Tree Scene.
"""

from manim import Scene, Text, VGroup, Line, Circle, UP, DOWN, LEFT, RIGHT, Create, FadeIn
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class BayesTreeScene(Scene):
    """
    Scene: Visualize Bayes' theorem as a probability tree.
    P(A|B) = P(B|A) * P(A) / P(B)

    Example: Disease test
    - P(Disease) = 0.01 (prior)
    - P(Positive|Disease) = 0.95 (sensitivity)
    - P(Positive|No Disease) = 0.05 (false positive rate)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.p_disease: float = 0.01
        self.p_pos_given_disease: float = 0.95
        self.p_pos_given_no_disease: float = 0.05

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Bayes' Theorem — Probability Tree", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Tree layout positions
        root_x = -5.0
        level1_x = -1.5
        level2_x = 3.0
        root_y = 0.0

        # Level 1: Disease / No Disease
        disease_y = 1.5
        no_disease_y = -1.5

        # Level 2: Test results
        # Disease -> Positive, Negative
        dp_y = 2.5
        dn_y = 0.5
        # No Disease -> Positive, Negative
        ndp_y = -0.5
        ndn_y = -2.5

        # Root node
        root_circle = Circle(radius=0.2, stroke_color=MUTED_COLOR, stroke_width=1.5)
        root_circle.move_to([root_x, root_y, 0])
        root_label = Text("Start", font_size=12, color=MUTED_COLOR)
        root_label.next_to(root_circle, UP, buff=0.15)

        self.play(Create(root_circle), FadeIn(root_label), run_time=0.4)

        # Level 1 nodes
        disease_circle = Circle(radius=0.25, stroke_color=ACCENT_COLOR, stroke_width=2)
        disease_circle.move_to([level1_x, disease_y, 0])
        disease_label = Text("Disease", font_size=14, color=ACCENT_COLOR)
        disease_label.next_to(disease_circle, UP, buff=0.15)

        no_disease_circle = Circle(radius=0.25, stroke_color=MUTED_COLOR, stroke_width=2)
        no_disease_circle.move_to([level1_x, no_disease_y, 0])
        no_disease_label = Text("No Disease", font_size=14, color=MUTED_COLOR)
        no_disease_label.next_to(no_disease_circle, DOWN, buff=0.15)

        # Level 1 lines
        line_d = Line(
            [root_x + 0.2, root_y, 0],
            [level1_x - 0.25, disease_y, 0],
            stroke_color=ACCENT_COLOR, stroke_width=2,
        )
        line_nd = Line(
            [root_x + 0.2, root_y, 0],
            [level1_x - 0.25, no_disease_y, 0],
            stroke_color=MUTED_COLOR, stroke_width=2,
        )

        # Level 1 probability labels
        p_d_label = Text(f"P(D)={self.p_disease}", font_size=13, color=ACCENT_COLOR)
        p_d_label.move_to([(root_x + level1_x) / 2 - 0.3, (root_y + disease_y) / 2 + 0.3, 0])

        p_nd_label = Text(f"P(~D)={1 - self.p_disease:.2f}", font_size=13, color=MUTED_COLOR)
        p_nd_label.move_to([(root_x + level1_x) / 2 - 0.3, (root_y + no_disease_y) / 2 - 0.3, 0])

        self.play(
            Create(line_d), Create(line_nd),
            Create(disease_circle), Create(no_disease_circle),
            FadeIn(disease_label), FadeIn(no_disease_label),
            FadeIn(p_d_label), FadeIn(p_nd_label),
            run_time=1.0,
        )

        # Level 2 nodes
        # Disease -> Positive
        dp_circle = Circle(radius=0.2, stroke_color=ACCENT_COLOR, stroke_width=2)
        dp_circle.move_to([level2_x, dp_y, 0])
        dp_label = Text("+", font_size=16, color=ACCENT_COLOR)
        dp_label.move_to(dp_circle.get_center())

        # Disease -> Negative
        dn_circle = Circle(radius=0.2, stroke_color=MUTED_COLOR, stroke_width=1.5)
        dn_circle.move_to([level2_x, dn_y, 0])
        dn_label = Text("-", font_size=16, color=MUTED_COLOR)
        dn_label.move_to(dn_circle.get_center())

        # No Disease -> Positive
        ndp_circle = Circle(radius=0.2, stroke_color=ACCENT_COLOR, stroke_width=2)
        ndp_circle.move_to([level2_x, ndp_y, 0])
        ndp_label = Text("+", font_size=16, color=ACCENT_COLOR)
        ndp_label.move_to(ndp_circle.get_center())

        # No Disease -> Negative
        ndn_circle = Circle(radius=0.2, stroke_color=MUTED_COLOR, stroke_width=1.5)
        ndn_circle.move_to([level2_x, ndn_y, 0])
        ndn_label = Text("-", font_size=16, color=MUTED_COLOR)
        ndn_label.move_to(ndn_circle.get_center())

        # Level 2 lines
        line_dp = Line(
            [level1_x + 0.25, disease_y, 0],
            [level2_x - 0.2, dp_y, 0],
            stroke_color=ACCENT_COLOR, stroke_width=2,
        )
        line_dn = Line(
            [level1_x + 0.25, disease_y, 0],
            [level2_x - 0.2, dn_y, 0],
            stroke_color=MUTED_COLOR, stroke_width=1.5,
        )
        line_ndp = Line(
            [level1_x + 0.25, no_disease_y, 0],
            [level2_x - 0.2, ndp_y, 0],
            stroke_color=ACCENT_COLOR, stroke_width=2,
        )
        line_ndn = Line(
            [level1_x + 0.25, no_disease_y, 0],
            [level2_x - 0.2, ndn_y, 0],
            stroke_color=MUTED_COLOR, stroke_width=1.5,
        )

        # Level 2 probability labels
        p_pos_d = Text(f"P(+|D)={self.p_pos_given_disease}", font_size=12, color=ACCENT_COLOR)
        p_pos_d.move_to([(level1_x + level2_x) / 2, (disease_y + dp_y) / 2 + 0.2, 0])

        p_neg_d = Text(f"P(-|D)={1 - self.p_pos_given_disease:.2f}", font_size=12, color=MUTED_COLOR)
        p_neg_d.move_to([(level1_x + level2_x) / 2, (disease_y + dn_y) / 2 - 0.2, 0])

        p_pos_nd = Text(f"P(+|~D)={self.p_pos_given_no_disease}", font_size=12, color=ACCENT_COLOR)
        p_pos_nd.move_to([(level1_x + level2_x) / 2, (no_disease_y + ndp_y) / 2 + 0.2, 0])

        p_neg_nd = Text(f"P(-|~D)={1 - self.p_pos_given_no_disease:.2f}", font_size=12, color=MUTED_COLOR)
        p_neg_nd.move_to([(level1_x + level2_x) / 2, (no_disease_y + ndn_y) / 2 - 0.2, 0])

        self.play(
            Create(line_dp), Create(line_dn), Create(line_ndp), Create(line_ndn),
            Create(dp_circle), Create(dn_circle), Create(ndp_circle), Create(ndn_circle),
            FadeIn(dp_label), FadeIn(dn_label), FadeIn(ndp_label), FadeIn(ndn_label),
            FadeIn(p_pos_d), FadeIn(p_neg_d), FadeIn(p_pos_nd), FadeIn(p_neg_nd),
            run_time=1.5,
        )

        # Compute Bayes' theorem result
        p_pos = (self.p_pos_given_disease * self.p_disease
                 + self.p_pos_given_no_disease * (1 - self.p_disease))
        p_disease_given_pos = (self.p_pos_given_disease * self.p_disease) / p_pos

        # Show the Bayes formula and result
        formula = Text(
            f"P(D|+) = P(+|D) * P(D) / P(+)",
            font_size=16, color=TEXT_COLOR,
        )
        formula.to_edge(DOWN, buff=1.2)

        result = Text(
            f"P(D|+) = {self.p_pos_given_disease} x {self.p_disease} / {p_pos:.4f} = {p_disease_given_pos:.4f}",
            font_size=16, color=ACCENT_COLOR,
        )
        result.next_to(formula, DOWN, buff=0.2)

        insight = Text(
            f"Only {p_disease_given_pos*100:.1f}% chance of disease given positive test!",
            font_size=16, color=TEXT_COLOR,
        )
        insight.next_to(result, DOWN, buff=0.2)

        self.play(FadeIn(formula), run_time=0.5)
        self.play(FadeIn(result), run_time=0.5)
        self.play(FadeIn(insight), run_time=0.5)

        self.wait(2.0)
