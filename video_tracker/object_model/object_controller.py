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

        # TODO: Change where object selector is
        self._object_selector = ObjectSelector(self, self._overlay_controller)

    def get_object_names(self):
        """
        Returns a list of all of the names of the objects.
        """
        object_names = [o.get_name() for o in self._objects]
        return object_names

    def get_object_display(self):
        """
        Returns the object display.
        """
        return self._object_display

    def get_object_selector(self):
        """
        Returns the object selector.
        """
        return self._object_selector

    def initialise_display(self):
        """
        Initialises the object display.
        """
        self._object_display.initialise_display()

    def perform_update(self):
        """
        Updates the object display, selector and the overlay controller.
        """
        self._object_display.update()
        self._object_selector.update()
        self._overlay_controller.update()

    def create_object(self):
        """
        Creates an object, names it and returns it.

        :return: The created object.
        """
        object_ = ObjectModel(self,
                              name='Object #'+str(self._current_object_id))
        self._objects.append(object_)

        self._current_object_id += 1

        self.perform_update()

        return object_

    def set_current_object(self, object_name, perform_update=True):
        """
        Sets the current object to the one with the specified name.

        :param object_name: The name of the object to be set as the
        current object.
        :param perform_update: Whether to perform an update after setting the
        object.
        """
        self._current_object_name = object_name

        if perform_update:
            self.perform_update()

    def get_current_object(self):
        """
        Returns the current object (or None if it can't be found).
        """
        if self._current_object_name is None:
            return None
        else:
            for o in self._objects:
                if o.get_name() == self._current_object_name:
                    return o
            return None

    def track_current_object(self, x, y):
        """
        Adds a point to the current object at the current time.

        :param x: The x position of the point (px)
        :param y: The y position of the point (px)
        """
        self.get_current_object().add_point(x, y, self._video_controller.get_current_position())

    def get_ruler_length(self):
        """
        Returns the actual length, specified length and unit of the ruler.
        """
        return self._overlay_controller.get_ruler_length()

    def get_reference_angle(self):
        """
        Returns the angle of the reference axes from the horizontal (deg)
        """
        return self._overlay_controller.get_reference_angle()

    def get_origin_pos(self):
        """
        Returns the position of the reference axes origin (px).
        """
        return self._overlay_controller.get_origin_pos()

    def get_points_to_display(self):
        """
        Returns a list of points to display, for each object.
        """
        points = []
        for object in self._objects:
            points.append({'points': object.get_last_n_points(NUM_POINTS_TO_DISPLAY)})
        return points

    def get_data(self, *args):
        """
        Returns the data from the current object for the specified parameters.

        :param args: The parameters to get data for (e.g. 'x', 'vy', 'a')
        """
        current_object = self.get_current_object()
        if current_object is None:
            return None
        return current_object.get_data(*args)

    def update(self):  # TODO: Reconcile the perform_update and update methods.
        """
        Updates the object controller.
        """
        self._object_display.update()
