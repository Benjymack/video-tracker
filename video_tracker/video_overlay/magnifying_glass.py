# Imports
from PyQt5.QtWidgets import QGraphicsPixmapItem, QStyleOptionGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF


# Constants
SCALE_FACTOR = 5
WIDTH = 20
HEIGHT = 20


# Classes
class MagnifyingGlass(QGraphicsPixmapItem):
    def __init__(self, parent, video_widget):
        super().__init__(parent)

        self._video_widget = video_widget

        self._x, self._y = 0, 0

        ellipse_rect = QRectF(0, 0, WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR)
        self._path = QPainterPath()
        self._path.addEllipse(ellipse_rect)

    def update_image(self):
        """
        Updates the image that the magnifying glass displays.
        """
        pixmap = QPixmap(WIDTH * SCALE_FACTOR, HEIGHT * SCALE_FACTOR)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setClipPath(self._path, Qt.IntersectClip)
        painter.scale(SCALE_FACTOR, SCALE_FACTOR)
        painter.translate(-self._x, -self._y)
        self._video_widget.paint(painter, QStyleOptionGraphicsItem())
        self.setPixmap(pixmap)
        painter.end()

    def mouse_move(self, event):
        """
        Updates the position and the image of the magnifying glass.

        :param event: The QEvent that contains the position of
        the mouse movement.
        """
        x, y = event.scenePos().x(), event.scenePos().y()

        width = self.boundingRect().width()
        height = self.boundingRect().height()

        self._x, self._y = x - WIDTH/2, y - WIDTH/2

        self.update_image()

        self.setPos(QPointF(x - width/2, y - height/2))

        return False

    def mouse_press(self, event):
        return False

    def mouse_release(self, event):
        return False

    def load(self, data):
        self.setVisible(data['visible'])

    def dump(self):
        return {
            'visible': self.isVisible(),
        }
