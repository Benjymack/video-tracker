# Imports
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt


# Classes
class VideoView(QGraphicsView):
    def enterEvent(self, event):
        super().enterEvent(event)
        self.viewport().setCursor(Qt.CrossCursor)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.viewport().setCursor(Qt.CrossCursor)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.viewport().setCursor(Qt.CrossCursor)