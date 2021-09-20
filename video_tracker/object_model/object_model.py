# Imports
from math import sin, cos, radians


# Exceptions
class InvalidMeasurementError(Exception):
    pass


# Classes
class ObjectModel:
    # Model
    def __init__(self, object_controller, points=None):
        if points is None:
            points = {}
        self._points = points
        self._object_controller = object_controller

        self._available_measurements = {
            'x': (self._get_x, lambda: self._get_len_unit()),
            'y': (self._get_y, lambda: self._get_len_unit()),
        }

    def _get_len_unit(self):
        return 'm'  # TODO: Get actual length measurement

    def add_point(self, x, y, frame):
        if not isinstance(frame, int):
            raise TypeError('Frame number must be an integer')
        self._points[frame] = (x, y)

    def _get_scale_factor(self):
        pixels, actual, unit = self._object_controller.get_ruler_length()
        return actual / pixels, unit

    def _convert_to_true_position(self, x, y):
        origin_x, origin_y = self._object_controller.get_origin_pos()

        scale = self._get_scale_factor()[0]

        ref_angle = radians(self._object_controller.get_reference_angle())

        move_x, move_y = x - origin_x, origin_y - y  # Opposite because in the
        # widget, positive y is down

        rot_x = cos(ref_angle) * move_x - sin(ref_angle) * move_y
        rot_y = sin(ref_angle) * move_x + cos(ref_angle) * move_y

        true_x = scale * rot_x
        true_y = scale * rot_y

        return true_x, true_y

    def get_last_n_points(self, n):
        return dict(sorted(self._points.items())[-n:])

    def _get_x(self):
        x_positions = {}
        for time, point in self._points.items():
            x, _ = self._convert_to_true_position(*point)
            x_positions[time] = x
        return x_positions

    def _get_y(self):
        y_positions = {}
        for time, point in self._points.items():
            _, y = self._convert_to_true_position(*point)
            y_positions[time] = y
        return y_positions

    def calculate_measurement(self, measurement):
        if measurement not in self._available_measurements:
            raise InvalidMeasurementError(f'{measurement} is not a valid '
                                          f'measurement.')
        return self._available_measurements[measurement][0]()

    def get_available_measurements(self):
        return {key: value[1]() for key, value in \
                self._available_measurements.items()}

    def get_data(self, *args):
        data = {}

        for arg in args:
            measurements = self.calculate_measurement(arg)
            for time, measurement in measurements.items():
                if time not in data:
                    data[time] = {}
                data[time][arg] = measurement

        return data
