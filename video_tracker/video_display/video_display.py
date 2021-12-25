# Imports
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtCore import Qt, QSize, QRectF

try:
    from video_display.control_bar import ControlBar
    from video_display.graphics_scene import GraphicsScene
    from video_display.video_view import VideoView
except ImportError:
    from control_bar import ControlBar
    from graphics_scene import GraphicsScene
    from video_view import VideoView


# Constants
SIZE_HINT = QSize(640, 480)


class VideoDisplay(QWidget):
    # This would be a view
    def __init__(self):
        super().__init__()

        self._mouse_press = lambda event: None
        self._mouse_release = lambda event: None

        # Create the video
        self._video_widget = QGraphicsVideoItem()
        self._video_widget.nativeSizeChanged.connect(self._native_size_changed)

        self._scene = GraphicsScene(self)
        self._view = VideoView(self._scene)
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

        self._layout.setContentsMargins(0, 0, 0, 0)

        # Set the default scene size to avoid issues with cursor movements
        # expanding the scene
        self._scene.setSceneRect(
            QRectF(0, 0, SIZE_HINT.width(), SIZE_HINT.height()))

    def _native_size_changed(self, size):
        """
        Rescale the video if the native size of the video is changed.

        :param size: The native size of the video
        """
        if size.isEmpty():
            return  # Stop weird issue with it not being centered if we
            # scale an empty QSizeF
        size.scale(SIZE_HINT.width(), SIZE_HINT.height(), Qt.KeepAspectRatio)
        self._video_widget.setSize(size)
        self.resizeEvent(None)

        self._scene.setSceneRect(QRectF(0, 0, size.width(), size.height()))

    def add_overlay(self, overlay, mouse_press, mouse_move, mouse_release):
        """
        Adds an overlay to the video display, as well as binding the mouse
        press, movement and release events to the provided functions.

        :param overlay: The overlay (QGraphicsItem) to add
        :param mouse_press: Function for when the mouse is pressed on the scene.
        :param mouse_move: Function for when the mouse is moved on the scene.
        :param mouse_release: Function for when the mouse is released on the
        scene.
        """
        self._scene.addItem(overlay)
        self._mouse_press = mouse_press
        self._scene.set_move_function(mouse_move)
        self._mouse_release = mouse_release

    def sizeHint(self):
        """
        Returns the size hint of the video display.
        """
        return SIZE_HINT

    def resizeEvent(self, event):
        """
        When the video display is resized, fit the video into the view.
        """
        self._view.fitInView(self._video_widget, Qt.KeepAspectRatio)

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

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        # TODO: Make it more obvious that I am overriding this
        event.scenePos = lambda evt=event: self.get_scene_pos(evt.pos())
        self._mouse_press(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        event.scenePos = lambda evt=event: self.get_scene_pos(evt.pos())
        self._mouse_release(event)

    def get_scene_pos(self, pos):
        return self._view.mapToScene(pos)
