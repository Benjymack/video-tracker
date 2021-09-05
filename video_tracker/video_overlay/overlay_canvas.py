# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtCore import QSizeF, QPointF

try:
    from video_overlay.reference_axes import ReferenceAxes
except ImportError:
    from reference_axes import ReferenceAxes


# Classes
class OverlayCanvas(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self._reference_axes = ReferenceAxes(self)

        self._reference_axes._move_origin_to(QPointF(100, 150))

    def get_reference_axes(self):
        return self._reference_axes

