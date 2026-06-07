"""
3D Solids Scene - Visualize 3D geometric solids.
"""

from manim import Scene, Text, VGroup, UP, DOWN, LEFT, RIGHT, Create, FadeIn, Rotate
import numpy as np

from manim_assets.config.colors import BG_COLOR, TEXT_COLOR, ACCENT_COLOR, MUTED_COLOR


class Solids3DScene(Scene):
    """
    Scene: Show 3D solids with rotation animation.
    Uses isometric projection for 3D appearance.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("3D Solids", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        # Isometric projection helper
        proj = lambda v: np.array([v[0] - v[2] * 0.5, v[1] + v[2] * 0.5, 0])

        # Create a cube using projected vertices
        from manim import Polygon, Line

        # Cube vertices
        cube_verts = [
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
        ]
        projected = [proj(np.array(v)) for v in cube_verts]

        # Cube faces (back faces first for proper overlap)
        faces = [
            # Back face
            [0, 1, 5, 4],  # bottom-back
            [0, 3, 7, 4],  # left-back
            [4, 5, 6, 7],  # back
            # Front faces
            [0, 1, 2, 3],  # front
            [1, 2, 6, 5],  # right
            [3, 2, 6, 7],  # top
        ]

        face_colors = [
            (MUTED_COLOR, 0.05),
            (MUTED_COLOR, 0.05),
            (MUTED_COLOR, 0.08),
            (ACCENT_COLOR, 0.1),
            (ACCENT_COLOR, 0.08),
            (ACCENT_COLOR, 0.12),
        ]

        cube = VGroup()
        for i, face_idx in enumerate(faces):
            face_pts = [projected[j] for j in face_idx]
            color, opacity = face_colors[i]
            face = Polygon(
                *face_pts,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=color,
                fill_opacity=opacity,
            )
            cube.add(face)

        cube.scale(1.5)
        cube.shift(LEFT * 3)

        # Create a tetrahedron
        tet_verts = [
            [0, 0, 0], [1, 0, 0], [0.5, 0, 0.87], [0.5, 0.82, 0.29],
        ]
        tet_proj = [proj(np.array(v)) for v in tet_verts]

        tet_faces = [
            [0, 1, 2],  # base
            [0, 1, 3],  # front
            [1, 2, 3],  # right
            [0, 2, 3],  # left
        ]

        tet = VGroup()
        for i, face_idx in enumerate(tet_faces):
            face_pts = [tet_proj[j] for j in face_idx]
            opacity = 0.08 if i == 0 else 0.12
            face = Polygon(
                *face_pts,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=opacity,
            )
            tet.add(face)

        tet.scale(1.5)
        tet.shift(RIGHT * 3)

        # Labels
        cube_label = Text("Cube", font_size=18, color=TEXT_COLOR)
        cube_label.next_to(cube, DOWN, buff=0.3)
        tet_label = Text("Tetrahedron", font_size=18, color=TEXT_COLOR)
        tet_label.next_to(tet, DOWN, buff=0.3)

        # Animate
        self.play(Create(cube), FadeIn(cube_label), run_time=1.0)
        self.play(Create(tet), FadeIn(tet_label), run_time=1.0)

        # Rotate both
        self.play(
            Rotate(cube, angle=np.radians(30)),
            Rotate(tet, angle=np.radians(30)),
            run_time=1.0,
        )

        self.wait(2.0)


class PolyhedronScene(Scene):
    """
    Scene: Show Platonic solids with rotation.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Platonic Solids", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        from manim import RegularPolygon, Polygon

        # Create octahedron (2 projected views)
        proj = lambda v: np.array([v[0] - v[2] * 0.5, v[1] + v[2] * 0.5, 0])

        # Octahedron vertices
        oct_verts = [
            [0, 1, 0], [1, 0, 0], [0, 0, 1],
            [-1, 0, 0], [0, 0, -1], [0, -1, 0],
        ]
        oct_proj = [proj(np.array(v)) for v in oct_verts]

        # Build visible faces
        octahedron = VGroup()
        face_indices = [
            [0, 1, 2], [0, 2, 3], [0, 3, 4], [0, 4, 1],
            [5, 1, 2], [5, 2, 3], [5, 3, 4], [5, 4, 1],
        ]

        for i, face_idx in enumerate(face_indices):
            face_pts = [oct_proj[j] for j in face_idx]
            opacity = 0.1 if i < 4 else 0.15
            face = Polygon(
                *face_pts,
                stroke_color=MUTED_COLOR,
                stroke_width=1.5,
                fill_color=ACCENT_COLOR,
                fill_opacity=opacity,
            )
            octahedron.add(face)

        octahedron.scale(1.8)

        label = Text("Octahedron", font_size=18, color=TEXT_COLOR)
        label.next_to(octahedron, DOWN, buff=0.3)

        self.play(Create(octahedron), FadeIn(label), run_time=1.2)

        # Rotate
        self.play(
            Rotate(octahedron, angle=np.radians(45)),
            run_time=1.5,
        )

        # Show face/edge/vertex count
        info = Text("8 faces, 12 edges, 6 vertices", font_size=18, color=ACCENT_COLOR)
        info.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(info), run_time=0.5)

        self.wait(2.0)


