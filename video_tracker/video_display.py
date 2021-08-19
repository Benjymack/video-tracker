# Imports
from PyQt5.QtWidgets import QWidget, QLabel


class VideoDisplay(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self._label = QLabel('Hello World!', self)
