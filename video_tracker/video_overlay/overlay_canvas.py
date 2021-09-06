# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtCore import QSizeF, QPointF

try:
    from video_overlay.reference_axes import ReferenceAxes
    from video_overlay.ruler import Ruler
except ImportError:
    from reference_axes import ReferenceAxes
    from ruler import Ruler


# Classes
class OverlayCanvas(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self._reference_axes = ReferenceAxes(self)

        self._reference_axes._move_origin_to(QPointF(100, 150))

        self._ruler = Ruler(self)

    def get_reference_axes(self):
        return self._reference_axes

    def get_ruler(self):
        return self._ruler

