# Imports
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QHBoxLayout, QSlider, QSizePolicy


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
        self._play_pause_button.setFixedHeight(24)  # TODO: What is this for?
        self._play_pause_button.setIconSize(ICON_SIZE)
        self._play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # Scrubber
        self._scrubber = QSlider(Qt.Horizontal)
        self._scrubber.setRange(0, 0)

        # Frame decrement button
        self._frame_decrement_button = QPushButton()

        # Frame increment button
        self._frame_increment_button = QPushButton()

        # TODO: Trial the layout of the buttons
        self._layout = QHBoxLayout()
        self._layout.addWidget(self._frame_decrement_button)
        self._layout.addWidget(self._play_pause_button)
        self._layout.addWidget(self._frame_increment_button)
        self._layout.addWidget(self._scrubber)

        self.setLayout(self._layout)
        
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self._buttons = (
            self._play_pause_button,
            self._frame_decrement_button,
            self._frame_increment_button,
        )

    def register_controller(self, controller):
        self._play_pause_button.clicked.connect(controller.play_pause_toggle)  # TODO: Add function to controller
        self._scrubber.sliderMoved.connect(controller.position_changed)

    def set_enabled_buttons(self, are_enabled):
        for button in self._buttons:
            button.setEnabled(are_enabled)