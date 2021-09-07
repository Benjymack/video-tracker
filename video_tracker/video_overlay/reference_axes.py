# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, \
    QGraphicsLineItem, QGraphicsTextItem
from PyQt5.QtCore import QPointF

import math

# Constants
RECT_SIZE = 20
X_AXIS_DISTANCE = 150
Y_AXIS_DISTANCE = 100
X_ANGLE_RECT_DISTANCE = 100
Y_ANGLE_RECT_DISTANCE = 50
ARROW_SIDE_LENGTH = 10


# Classes
class ReferenceAxes(QGraphicsItemGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self._origin_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                              RECT_SIZE, RECT_SIZE, self)

        self._x_angle_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                               RECT_SIZE, RECT_SIZE, self)
        self._x_angle_rect.setX(X_ANGLE_RECT_DISTANCE)

        self._y_angle_rect = QGraphicsRectItem(-RECT_SIZE / 2, -RECT_SIZE / 2,
                                               RECT_SIZE, RECT_SIZE, self)
        self._y_angle_rect.setY(-Y_ANGLE_RECT_DISTANCE)

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

    def get_origin_pos(self):
        return self._reference_pos.x(), self._reference_pos.y()

    def get_reference_angle(self):
        return self._reference_angle

    def _move_origin_to(self, pos):
        self._reference_pos = pos
        self.setPos(self._reference_pos)

    def _move_angle_to(self, pos, offset_angle):
        dx = pos.x() - self._reference_pos.x()
        dy = pos.y() - self._reference_pos.y()

        angle = math.degrees(math.atan2(dy, dx)) + offset_angle

        self._reference_angle = angle
        self.setRotation(self._reference_angle)

        return math.sqrt(dx ** 2 + dy ** 2)

    def _mouse_event(self, event):
        if self._current_moved_point == 'origin':
            self._move_origin_to(event.scenePos())
        elif self._current_moved_point == 'anglex':
            self._x_angle_rect.setX(self._move_angle_to(event.scenePos(), 0))
        elif self._current_moved_point == 'angley':
            self._y_angle_rect.setY(-self._move_angle_to(event.scenePos(), 90))

    def mouse_press(self, event):
        if self._x_angle_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'anglex'
        elif self._y_angle_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'angley'
        elif self._origin_rect.sceneBoundingRect().contains(event.scenePos()):
            self._current_moved_point = 'origin'
        else:
            self._current_moved_point = None

        self._mouse_event(event)

    def mouse_move(self, event):
        self._mouse_event(event)

    def mouse_release(self, event):
        self._mouse_event(event)

        if self._current_moved_point in ('anglex', 'angley'):
            self._x_angle_rect.setX(X_ANGLE_RECT_DISTANCE)
            self._y_angle_rect.setY(-Y_ANGLE_RECT_DISTANCE)

        self._current_moved_point = None
