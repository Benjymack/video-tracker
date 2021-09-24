# Imports
try:
    from object_model.object_model import ObjectModel
    from object_model.object_display import ObjectDisplay
    from object_model.object_selector import ObjectSelector
except ImportError:
    from object_model import ObjectModel
    from object_display import ObjectDisplay
    from object_selector import ObjectSelector


# Constants
NUM_POINTS_TO_DISPLAY = 10


# Classes
class ObjectController:
    # Controller
    def __init__(self, overlay_controller, video_controller):
        self._objects = []
        self._overlay_controller = overlay_controller
        self._video_controller = video_controller

        self._current_object_name = None

        self._current_object_id = 1

        self._object_display = ObjectDisplay(self)

        self._object_selector = ObjectSelector(self)

    def get_object_names(self):
        object_names = [o.get_name() for o in self._objects]
        return object_names

    def get_object_display(self):
        return self._object_display

    def get_object_selector(self):
        return self._object_selector

    def initialise_display(self):
        self._object_display.initialise_display()

    def perform_update(self):
        self._object_display.update()
        self._object_selector.update()
        self._overlay_controller.update()

    def create_object(self):
        object_ = ObjectModel(self, name=str(self._current_object_id))
        self._objects.append(object_)

        self._current_object_id += 1

        self.perform_update()

        return object_

    def set_current_object(self, object_name, perform_update=True):
        self._current_object_name = object_name

        if perform_update:
            self.perform_update()

    def get_current_object(self):
        if self._current_object_name is None:
            return None
        else:
            for o in self._objects:
                if o.get_name() == self._current_object_name:
                    return o
            return None

    def track_current_object(self, x, y):
        self.get_current_object().add_point(x, y, self._video_controller.get_current_position())

    def get_ruler_length(self):
        return self._overlay_controller.get_ruler_length()

    def get_reference_angle(self):
        return self._overlay_controller.get_reference_angle()

    def get_origin_pos(self):
        return self._overlay_controller.get_origin_pos()

    def get_points_to_display(self):
        points = []
        for object in self._objects:
            points.append({'points': object.get_last_n_points(NUM_POINTS_TO_DISPLAY)})
        return points

    def get_data(self, *args):
        current_object = self.get_current_object()
        if current_object is None:
            return None
        return current_object.get_data(*args)

    def update(self):
        self._object_display.update()
