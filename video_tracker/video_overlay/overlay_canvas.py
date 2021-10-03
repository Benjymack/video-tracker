# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtGui import QPen
from PyQt5.QtCore import QPointF

try:
    from video_overlay.reference_axes import ReferenceAxes
    from video_overlay.ruler import Ruler
    from video_overlay.magnifying_glass import MagnifyingGlass
except ImportError:
    from reference_axes import ReferenceAxes
    from ruler import Ruler
    from magnifying_glass import MagnifyingGlass

# Constants
CROSS_LENGTH = 10


# Classes
class OverlayCanvas(QGraphicsItemGroup):
    def __init__(self, video_controller):
        super().__init__()

        self._magnifying_glass = MagnifyingGlass(
            self, video_controller.get_video_widget())
        self._magnifying_glass.setZValue(1)

        self._reference_axes = ReferenceAxes(self)
        self._reference_axes.setZValue(2)

        self._reference_axes._move_origin_to(QPointF(100, 150))

        self._ruler = Ruler(self)
        self._ruler.setZValue(2)

        self._points = []

    def get_reference_axes(self):
        """
        Returns the reference axes.
        """
        return self._reference_axes

    def get_ruler(self):
        """
        Returns the ruler.
        """
        return self._ruler

    def get_magnifying_glass(self):
        """
        Returns the magnifying glass.
        """
        return self._magnifying_glass

    def clear_points(self):
        """
        Clears all of the points that are currently being displayed.
        """
        for point in self._points:
            for line in point:
                line.scene().removeItem(line)
                self.removeFromGroup(line)
        self._points = []

    def draw_point(self, x, y, colour):
        """
        Draws a point at the specified position with the given colour.

        :param x: The x position of the point (px)
        :param y: The y position of the point (px)
        :param colour: The colour to draw with (QColor)
        """
        pen = QPen(colour)
        vertical_line = QGraphicsLineItem(x, y - CROSS_LENGTH,
                                          x, y + CROSS_LENGTH, self)
        vertical_line.setPen(pen)
        horizontal_line = QGraphicsLineItem(x - CROSS_LENGTH, y,
                                            x + CROSS_LENGTH, y, self)
        horizontal_line.setPen(pen)
        self._points.append((vertical_line, horizontal_line))

    def set_ruler_visibility(self, visibility):
        """
        Sets the visibility of the ruler to the given value.
        """
        self._ruler.setVisible(visibility)

    def set_axes_visibility(self, visibility):
        """
        Sets the visibility of the reference axes to the given value.
        """
        self._reference_axes.setVisible(visibility)

    def set_zoom_visibility(self, visibility):
        """
        Sets the visibility of the magnifying glass to the given value.
        """
        self._magnifying_glass.setVisible(visibility)
