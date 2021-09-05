# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsLineItem
from PyQt5.QtCore import QPointF

# Constants
RECT_SIZE = 20
X_AXIS_DISTANCE = 150
Y_AXIS_DISTANCE = 100


# Classes
class Ruler(QGraphicsItemGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self._origin_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                              RECT_SIZE, RECT_SIZE, self)

        self._angle_rect = QGraphicsRectItem(100, -RECT_SIZE / 2,
                                             RECT_SIZE, RECT_SIZE, self)

        self._x_line = QGraphicsLineItem(0, 0, X_AXIS_DISTANCE, 0, self)
        self._y_line = QGraphicsLineItem(0, 0, 0, -Y_AXIS_DISTANCE, self)

        self.setRotation(35)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        print('Press')

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        print('Move')

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        print('Release')

    def contains(self, point):
        actual_point = QPointF(point.x() - self.pos().x(), point.y() - self.pos().y())
        print(point)
        # print(self._angle_rect.shape().boundingRect())
        print(self._angle_rect.sceneBoundingRect().contains(point))
        print(self._origin_rect.sceneBoundingRect().contains(point))
        return True
