# Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoDisplay(QWidget):
    # This would be a view
    def __init__(self):
        super().__init__()

        # Based off: https://stackoverflow.com/a/57842233

        # Create the video
        self._video_widget = QVideoWidget()

        # TODO: Create the toolbar

        # Create the layout
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._video_widget)
        self.setLayout(self._layout)
