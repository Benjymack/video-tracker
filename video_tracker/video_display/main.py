# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow

from video_player import VideoPlayer
from video_display import VideoDisplay


# Constants
VIDEO_FILE_PATH = '../../tests/example_videos/video1.mp4'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._video_player = VideoPlayer()
        self._video_display = VideoDisplay()

        self._video_player.initialise_display(self._video_display._video_widget)
        self._video_player.set_video_file(VIDEO_FILE_PATH)
        self._video_player.toggle_play_state()

        self.setCentralWidget(self._video_display)


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()