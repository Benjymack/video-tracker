# Imports
from PyQt5.QtWidgets import QGraphicsScene


# Classes
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)

        self._mouse_move = lambda event: None

    def keyPressEvent(self, event):
        """
        Event for when the user presses a key.
        Passes the event down to the focused widget in the scene.
        """
        super().keyPressEvent(event)

        focused_item = self.focusItem()
        if focused_item is not None:
            focused_item.keyPressEvent(event)

    def set_move_function(self, mouse_move):
        self._mouse_move = mouse_move

    def mouseMoveEvent(self, event):
        """
        Passes the mouse movement down to any child elements.
        """
        super().mouseMoveEvent(event)

        self._mouse_move(event)