class PlatonicSolidsScene(Scene):
    """
    Scene: Show all five Platonic solids with names and properties.
    """

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("The 5 Platonic Solids", font_size=24, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.4)

        from manim import RegularPolygon, Polygon

        proj = lambda v: np.array([v[0] - v[2] * 0.5, v[1] + v[2] * 0.5, 0])

        # Tetrahedron
        tet_verts = [[0, 0, 0], [1, 0, 0], [0.5, 0, 0.87], [0.5, 0.82, 0.29]]
        tet_proj = [proj(np.array(v)) for v in tet_verts]
        tet = VGroup()
        for face_idx in [[0,1,2],[0,1,3],[1,2,3],[0,2,3]]:
            face_pts = [tet_proj[j] for j in face_idx]
            face = Polygon(*face_pts, stroke_color=MUTED_COLOR, stroke_width=1.2, fill_color=ACCENT_COLOR, fill_opacity=0.1)
            tet.add(face)
        tet.scale(0.9).shift(LEFT * 4 + UP * 0.5)

        # Cube
        cube_verts = [[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]]
        cube_proj = [proj(np.array(v)) for v in cube_verts]
        cube = VGroup()
        for face_idx in [[0,1,5,4],[0,3,7,4],[4,5,6,7],[0,1,2,3],[1,2,6,5],[3,2,6,7]]:
            face_pts = [cube_proj[j] for j in face_idx]
            face = Polygon(*face_pts, stroke_color=MUTED_COLOR, stroke_width=1.2, fill_color=ACCENT_COLOR, fill_opacity=0.1)
            cube.add(face)
        cube.scale(0.9).shift(LEFT * 1.5 + UP * 0.5)

        # Octahedron
        oct_verts = [[0,1,0],[1,0,0],[0,0,1],[-1,0,0],[0,0,-1],[0,-1,0]]
        oct_proj = [proj(np.array(v)) for v in oct_verts]
        octa = VGroup()
        for face_idx in [[0,1,2],[0,2,3],[0,3,4],[0,4,1],[5,1,2],[5,2,3],[5,3,4],[5,4,1]]:
            face_pts = [oct_proj[j] for j in face_idx]
            face = Polygon(*face_pts, stroke_color=MUTED_COLOR, stroke_width=1.2, fill_color=ACCENT_COLOR, fill_opacity=0.1)
            octa.add(face)
        octa.scale(0.9).shift(RIGHT * 1 + UP * 0.5)

        # Dodecahedron (simplified as 12-face shape using regular pentagon faces)
        # Use a simpler representation - just show a pentagon face with label
        dodec = RegularPolygon(n=5, stroke_color=MUTED_COLOR, stroke_width=1.2, fill_color=ACCENT_COLOR, fill_opacity=0.1)
        dodec.scale(0.7).shift(RIGHT * 3.5 + UP * 0.5)

        # Icosahedron (simplified as 20-face shape)
        ico = RegularPolygon(n=3, stroke_color=MUTED_COLOR, stroke_width=1.2, fill_color=ACCENT_COLOR, fill_opacity=0.1)
        ico.scale(0.7).shift(RIGHT * 5.5 + UP * 0.5)

        # Labels
        labels_data = [
            (tet, "Tetrahedron", "4 faces"),
            (cube, "Cube", "6 faces"),
            (octa, "Octahedron", "8 faces"),
            (dodec, "Dodecahedron", "12 faces"),
            (ico, "Icosahedron", "20 faces"),
        ]

        for shape, name, info_text in labels_data:
            name_label = Text(name, font_size=14, color=TEXT_COLOR)
            name_label.next_to(shape, DOWN, buff=0.15)
            info_label = Text(info_text, font_size=11, color=MUTED_COLOR)
            info_label.next_to(name_label, DOWN, buff=0.05)

            self.play(Create(shape), FadeIn(name_label), FadeIn(info_label), run_time=0.5)

        self.wait(2.0)
