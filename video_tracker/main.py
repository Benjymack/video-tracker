############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from video_display import VideoDisplay


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._video_display = VideoDisplay(self)

        self.setCentralWidget(self._video_display)

        # self._label = QLabel('Hi', self)


app = QApplication([])
main = MainWindow()
main.show()

app.exec_()
