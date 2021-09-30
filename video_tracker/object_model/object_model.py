# Imports
from math import sin, cos, radians, sqrt


# Exceptions
class InvalidMeasurementError(Exception):
    pass


# Classes
class ObjectModel:
    # Model
    def __init__(self, object_controller, points=None, name=''):
        if points is None:
            points = {}
        self._points = points
        self._object_controller = object_controller
        self._name = name

        self._available_measurements = {
            't': (self._get_t, self._get_time_unit),
            'x': (self._get_x, self._get_len_unit),
            'y': (self._get_y, self._get_len_unit),
            'r': (self._get_r, self._get_len_unit),
            'vx': (self._get_vx, self._get_vel_unit),
            'vy': (self._get_vy, self._get_vel_unit),
            'v': (self._get_v, self._get_vel_unit),
            'ax': (self._get_ax, self._get_acc_unit),
            'ay': (self._get_ay, self._get_acc_unit),
            'a': (self._get_a, self._get_acc_unit),
        }

    def get_name(self):
        return self._name

    def _get_time_unit(self):
        return 's'

    def _get_len_unit(self):
        return self._object_controller.get_ruler_length()[2]

    def _get_vel_unit(self):
        return self._get_len_unit() + '/' + self._get_time_unit()

    def _get_acc_unit(self):
        return self._get_vel_unit() + '^2'

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

    def _get_r(self):
        r_positions = {}
        for time, point in self._points.items():
            x, y = self._convert_to_true_position(*point)
            r_positions[time] = sqrt(x**2 + y**2)
        return r_positions

    def _calculate_derivative(self, points):
        d_values = {}
        prev_time, prev_p = None, None
        for time, p in points.items():
            if prev_p is None:
                d_values[time] = None
            else:
                d_values[time] = (p - prev_p)/(time - prev_time)

            prev_time, prev_p = time, p
        return d_values

    def _combine_values(self, x_points, y_points):
        values = {}

        for time, x in x_points.items():
            y = y_points[time]

            if x is None or y is None:
                values[time] = None
            else:
                values[time] = sqrt(x**2 + y**2)

        return values

    def _get_vx(self):
        return self._calculate_derivative(self._get_x())

    def _get_vy(self):
        return self._calculate_derivative(self._get_y())

    def _get_v(self):
        return self._combine_values(self._get_vx(), self._get_vy())

    def _get_ax(self):
        return self._calculate_derivative(self._get_vx())

    def _get_ay(self):
        return self._calculate_derivative(self._get_vy())

    def _get_a(self):
        return self._combine_values(self._get_ax(), self._get_ay())

    def _get_t(self):
        times = {}
        for time in self._points.keys():
            times[time] = time
        return times

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
            if arg == '':
                measurements = {time: '' for time in self._points.keys()}
            else:
                measurements = self.calculate_measurement(arg)
            for time, measurement in measurements.items():
                if time not in data:
                    data[time] = {}
                data[time][arg] = measurement

        return data
