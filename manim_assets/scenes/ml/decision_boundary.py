"""
Decision Boundary Scene - Separating 2D point clusters.
"""

from manim import Scene, Axes, Text, VGroup, Dot, Line, UP, DOWN, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class DecisionBoundaryScene(Scene):
    """
    Scene: Show two clusters of 2D points and animate a
    decision boundary line separating them.
    Uses logistic regression decision boundary.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(10)
        # Class 0: centered at (-1.5, -1)
        self.class0_x = np.random.normal(-1.5, 0.7, 20)
        self.class0_y = np.random.normal(-1.0, 0.7, 20)
        # Class 1: centered at (1.5, 1)
        self.class1_x = np.random.normal(1.5, 0.7, 20)
        self.class1_y = np.random.normal(1.0, 0.7, 20)

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Decision Boundary", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            x_length=8,
            y_length=8,
            axis_config={
                "stroke_color": MUTED_COLOR,
                "stroke_width": 1,
                "include_numbers": True,
                "font_size": 16,
                "decimal_number_config": {"color": MUTED_COLOR, "num_decimal_places": 0},
            },
            tips=False,
        )
        axes.shift(DOWN * 0.2)

        self.play(Create(axes), run_time=0.8)

        # Plot class 0 points
        class0_dots = VGroup()
        for x, y in zip(self.class0_x, self.class0_y):
            dot = Dot(point=axes.c2p(x, y), radius=0.07, color=ACCENT_COLOR)
            class0_dots.add(dot)

        # Plot class 1 points
        class1_dots = VGroup()
        for x, y in zip(self.class1_x, self.class1_y):
            dot = Dot(point=axes.c2p(x, y), radius=0.07, color=TEXT_COLOR)
            class1_dots.add(dot)

        self.play(FadeIn(class0_dots), FadeIn(class1_dots), run_time=1.0)

        # Compute decision boundary using logistic regression (closed-form for 2D)
        # Features: [1, x, y], labels: 0 or 1
        X = np.column_stack([
            np.ones(len(self.class0_x) + len(self.class1_x)),
            np.concatenate([self.class0_x, self.class1_x]),
            np.concatenate([self.class0_y, self.class1_y]),
        ])
        y = np.concatenate([np.zeros(len(self.class0_x)), np.ones(len(self.class1_x))])

        # Simple gradient descent for logistic regression
        weights = np.zeros(3)
        lr = 0.1
        for _ in range(200):
            z = X @ weights
            predictions = 1 / (1 + np.exp(-z))
            gradient = X.T @ (predictions - y) / len(y)
            weights -= lr * gradient

        # Decision boundary: w0 + w1*x + w2*y = 0 => y = -(w0 + w1*x) / w2
        w0, w1, w2 = weights

        # Draw boundary line
        x_vals = np.linspace(-4, 4, 100)
        y_vals = -(w0 + w1 * x_vals) / w2

        # Clip to visible range
        visible_points = []
        for xv, yv in zip(x_vals, y_vals):
            if -4 <= yv <= 4:
                visible_points.append(axes.c2p(xv, yv))

        if len(visible_points) > 1:
            from manim import VMobject
            boundary = VMobject(
                stroke_color=TEXT_COLOR,
                stroke_width=2.5,
            )
            boundary.set_points_as_corners(visible_points)
            self.play(Create(boundary), run_time=1.5)

        # Labels
        class0_label = Text("Class 0", font_size=14, color=ACCENT_COLOR)
        class0_label.move_to(axes.c2p(-2.5, 3))
        class1_label = Text("Class 1", font_size=14, color=TEXT_COLOR)
        class1_label.move_to(axes.c2p(2.5, -3))

        self.play(FadeIn(class0_label), FadeIn(class1_label), run_time=0.4)

        # Show boundary equation
        eq_text = Text(
            f"Boundary: {w1:.2f}x + {w2:.2f}y + {w0:.2f} = 0",
            font_size=16, color=MUTED_COLOR,
        )
        eq_text.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(eq_text), run_time=0.4)

        self.wait(2.0)
