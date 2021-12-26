############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QAction, \
    QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer

import platform
import ctypes
import json

from json.decoder import JSONDecodeError

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

        self._video_controller.set_object_controller(self._object_controller)
        self._overlay_controller.set_object_controller(self._object_controller)

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

        # Update the magnifying glass periodically
        self._magnifying_glass = self._overlay_controller.get_magnifying_glass()
        self._magnifying_glass_timer = QTimer(self)
        self._magnifying_glass_timer.setInterval(100)
        self._magnifying_glass_timer.timeout.connect(
            self._magnifying_glass.update_image)
        self._magnifying_glass_timer.start()

    def _open_video(self, checked):
        file_name, _ = QFileDialog.getOpenFileName(
            caption='Import Video',
            filter='Video Files (*.avi *.mov *.mp4);;All Files (*.*)')

        if file_name is None or file_name == '':
            return

        self._video_controller.open_video_file(file_name)

    def _export_data(self, checked):
        export_dialog = ExportDialog(self, self._object_controller)
        export_dialog.exec_()

    def _create_actions(self):
        self._new_action = QAction('&New')
        self._open_action = QAction('&Open')
        self._open_action.triggered.connect(self._open_file)

        self._save_action = QAction('&Save')
        self._save_action.triggered.connect(self._save_file)
        self._save_as_action = QAction('Save &As')
        self._save_as_action.triggered.connect(self._save_as_file)

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
        self._file_menu.addAction(self._open_action)
        self._file_menu.addSeparator()
        self._file_menu.addActions((self._save_action, self._save_as_action))
        self._file_menu.addSeparator()
        self._file_menu.addActions((self._import_action, self._export_action))

        # self._edit_menu = self._menu_bar.addMenu('&Edit')
        # self._edit_menu.addActions((self._undo_action, self._redo_action))

    def _dump(self):
        return {
            'version': 1,  # TODO: Check version
            'video_controller': self._video_controller.dump(),
            'overlay_controller': self._overlay_controller.dump(),
            'object_controller': self._object_controller.dump(),
        }

    def _load(self, data):
        self._video_controller.load(data['video_controller'])
        self._object_controller.load(data['object_controller'])
        self._overlay_controller.load(data['overlay_controller'])

    def _open_file(self):
        # Get the file path from the user
        # TODO: Decide extension
        file_name, _ = QFileDialog.getOpenFileName(
            caption='Open File',
            filter='All Files (*.*)')

        if file_name is None or file_name == '':
            return

        # Open the file
        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
        except (JSONDecodeError, UnicodeDecodeError) as e:
            return  # TODO: Display message to user about error loading JSON

        # Load the data
        self._load(data)

    def _save_file(self):
        if False:  # TODO: Check if a file has been opened before
            pass
        else:
            self._save_as_file()

    def _save_as_file(self, file_name=None):
        # TODO: Decide extension
        if not isinstance(file_name, str):
            file_name, _ = QFileDialog.getSaveFileName(
                caption='Save As',
                filter='All Files (*.*)')

        if file_name is None or file_name == '':
            return

        # Prepare the data
        data = self._dump()

        # Write the data to the file
        with open(file_name, 'w') as f:
            json.dump(data, f)


if __name__ == '__main__':
    make_dpi_aware()

    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()
