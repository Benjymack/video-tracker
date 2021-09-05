# Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsLineItem
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtCore import QSizeF, Qt, QSize

try:
    from video_display.control_bar import ControlBar
    from video_display.graphics_scene import GraphicsScene
except ImportError:
    from control_bar import ControlBar
    from graphics_scene import GraphicsScene


# Constants
SIZE_HINT = QSize(640, 480)


class VideoDisplay(QWidget):
    # This would be a view
    def __init__(self):
        super().__init__()

        # Based off: https://stackoverflow.com/a/57842233

        # Create the video
        self._video_widget = QGraphicsVideoItem()
        self._video_widget.nativeSizeChanged.connect(self._native_size_changed)

        self._scene = GraphicsScene(self)
        self._view = QGraphicsView(self._scene)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._scene.addItem(self._video_widget)

        # Create the control bar
        self._control_bar = ControlBar()

        # Create the layout
        self._layout = QVBoxLayout()
        self._layout.addWidget(self._view)
        self._layout.addWidget(self._control_bar)
        self.setLayout(self._layout)

    def _native_size_changed(self, size):
        if size.isEmpty():
            return  # Stop weird issue with it not being centered if we
            # scale an empty QSizeF
        size.scale(SIZE_HINT.width(), SIZE_HINT.height(), Qt.KeepAspectRatio)
        self._video_widget.setSize(size)
        self.resizeEvent(None)

    def add_overlay(self, overlay, mouse_press, mouse_move, mouse_release):
        self._scene.addItem(overlay)
        self._scene.set_functions(mouse_press, mouse_move, mouse_release)

    def sizeHint(self):
        return SIZE_HINT

    def resizeEvent(self, event):
        self._view.fitInView(self._video_widget, Qt.KeepAspectRatio)
        print(self._video_widget.size())

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
