# Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget

from .control_bar import ControlBar


class VideoDisplay(QWidget):
    # This would be a view
    def __init__(self):
        super().__init__()

        # Based off: https://stackoverflow.com/a/57842233

        # Create the video
        self._video_widget = QVideoWidget()

        # Create the control bar
        self._control_bar = ControlBar()

        # Create the layout
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._video_widget)
        self._layout.addWidget(self._control_bar)
        self.setLayout(self._layout)

    def get_video_widget(self):
        """
        Returns the video widget.
        """
        return self._video_widget

    def register_controller(self, controller):
        """
        Registers a controller to the video display.
        """
        self._control_bar.register_controller(controller)

    def set_position(self, new_position):
        """
        Sets the position of the video display.

        :param new_position: The new position (ms)
        """
        self._control_bar.set_position(new_position)

    def set_duration(self, new_duration):
        """
        Sets the duration of the video display.

        :param new_duration: The new duration (ms)
        """
        self._control_bar.set_duration(new_duration)

    def set_media_state(self, new_state):
        """
        Sets the media state of the video display.

        :param new_state: The new media state
        """
        self._control_bar.set_media_state(new_state)

    def enable_controls(self):
        """
        Enables the controls for the video display.
        """
        self._control_bar.set_enabled_controls(True)
