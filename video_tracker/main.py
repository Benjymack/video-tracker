############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QAction, \
    QWidget, QVBoxLayout, QFileDialog

import platform
import ctypes

from video_display import VideoController
from video_overlay import OverlayController
from object_model import ObjectController, ExportDialog

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
        self._video_controller.get_video_player().register_magnifying_glass(
            self._overlay_controller.get_magnifying_glass())

        self._object_controller.create_object()

        self._object_controller.initialise_display()

        # Display the video, etc
        self._main_widget = QSplitter()
        self._main_widget.setContentsMargins(10, 10, 10, 10)

        self._main_widget.addWidget(self._video_controller.get_video_display())
        self._main_widget.addWidget(
            self._object_controller.get_object_display())

        self._main_container = QWidget()
        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._object_controller.get_object_selector())
        self._layout.addWidget(self._main_widget)
        self._main_container.setLayout(self._layout)

        self.setCentralWidget(self._main_container)

        # Create a menubar
        self._create_menu()

        # Set the title
        self.setWindowTitle(
            'Video Tracker')  # TODO: Come up with a better title

    def _open_video(self, checked):
        file_name, _ = QFileDialog.getOpenFileName(
            caption='Import Video',
            filter='Video Files (*.avi *.mov *.mp4);;All Files (*.*)')
        self._video_controller.open_video_file(file_name)
        self._video_controller.play_pause_toggle()
        self._video_controller.play_pause_toggle()

    def _export_data(self, checked):
        export_dialog = ExportDialog(self, self._object_controller)
        export_dialog.exec_()

    def _create_actions(self):
        self._new_action = QAction('&New')
        self._open_action = QAction('&Open')

        self._save_action = QAction('&Save')
        self._save_as_action = QAction('Save &As')

        self._import_action = QAction('&Import Video')
        self._import_action.triggered.connect(self._open_video)
        self._export_action = QAction('&Export Data')
        self._export_action.triggered.connect(self._export_data)

        self._undo_action = QAction('&Undo')
        self._redo_action = QAction('&Redo')

    def _create_menu(self):
        self._create_actions()

        self._menu_bar = self.menuBar()

        self._file_menu = self._menu_bar.addMenu('&File')
        # self._file_menu.addActions((self._new_action, self._open_action))
        # self._file_menu.addSeparator()
        # self._file_menu.addActions((self._save_action, self._save_as_action))
        # self._file_menu.addSeparator()
        self._file_menu.addActions((self._import_action, self._export_action))

        # self._edit_menu = self._menu_bar.addMenu('&Edit')
        # self._edit_menu.addActions((self._undo_action, self._redo_action))


if __name__ == '__main__':
    make_dpi_aware()

    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()
