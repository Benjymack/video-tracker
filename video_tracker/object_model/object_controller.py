# Imports
try:
    from object_model.object_model import ObjectModel
except ImportError:
    from object_model import ObjectModel


# Classes
class ObjectController:
    # Controller
    def __init__(self, overlay_controller):
        self._objects = []
        self._overlay_controller = overlay_controller

    def create_object(self):
        object_ = ObjectModel(self)
        self._objects.append(object_)
        return object_

    def _get_current_object(self):
        return self._objects[0]  # TODO: Properly determine the object

    def track_current_object(self, pos):
        print(pos)
        print(self._get_current_object())

    def get_ruler_length(self):
        return self._overlay_controller.get_ruler_length()

    def get_origin_pos(self):
        return self._overlay_controller.get_origin_pos()
