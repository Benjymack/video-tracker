############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget

from video_display import VideoController
from video_overlay import OverlayController
from object_model import ObjectController


# Constants
VIDEO_FILE_PATH = 'tests/example_videos/video1.mp4'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the video, overlay and object controllers
        self._video_controller = VideoController()

        self._overlay_controller = OverlayController(self._video_controller)

        self._object_controller = ObjectController(self._overlay_controller, self._video_controller)

        self._overlay_controller.set_object_controller(self._object_controller)

        self._object_controller.create_object()

        # Display the video, etc
        self._main_widget = QWidget()

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._video_controller.get_video_display())
        self._layout.addWidget(self._object_controller.get_object_display())
        self._main_widget.setLayout(self._layout)

        self.setCentralWidget(self._main_widget)

        # Create a menubar
        # self._menu_bar = self.menuBar()

        # self._file_menu = self._menu_bar.addMenu('&File')

        # Open a video, only for example
        self._video_controller.open_video_file(VIDEO_FILE_PATH)
        # self._video_controller.play_pause_toggle()


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()
