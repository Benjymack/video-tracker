# Imports
try:
    from video_overlay.overlay_canvas import OverlayCanvas
except ImportError:
    from overlay_canvas import OverlayCanvas

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


# Classes
class OverlayController:
    # Controller
    def __init__(self, video_controller, overlay_canvas=OverlayCanvas):
        self._object_controller = None
        self._video_controller = video_controller

        # Create the overlay canvas
        self._overlay_canvas = overlay_canvas(self._video_controller)
        self._video_controller.add_overlay(self._overlay_canvas,
                                           self._mouse_press, self._mouse_move,
                                           self._mouse_release)

        self._reference_axes = self._overlay_canvas.get_reference_axes()
        self._reference_axes.register_controller(self)
        self._ruler = self._overlay_canvas.get_ruler()
        self._magnifying_glass = self._overlay_canvas.get_magnifying_glass()

        self._overlay_items = (
            self._reference_axes,
            self._ruler,
            self._magnifying_glass,
        )

        self._auto_increment = False
        self._toolbar = None

    def get_magnifying_glass(self):
        """
        Returns the magnifying glass.
        """
        return self._magnifying_glass

    def get_origin_pos(self):
        """
        Returns the position of the origin in pixels.
        """
        return self._reference_axes.get_origin_pos()

    def get_reference_angle(self):
        """
        Returns the reference angle.
        (0-360 degrees going counter-clockwise from right horizontal).
        """
        return self._reference_axes.get_reference_angle()

    def set_reference_angle(self, angle):
        """
        Sets the reference angle of the axes to the specified angle (deg).
        """
        self._reference_axes.set_reference_angle(angle)

    def update_reference_angle(self, angle):
        """
        Updates the reference angle in the toolbar to the specified angle (deg).
        """
        if self._toolbar is not None:
            self._toolbar.update_reference_angle(angle)

    def register_toolbar(self, toolbar):
        """
        Registers the given toolbar.
        """
        self._toolbar = toolbar

    def _find_items_containing(self, pos):
        """
        Yields any of the overlay items that contain the supplied position.

        :param pos: The position (QPointF) to use.
        :return: A generator of the items that contain the position.
        """
        for item in self._overlay_items:
            yield item

    def _mouse_press(self, event):
        """
        Pass the mouse press down to any overlay items that are there,
        or otherwise tracks the current point.
        """

        if not self._video_controller.is_video_imported():
            return

        anything_done = False
        for item in self._find_items_containing(event.scenePos()):
            anything_done |= item.mouse_press(event)

        if not anything_done and event.button() == Qt.LeftButton and \
                self._object_controller is not None and \
                self._video_controller.is_video_imported():
            # Track the object
            self._object_controller.track_current_object(event.scenePos().x(), event.scenePos().y())

            # Update the overlay
            self.update()

            # Increment the video if applicable
            if self._auto_increment:
                self._video_controller.increment_position()

        if anything_done:
            self.update(False)

    def _mouse_move(self, event):
        """
        Pass the mouse movement down to any containing overlay items.
        """

        if not self._video_controller.is_video_imported():
            return

        anything_done = False
        for item in self._find_items_containing(event.scenePos()):
            anything_done |= item.mouse_move(event)

        if anything_done:
            self.update(False)

    def _mouse_release(self, event):
        """
        Pass the mouse release down to any containing overlay items.
        """

        if not self._video_controller.is_video_imported():
            return

        anything_done = False
        for item in self._find_items_containing(event.scenePos()):
            anything_done |= item.mouse_release(event)

        if anything_done:
            self.update(False)

    def get_ruler_length(self):
        """
        Returns the pixel length of the ruler,
        as well as the user-specified length and unit.
        """
        return self._ruler.get_ruler_length()

    def set_object_controller(self, object_controller):
        """
        Registers an object controller to the overlay controller.
        """
        self._object_controller = object_controller

    def _display_object_points(self):
        """
        Displays the recent points of the objects on the overlay.
        """
        if self._object_controller is not None:
            object_points = self._object_controller.get_points_to_display()

            colour = QColor()
            colour.setRgb(255, 0, 0)

            self._overlay_canvas.clear_points()
            for object in object_points:
                for point_id, point in object['points'].items():
                    self._overlay_canvas.draw_point(*point, colour)

    def update(self, redisplay_points=True):
        """
        Redisplays the points and updates the object controller.

        :param redisplay_points: Whether to redisplay the points.
        """
        if redisplay_points:
            self._display_object_points()

        if self._object_controller is not None:
            self._object_controller.update()

    def set_ruler_visibility(self, visibility):
        """
        Sets the visibility of the ruler to the given value.
        """
        self._overlay_canvas.set_ruler_visibility(visibility)

    def set_axes_visibility(self, visibility):
        """
        Sets the visibility of the reference axes to the given value.
        """
        self._overlay_canvas.set_axes_visibility(visibility)

    def set_zoom_visibility(self, visibility):
        """
        Sets the visibility of the magnifying glass to the given value.
        """
        self._overlay_canvas.set_zoom_visibility(visibility)

    def set_auto_increment(self, value):
        """
        Sets whether to auto-increment when a user tracks a point or not.

        :param value: Whether to auto-increment or not
        """
        self._auto_increment = value

    def load(self, data):
        self._reference_axes.load(data['reference_axes'])
        self._ruler.load(data['ruler'])
        self._magnifying_glass.load(data['magnifying_glass'])
        self.set_auto_increment(data['auto_increment'])
        self.update()
        # TODO: Might have to update the toolbar

    def dump(self):
        return {
            'reference_axes': self._reference_axes.dump(),
            'ruler': self._ruler.dump(),
            'magnifying_glass': self._magnifying_glass.dump(),
            'auto_increment': self._auto_increment,
        }
