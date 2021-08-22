# Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget

from control_bar import ControlBar


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

    def register_controller(self, controller):
        self._control_bar.register_controller(controller)

    def set_position(self, new_position):
        self._control_bar.set_position(new_position)

    def set_duration(self, new_duration):
        self._control_bar.set_duration(new_duration)

    def set_media_state(self, new_state):
        self._control_bar.set_media_state(new_state)

    def enable_controls(self):
        self._control_bar.set_enabled_controls(True)
