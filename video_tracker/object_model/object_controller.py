# Imports
try:
    from object_model.object_model import ObjectModel
    from object_model.object_display import ObjectDisplay
    from object_model.object_selector import ObjectSelector
except ImportError:
    from object_model import ObjectModel
    from object_display import ObjectDisplay
    from object_selector import ObjectSelector

import csv

# Constants
NUM_POINTS_TO_DISPLAY = 10


# Exceptions
class UnknownFileTypeError(Exception):
    pass


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

    def get_all_possible_measurements(self):
        possible_measurements = {}
        for o in self._objects:
            for measurement, unit in o.get_available_measurements().items():
                possible_measurements[measurement] = unit
        return possible_measurements

    def get_measurements_per_object(self):
        measurements = {}
        for o in self._objects:
            measurements[o.get_name()] = set(
                o.get_available_measurements().keys())
        return measurements

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
                              name='Object #' + str(self._current_object_id))
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

    def _get_object_by_name(self, name):
        for o in self._objects:
            if o.get_name() == name:
                return o
        return None

    def get_current_object(self):
        """
        Returns the current object (or None if it can't be found).
        """
        if self._current_object_name is None:
            return None
        else:
            return self._get_object_by_name(self._current_object_name)

    def track_current_object(self, x, y):
        """
        Adds a point to the current object at the current time.

        :param x: The x position of the point (px)
        :param y: The y position of the point (px)
        """
        self.get_current_object().add_point(
            x, y, self._video_controller.get_current_position())

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
            points.append(
                {'points': object.get_last_n_points(NUM_POINTS_TO_DISPLAY)})
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

    def export_to_file(self, data_to_export, file_name, format_):
        # Determine the data to get from the models
        data_per_object = {}
        for o, measurement in data_to_export:
            if o not in data_per_object:
                data_per_object[o] = []
            data_per_object[o].append(measurement)

        # Get the data from the models
        export_data = {
            o: self._get_object_by_name(o).get_data(*data_per_object[o])
            for o in data_per_object.keys()
        }

        # Put the data into a tabular format, more suitable for exporting
        object_measurement_to_column = {x: i for i, x in
                                        enumerate(data_to_export)}

        all_times = set()
        for o, data in export_data.items():
            all_times |= set(data.keys())

        all_times = sorted(list(all_times))

        final_data = []

        for time in all_times:
            final_data.append([None] * len(data_to_export))

            for o, data in export_data.items():
                try:
                    time_data = data[time]
                except KeyError:
                    continue

                for measurement, value in time_data.items():
                    final_data[-1][
                        object_measurement_to_column[(o, measurement)]] = value

        # Get the units of the measurements
        units = {}
        for name, measurement in data_to_export:
            object_ = self._get_object_by_name(name)

            units[(name, measurement)] = object_.get_unit(measurement)

        # Add headers
        headers = []
        for x in data_to_export:
            header = x[1]+' ('+x[0]+')'
            if units[x] is not None:
                header += ' ['+units[x]+']'
            headers.append(header)
        final_data.insert(0, headers)

        # Write the data to a file
        if format_ == 'csv':
            with open(file_name, 'w', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(final_data)
        else:
            raise UnknownFileTypeError(f'{format_} is not a known file type '
                                       f'(acceptable: csv)')

    def get_time(self, frame):
        return self._video_controller.get_time(frame)
