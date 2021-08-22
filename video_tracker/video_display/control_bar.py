# Imports
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QHBoxLayout, QSlider, QSizePolicy
from PyQt5.QtMultimedia import QMediaPlayer


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
        # TODO: Trial which button to use (seek or skip)
        self._frame_decrement_button = QPushButton()
        self._frame_decrement_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        # Frame increment button
        self._frame_increment_button = QPushButton()
        self._frame_increment_button.setIcon(self.style().standardIcon(QStyle.SP_MediaSkipForward))

        # TODO: Trial the layout of the buttons
        self._layout = QHBoxLayout()
        self._layout.addWidget(self._frame_decrement_button)
        self._layout.addWidget(self._play_pause_button)
        self._layout.addWidget(self._frame_increment_button)
        self._layout.addWidget(self._scrubber)

        self.setLayout(self._layout)
        
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self._controls = (
            self._play_pause_button,
            self._frame_decrement_button,
            self._frame_increment_button,
            self._scrubber,
        )

        self.set_enabled_controls(False)  # Disable the buttons until a video is opened

    def register_controller(self, controller):
        """
        Registers a controller to the control bar.
        Expects the following methods to be defined:

            play_pause_toggle()
            position_changed(new_position)

        :param controller: The controller to connect the signals to
        """
        self._play_pause_button.clicked.connect(controller.play_pause_toggle)
        self._scrubber.sliderMoved.connect(controller.position_changed)

    def set_enabled_controls(self, are_enabled):
        """
        Changes whether the controls (buttons, scrubber, etc) are enabled.

        :param are_enabled: The new enabled status of the controls.
        """
        for control in self._controls:
            control.setEnabled(are_enabled)

    def set_duration(self, new_duration):
        """
        Sets the duration of the scrubber bar.

        :param new_duration: The new duration (frames)
        """
        self._scrubber.setRange(0, new_duration)

    def set_position(self, new_position):
        """
        Sets the position of the scrubber bar.

        :param new_position: The new position (frames)
        """
        self._scrubber.setValue(new_position)

    def set_media_state(self, new_state):
        """
        Sets the media state of the control bar (for the play/pause button)

        :param new_state: The new state to use
        """
        if new_state == QMediaPlayer.PlayingState:
            self._play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self._play_pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
