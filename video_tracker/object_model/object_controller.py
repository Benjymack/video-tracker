# Imports
try:
    from object_model.object_model import ObjectModel
    from object_model.object_display import ObjectDisplay
except ImportError:
    from object_model import ObjectModel
    from object_display import ObjectDisplay


# Constants
NUM_POINTS_TO_DISPLAY = 10


# Classes
class ObjectController:
    # Controller
    def __init__(self, overlay_controller, video_controller):
        self._objects = []
        self._overlay_controller = overlay_controller
        self._video_controller = video_controller

        self._object_display = ObjectDisplay()

    def get_object_display(self):
        return self._object_display

    def create_object(self):
        object_ = ObjectModel(self)
        self._objects.append(object_)
        return object_

    def _get_current_object(self):
        return self._objects[0]  # TODO: Properly determine the object

    def track_current_object(self, x, y):
        self._get_current_object().add_point(x, y, self._video_controller.get_current_position())

    def get_ruler_length(self):
        return self._overlay_controller.get_ruler_length()

    def get_origin_pos(self):
        return self._overlay_controller.get_origin_pos()

    def get_points_to_display(self):
        points = []
        for object in self._objects:
            points.append({'points': object.get_last_n_points(NUM_POINTS_TO_DISPLAY)})
        return points
