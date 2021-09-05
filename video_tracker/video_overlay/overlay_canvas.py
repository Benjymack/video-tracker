# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem
from PyQt5.QtCore import QSizeF

from .ruler import Ruler


# Classes
class OverlayCanvas(QGraphicsItemGroup):
    def __init__(self):
        super().__init__()

        self._ruler = Ruler(self)

        self._ruler.setPos(100, 100)

