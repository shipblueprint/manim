"""
Stack / Queue Operations Scene - Push/Pop/Enqueue/Dequeue.
"""

from manim import Scene, Text, VGroup, Rectangle, Arrow, UP, DOWN, LEFT, RIGHT, Create, FadeIn, FadeOut
import numpy as np

from manim_assets.config import ACCENT_COLOR, BG_COLOR, HEADING_FONT, MUTED_COLOR, TEXT_COLOR


class StackQueueScene(Scene):
    """
    Scene: Visualize Stack (LIFO) and Queue (FIFO) operations.
    Left side: Stack with push/pop.
    Right side: Queue with enqueue/dequeue.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cell_width: float = 1.4
        self.cell_height: float = 0.55
        self.max_visible: int = 5

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = Text("Stack & Queue Operations", font_size=24, color=TEXT_COLOR, font=HEADING_FONT)
        title.to_edge(UP, buff=0.5)
        self.play(FadeIn(title), run_time=0.5)

        # === STACK (left side) ===
        stack_x = -3.5
        stack_label = Text("Stack (LIFO)", font_size=18, color=ACCENT_COLOR)
        stack_label.move_to([stack_x, 3.0, 0])
        self.add(stack_label)

        # Stack container outline
        stack_container = Rectangle(
            width=self.cell_width + 0.2,
            height=self.max_visible * (self.cell_height + 0.05) + 0.1,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
            fill_opacity=0,
        )
        stack_container.move_to([stack_x, 0.5, 0])
        self.add(stack_container)

        # TOP label
        top_label = Text("TOP", font_size=12, color=ACCENT_COLOR)
        top_label.next_to(stack_container, RIGHT, buff=0.15).shift(UP * (self.max_visible - 1) * (self.cell_height + 0.05) / 2)
        self.add(top_label)

        # Stack operations
        stack_items: list = []  # list of (rect, label) from bottom to top
        stack_values = [10, 20, 30]

        # Push operations
        for val in stack_values:
            self._stack_push(stack_items, stack_x, val, "Push")

        # Pop operation
        self._stack_pop(stack_items, stack_x, "Pop")

        # Push one more
        self._stack_push(stack_items, stack_x, 40, "Push")

        self.wait(0.5)

        # === QUEUE (right side) ===
        queue_x = 3.5
        queue_label = Text("Queue (FIFO)", font_size=18, color=TEXT_COLOR)
        queue_label.move_to([queue_x, 3.0, 0])
        self.add(queue_label)

        # Queue container outline (horizontal)
        queue_container = Rectangle(
            width=self.max_visible * (self.cell_width + 0.1) + 0.1,
            height=self.cell_height + 0.2,
            stroke_color=MUTED_COLOR,
            stroke_width=1.5,
            fill_opacity=0,
        )
        queue_container.move_to([queue_x, 0.5, 0])
        self.add(queue_container)

        # FRONT / BACK labels
        front_label = Text("FRONT", font_size=12, color=TEXT_COLOR)
        front_label.next_to(queue_container, DOWN, buff=0.15).shift(LEFT * 1.5)
        back_label = Text("BACK", font_size=12, color=TEXT_COLOR)
        back_label.next_to(queue_container, DOWN, buff=0.15).shift(RIGHT * 1.5)
        self.add(front_label, back_label)

        # Queue operations
        queue_items: list = []  # list of (rect, label) from front to back
        queue_values = [100, 200, 300]

        # Enqueue operations
        for val in queue_values:
            self._queue_enqueue(queue_items, queue_x, val, "Enqueue")

        # Dequeue operation
        self._queue_dequeue(queue_items, queue_x, "Dequeue")

        # Enqueue one more
        self._queue_enqueue(queue_items, queue_x, 400, "Enqueue")

        self.wait(2.0)

    def _stack_push(self, stack_items: list, stack_x: float, value: int, op_name: str) -> None:
        """Push a value onto the stack."""
        op_text = Text(f"{op_name}({value})", font_size=14, color=ACCENT_COLOR)
        op_text.move_to([stack_x, -2.5, 0])
        self.add(op_text)

        # Create cell
        rect = Rectangle(
            width=self.cell_width,
            height=self.cell_height,
            stroke_color=ACCENT_COLOR,
            stroke_width=1.5,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.15,
        )
        label = Text(str(value), font_size=14, color=TEXT_COLOR)

        # Position: on top of existing items
        n = len(stack_items)
        base_y = 0.5 - (self.max_visible - 1) * (self.cell_height + 0.05) / 2
        y = base_y + n * (self.cell_height + 0.05)

        rect.move_to([stack_x, y, 0])
        label.move_to(rect.get_center())

        # Animate from above
        rect.move_to([stack_x, y + 1.5, 0])
        label.move_to(rect.get_center())

        self.play(
            rect.animate.move_to([stack_x, y, 0]),
            label.animate.move_to([stack_x, y, 0]),
            Create(rect),
            FadeIn(label),
            run_time=0.5,
        )

        stack_items.append((rect, label))
        self.remove(op_text)

    def _stack_pop(self, stack_items: list, stack_x: float, op_name: str) -> None:
        """Pop the top value from the stack."""
        if not stack_items:
            return

        rect, label = stack_items[-1]
        popped_val = label.text

        op_text = Text(f"{op_name}() -> {popped_val}", font_size=14, color=ACCENT_COLOR)
        op_text.move_to([stack_x, -2.5, 0])
        self.add(op_text)

        # Highlight then remove
        self.play(
            rect.animate.set_stroke(color=TEXT_COLOR, width=2.5),
            run_time=0.3,
        )
        self.play(
            FadeOut(rect),
            FadeOut(label),
            run_time=0.4,
        )

        stack_items.pop()
        self.remove(op_text)

    def _queue_enqueue(self, queue_items: list, queue_x: float, value: int, op_name: str) -> None:
        """Enqueue a value at the back of the queue."""
        op_text = Text(f"{op_name}({value})", font_size=14, color=TEXT_COLOR)
        op_text.move_to([queue_x, -2.5, 0])
        self.add(op_text)

        rect = Rectangle(
            width=self.cell_width,
            height=self.cell_height,
            stroke_color=TEXT_COLOR,
            stroke_width=1.5,
            fill_color=TEXT_COLOR,
            fill_opacity=0.1,
        )
        label = Text(str(value), font_size=14, color=TEXT_COLOR)

        # Position: at the back (right side)
        n = len(queue_items)
        base_x = queue_x - (self.max_visible - 1) * (self.cell_width + 0.1) / 2
        x = base_x + n * (self.cell_width + 0.1)

        rect.move_to([x, 0.5, 0])
        label.move_to(rect.get_center())

        # Animate from right
        rect.move_to([x + 2.0, 0.5, 0])
        label.move_to(rect.get_center())

        self.play(
            rect.animate.move_to([x, 0.5, 0]),
            label.animate.move_to([x, 0.5, 0]),
            Create(rect),
            FadeIn(label),
            run_time=0.5,
        )

        queue_items.append((rect, label))
        self.remove(op_text)

    def _queue_dequeue(self, queue_items: list, queue_x: float, op_name: str) -> None:
        """Dequeue a value from the front of the queue."""
        if not queue_items:
            return

        rect, label = queue_items[0]
        dequeued_val = label.text

        op_text = Text(f"{op_name}() -> {dequeued_val}", font_size=14, color=TEXT_COLOR)
        op_text.move_to([queue_x, -2.5, 0])
        self.add(op_text)

        # Highlight then remove
        self.play(
            rect.animate.set_stroke(color=ACCENT_COLOR, width=2.5),
            run_time=0.3,
        )
        self.play(
            FadeOut(rect),
            FadeOut(label),
            run_time=0.4,
        )

        queue_items.pop(0)

        # Shift remaining items left
        shift_anims = []
        base_x = queue_x - (self.max_visible - 1) * (self.cell_width + 0.1) / 2
        for i, (r, l) in enumerate(queue_items):
            target_x = base_x + i * (self.cell_width + 0.1)
            shift_anims.append(r.animate.move_to([target_x, 0.5, 0]))
            shift_anims.append(l.animate.move_to([target_x, 0.5, 0]))

        if shift_anims:
            self.play(*shift_anims, run_time=0.4)

        self.remove(op_text)
