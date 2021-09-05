# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsLineItem
from PyQt5.QtCore import QPointF

import math

# Constants
RECT_SIZE = 20
X_AXIS_DISTANCE = 150
Y_AXIS_DISTANCE = 100


# Classes
class ReferenceAxes(QGraphicsItemGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self._origin_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                              RECT_SIZE, RECT_SIZE, self)

        self._angle_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                             RECT_SIZE, RECT_SIZE, self)
        self._angle_rect.setX(100)

        self._x_line = QGraphicsLineItem(0, 0, X_AXIS_DISTANCE, 0, self)
        self._y_line = QGraphicsLineItem(0, 0, 0, -Y_AXIS_DISTANCE, self)

        self._current_moved_point = None

        self._reference_pos = QPointF(0, 0)
        self._reference_angle = 0

    def _move_origin_to(self, pos):
        self._reference_pos = pos
        self.setPos(self._reference_pos)

    def _move_angle_to(self, pos):
        dx = pos.x() - self._reference_pos.x()
        dy = pos.y() - self._reference_pos.y()

        angle = math.degrees(math.atan2(dy, dx))

        self._reference_angle = angle
        self.setRotation(self._reference_angle)

        self._angle_rect.setX(math.sqrt(dx**2 + dy**2))

    def mouse_event(self, event):
        if self._current_moved_point == 'origin':
            self._move_origin_to(event.scenePos())
        elif self._current_moved_point == 'angle':
            self._move_angle_to(event.scenePos())
        else:
            pass

    def mouse_press(self, event):
        if self._angle_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'angle'
        elif self._origin_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'origin'
        else:
            self._current_moved_point = None

        self.mouse_event(event)

    def mouse_move(self, event):
        print('Reference move')

        self.mouse_event(event)

    def mouse_release(self, event):
        print('Reference release')

        self.mouse_event(event)

        self._current_moved_point = None
