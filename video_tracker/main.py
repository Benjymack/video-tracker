############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QAction

import platform
import ctypes

from video_display import VideoController
from video_overlay import OverlayController
from object_model import ObjectController


# Constants
VIDEO_FILE_PATH = 'tests/example_videos/video1.mp4'


# Functions
def make_dpi_aware():
    # https://github.com/pyqtgraph/pyqtgraph/issues/756
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)


# Classes
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the video, overlay and object controllers
        self._video_controller = VideoController()

        self._overlay_controller = OverlayController(self._video_controller)

        self._object_controller = ObjectController(self._overlay_controller,
                                                   self._video_controller)

        self._overlay_controller.set_object_controller(self._object_controller)

        self._object_controller.create_object()

        self._object_controller.initialise_display()

        # Display the video, etc
        self._main_widget = QSplitter()
        self._main_widget.setContentsMargins(10, 10, 10, 10)

        self._main_widget.addWidget(self._video_controller.get_video_display())
        self._main_widget.addWidget(self._object_controller.get_object_display())

        self.setCentralWidget(self._main_widget)

        # Create a menubar
        self._create_menu()

        # Open a video, only for example
        self._video_controller.open_video_file(VIDEO_FILE_PATH)
        # self._video_controller.play_pause_toggle()

    def _create_actions(self):
        self._new_action = QAction('&New')
        self._open_action = QAction('&Open')
        self._save_action = QAction('&Save')
        self._save_as_action = QAction('Save &As')
        self._import_action = QAction('&Import')
        self._export_action = QAction('&Export')

        self._undo_action = QAction('&Undo')
        self._redo_action = QAction('&Redo')

    def _create_menu(self):
        self._create_actions()

        self._menu_bar = self.menuBar()

        self._file_menu = self._menu_bar.addMenu('&File')
        self._file_menu.addActions((self._new_action, self._open_action))
        self._file_menu.addSeparator()
        self._file_menu.addActions((self._save_action, self._save_as_action))
        self._file_menu.addSeparator()
        self._file_menu.addActions((self._import_action, self._export_action))

        self._edit_menu = self._menu_bar.addMenu('&Edit')
        self._edit_menu.addActions((self._undo_action, self._redo_action))


if __name__ == '__main__':
    # QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    make_dpi_aware()

    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()
