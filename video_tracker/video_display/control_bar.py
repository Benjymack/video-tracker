# Imports
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QHBoxLayout


# Constants
ICON_SIZE = QSize(16, 16)


# Classes
class ControlBar(QWidget):
    # This is another view
    def __init__(self):
        super().__init__()

        # Also based off: https://stackoverflow.com/a/57842233

        # Play/pause button
        self._play_pause_button = QPushButton()
        self._play_pause_button.setEnabled(False)  # Before the user has opened a video, disable the button
        self._play_pause_button.setFixedHeight(24)  # TODO: What is this for?
        self._play_pause_button.setIconSize(ICON_SIZE)
        self._play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # TODO: Trial the layout of the buttons
        self._layout = QHBoxLayout()
        self._layout.addWidget(self._play_pause_button)

        self.setLayout(self._layout)

    def register_controller(self, controller):
        self._play_pause_button.clicked.connect(controller.play_pause_toggle)  # TODO: Add function to controller
