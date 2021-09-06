# Imports
from PyQt5.QtWidgets import QGraphicsTextItem


# Classes
class LengthText(QGraphicsTextItem):
    def focusOutEvent(self, event):
        print('Hi')

    def focusInEvent(self, event):
        print('Ho')

    def mouseDoubleClickEvent(self, event):
        print('Double click')