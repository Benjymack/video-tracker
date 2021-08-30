# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow

from video_controller import VideoController


# Constants
VIDEO_FILE_PATH = '../../tests/example_videos/video1.mp4'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._video_controller = VideoController()

        self._video_controller.open_video_file(VIDEO_FILE_PATH)
        self._video_controller.play_pause_toggle()

        self.setCentralWidget(self._video_controller.get_video_display())


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()