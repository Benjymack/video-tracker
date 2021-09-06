# Imports
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsLineItem, \
    QGraphicsTextItem
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTextCursor

try:
    from video_overlay.length_text import LengthText
except ImportError:
    from length_text import LengthText

import math

# Constants
TRIGGER_DISTANCE = 10
RULER_DISTANCE = 10


# Classes
class Ruler(QGraphicsItemGroup):
    def __init__(self, parent):
        super().__init__(parent)

        self._pos1 = QPointF(100, 100)
        self._pos2 = QPointF(120, 80)

        self._pos1_line = QGraphicsLineItem(0, 0, 0, RULER_DISTANCE, self)
        self._pos2_line = QGraphicsLineItem(0, 0, 0, RULER_DISTANCE, self)
        self._join_line = QGraphicsLineItem(0, RULER_DISTANCE,
                                            0, RULER_DISTANCE, self)

        self._length_text = LengthText('1m', self)
        # self._length_text.setFlags(QGraphicsTextItem.ItemIsFocusable | QGraphicsTextItem.ItemIsSelectable)
        # self._length_text.setTextInteractionFlags(Qt.TextEditorInteraction)

        self._update_lines()

        self._current_moving_pos = 0

    def _update_lines(self):
        join_angle = math.degrees(math.atan2(self._pos1.y() - self._pos2.y(),
                                             self._pos1.x() - self._pos2.x()))

        offset_angle = join_angle + 90

        offset_angle_rad = math.radians(offset_angle)

        if math.sin(offset_angle_rad) < 0:
            offset_angle_rad -= math.pi
            join_angle -= 180

        join_angle_rad = math.radians(join_angle)

        x1 = self._pos1.x() - math.cos(offset_angle_rad) * TRIGGER_DISTANCE
        y1 = self._pos1.y() - math.sin(offset_angle_rad) * TRIGGER_DISTANCE
        x2 = self._pos2.x() - math.cos(offset_angle_rad) * TRIGGER_DISTANCE
        y2 = self._pos2.y() - math.sin(offset_angle_rad) * TRIGGER_DISTANCE

        self._pos1_line.setLine(self._pos1.x(), self._pos1.y(), x1, y1)
        self._pos2_line.setLine(self._pos2.x(), self._pos2.y(), x2, y2)
        self._join_line.setLine(x1, y1, x2, y2)


        text_width = self._length_text.boundingRect().width()
        text_x = (x1 + x2) / 2 - math.cos(join_angle_rad) * text_width / 2
        text_y = (y1 + y2) / 2 - math.sin(join_angle_rad) * text_width / 2

        self._length_text.setPos(text_x, text_y)
        self._length_text.setRotation(join_angle)

    def _move_pos1(self, pos):
        self._pos1 = pos
        self._update_lines()

    def _move_pos2(self, pos):
        self._pos2 = pos
        self._update_lines()

    def _mouse_event(self, event):
        if self._current_moving_pos == 1:
            self._move_pos1(event.scenePos())
        elif self._current_moving_pos == 2:
            self._move_pos2(event.scenePos())

    def mouse_press(self, event):
        print('Ruler press')

        event_x, event_y = event.scenePos().x(), event.scenePos().y()

        # Determine the closest moving point
        pos1_distance = math.sqrt((event_x - self._pos1.x()) ** 2
                                  + (event_y - self._pos1.y()) ** 2)
        pos2_distance = math.sqrt((event_x - self._pos2.x()) ** 2
                                  + (event_y - self._pos2.y()) ** 2)

        if pos1_distance <= TRIGGER_DISTANCE and pos1_distance <= pos2_distance:
            self._current_moving_pos = 1
            print(1)
        elif pos2_distance <= TRIGGER_DISTANCE and \
                pos2_distance <= pos1_distance:
            self._current_moving_pos = 2
            print(2)
        else:
            self._current_moving_pos = 0
            if self._length_text.sceneBoundingRect().contains(event.scenePos()):
                self._length_text.setTextInteractionFlags(Qt.TextEditorInteraction)
                self._length_text.setFocus()

        if not self._length_text.hasFocus():
            self._length_text.setTextInteractionFlags(Qt.NoTextInteraction)
            cursor = self._length_text.textCursor()
            cursor.clearSelection()
            self._length_text.setTextCursor(cursor)

        self._mouse_event(event)

    def mouse_move(self, event):
        self._mouse_event(event)
        print(self._length_text.hasFocus())

    def mouse_release(self, event):
        self._mouse_event(event)

        self._current_moving_pos = 0
