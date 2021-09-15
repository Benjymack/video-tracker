# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QSizeF, QPointF

try:
    from video_overlay.reference_axes import ReferenceAxes
    from video_overlay.ruler import Ruler
except ImportError:
    from reference_axes import ReferenceAxes
    from ruler import Ruler

# Constants
CROSS_LENGTH = 10


# Classes
class OverlayCanvas(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self._reference_axes = ReferenceAxes(self)

        self._reference_axes._move_origin_to(QPointF(100, 150))

        self._ruler = Ruler(self)

        self._points = []

    def get_reference_axes(self):
        return self._reference_axes

    def get_ruler(self):
        return self._ruler

    def clear_points(self):
        for point in self._points:
            for line in point:
                line.scene().removeItem(line)
                self.removeFromGroup(line)
        self._points = []

    def draw_point(self, x, y, colour):
        pen = QPen(colour)
        vertical_line = QGraphicsLineItem(x, y - CROSS_LENGTH,
                                          x, y + CROSS_LENGTH, self)
        vertical_line.setPen(pen)
        horizontal_line = QGraphicsLineItem(x - CROSS_LENGTH, y,
                                            x + CROSS_LENGTH, y, self)
        horizontal_line.setPen(pen)
        self._points.append((vertical_line, horizontal_line))
