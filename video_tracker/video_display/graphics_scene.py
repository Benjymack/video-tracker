# Imports
from PyQt5.QtWidgets import QGraphicsScene


# Classes
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self._mouse_press = lambda event: None
        self._mouse_move = lambda event: None
        self._mouse_release = lambda event: None

    def keyPressEvent(self, event):
        """
        Event for when the user presses a key.
        Passes the event down to the focused widget in the scene.
        """
        super().keyPressEvent(event)

        focused_item = self.focusItem()
        if focused_item is not None:
            focused_item.keyPressEvent(event)

    def set_functions(self, mouse_press, mouse_move, mouse_release):
        """
        Sets the functions to call when the user presses, moves or releases the
        mouse.
        """
        self._mouse_press = mouse_press
        self._mouse_move = mouse_move
        self._mouse_release = mouse_release

    def mousePressEvent(self, event):
        """
        Passes the mouse press down to any child elements.
        """
        super().mousePressEvent(event)

        self._mouse_press(event)

    def mouseMoveEvent(self, event):
        """
        Passes the mouse movement down to any child elements.
        """
        super().mouseMoveEvent(event)

        self._mouse_move(event)

    def mouseReleaseEvent(self, event):
        """
        Passes the mouse release down to any child elements.
        """
        super().mouseReleaseEvent(event)

        self._mouse_release(event)
