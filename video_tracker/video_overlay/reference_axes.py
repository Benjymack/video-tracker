# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import QPointF

import math

# Constants
RECT_SIZE = 20
X_AXIS_DISTANCE = 150
Y_AXIS_DISTANCE = 100
ANGLE_RECT_DISTANCE = 100
ARROW_SIDE_LENGTH = 10


# Classes
class ReferenceAxes(QGraphicsItemGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self._origin_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                              RECT_SIZE, RECT_SIZE, self)

        self._angle_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                             RECT_SIZE, RECT_SIZE, self)
        self._angle_rect.setX(ANGLE_RECT_DISTANCE)

        self._x_line = QGraphicsLineItem(0, 0, X_AXIS_DISTANCE, 0, self)
        self._x_arrow_1 = QGraphicsLineItem(X_AXIS_DISTANCE-ARROW_SIDE_LENGTH,
                                            ARROW_SIDE_LENGTH,
                                            X_AXIS_DISTANCE, 0, self)
        self._x_arrow_2 = QGraphicsLineItem(X_AXIS_DISTANCE - ARROW_SIDE_LENGTH,
                                            -ARROW_SIDE_LENGTH,
                                            X_AXIS_DISTANCE, 0, self)
        self._x_text = QGraphicsTextItem('x', self)
        self._x_text.setPos(X_AXIS_DISTANCE - 2.5*ARROW_SIDE_LENGTH,
                            RECT_SIZE / 4)

        self._y_line = QGraphicsLineItem(0, 0, 0, -Y_AXIS_DISTANCE, self)
        self._y_arrow_1 = QGraphicsLineItem(ARROW_SIDE_LENGTH,
                                            ARROW_SIDE_LENGTH - Y_AXIS_DISTANCE,
                                            0, -Y_AXIS_DISTANCE, self)
        self._y_arrow_2 = QGraphicsLineItem(-ARROW_SIDE_LENGTH,
                                            ARROW_SIDE_LENGTH - Y_AXIS_DISTANCE,
                                            0, -Y_AXIS_DISTANCE, self)
        self._y_text = QGraphicsTextItem('y', self)
        self._y_text.setPos(-RECT_SIZE,
                            -Y_AXIS_DISTANCE + ARROW_SIDE_LENGTH)

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

    def mouse_press(self, event):
        if self._angle_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'angle'
        elif self._origin_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'origin'
        else:
            self._current_moved_point = None

        self.mouse_event(event)

    def mouse_move(self, event):
        self.mouse_event(event)

    def mouse_release(self, event):
        self.mouse_event(event)

        if self._current_moved_point == 'angle':
            self._angle_rect.setX(ANGLE_RECT_DISTANCE)

        self._current_moved_point = None
