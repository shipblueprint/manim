"""
K-Means Clustering Scene - Convergence animation.
"""

from manim import Scene, Text, VGroup, Dot, Circle, UP, DOWN, Create, FadeIn
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class KMeansScene(Scene):
    """
    Scene: Show K-means clustering convergence.
    Points are assigned to nearest centroid, then centroids update.
    Repeats until convergence.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        np.random.seed(5)
        self.k: int = 3
        self.max_iters: int = 5
        # Generate 3 clusters of data
        self.points = np.vstack([
            np.random.normal([-2, 2], 0.6, (15, 2)),
            np.random.normal([2, 2], 0.6, (15, 2)),
            np.random.normal([0, -1.5], 0.6, (15, 2)),
        ])
        # Initial centroids (deliberately bad starting positions)
        self.initial_centroids = np.array([[-1, -1], [1, -1], [0, 3]])

    def _assign(self, points: np.ndarray, centroids: np.ndarray) -> np.ndarray:
        """Assign each point to nearest centroid."""
        distances = np.zeros((len(points), len(centroids)))
        for i, c in enumerate(centroids):
            distances[:, i] = np.linalg.norm(points - c, axis=1)
        return np.argmin(distances, axis=1)

    def _update_centroids(self, points: np.ndarray, labels: np.ndarray, k: int) -> np.ndarray:
        """Compute new centroids as mean of assigned points."""
        new_centroids = np.zeros((k, 2))
        for i in range(k):
            cluster_points = points[labels == i]
            if len(cluster_points) > 0:
                new_centroids[i] = cluster_points.mean(axis=0)
            else:
                new_centroids[i] = centroids[i]  # keep old centroid
        return new_centroids

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("K-Means Clustering", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # Cluster colors (for k=3) — all from brand palette
        cluster_colors = [ACCENT_COLOR, TEXT_COLOR, MUTED_COLOR]

        # Coordinate mapping: data range [-4,4] -> screen
        def data_to_screen(x, y):
            return [x * 0.9, y * 0.9 - 0.3, 0]

        # Show all points initially (gray)
        point_dots = []
        for pt in self.points:
            dot = Dot(
                point=data_to_screen(pt[0], pt[1]),
                radius=0.06,
                color=MUTED_COLOR,
            )
            point_dots.append(dot)
            self.add(dot)

        self.wait(0.5)

        # Show initial centroids
        centroids = self.initial_centroids.copy()
        centroid_markers = []
        for i, c in enumerate(centroids):
            marker = Circle(
                radius=0.25,
                stroke_color=cluster_colors[i],
                stroke_width=2.5,
                fill_color=cluster_colors[i],
                fill_opacity=0.15,
            )
            marker.move_to(data_to_screen(c[0], c[1]))
            centroid_markers.append(marker)
            self.add(marker)

        iter_label = Text("Iteration 0", font_size=16, color=MUTED_COLOR)
        iter_label.to_edge(DOWN, buff=0.5)
        self.add(iter_label)

        # K-means iterations
        for iteration in range(self.max_iters):
            # Assign step
            labels = self._assign(self.points, centroids)

            # Color points by cluster
            color_anims = []
            for idx, (dot, label) in enumerate(zip(point_dots, labels)):
                color_anims.append(dot.animate.set_color(cluster_colors[label]))
            self.play(*color_anims, run_time=0.6)

            # Update centroids
            new_centroids = self._update_centroids(self.points, labels, self.k)

            # Animate centroid movement
            move_anims = []
            for i in range(self.k):
                target = data_to_screen(new_centroids[i][0], new_centroids[i][1])
                move_anims.append(centroid_markers[i].animate.move_to(target))
            self.play(*move_anims, run_time=0.6)

            # Check convergence
            if np.allclose(centroids, new_centroids, atol=0.01):
                converged_text = Text("Converged!", font_size=18, color=ACCENT_COLOR)
                converged_text.next_to(iter_label, UP, buff=0.2)
                self.play(FadeIn(converged_text), run_time=0.4)
                break

            centroids = new_centroids

            # Update iteration label
            new_iter_label = Text(f"Iteration {iteration + 1}", font_size=16, color=MUTED_COLOR)
            new_iter_label.to_edge(DOWN, buff=0.5)
            self.play(
                iter_label.animate.become(new_iter_label),
                run_time=0.3,
            )
            iter_label = new_iter_label

        # Final cluster labels
        for i in range(self.k):
            cx, cy = centroids[i]
            label = Text(f"C{i+1}", font_size=14, color=cluster_colors[i])
            label.move_to(data_to_screen(cx, cy + 0.6))
            self.add(label)

        self.wait(2.0)
