# Imports
from PyQt5.QtWidgets import QGraphicsScene


# Classes
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self._mouse_press = lambda event: None
        self._mouse_move = lambda event: None
        self._mouse_release = lambda event: None

    def set_functions(self, mouse_press, mouse_move, mouse_release):
        self._mouse_press = mouse_press
        self._mouse_move = mouse_move
        self._mouse_release = mouse_release

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        self._mouse_press(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        self._mouse_move(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        self._mouse_release(event)
