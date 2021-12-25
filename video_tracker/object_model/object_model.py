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
            'frame': (self._get_frame, lambda: None),
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
        """
        Returns the name of the object.
        """
        return self._name

    def _get_time_unit(self):
        """
        Returns the unit of time (s).
        """
        return 's'

    def _get_len_unit(self):
        """
        Returns the unit of length.
        """
        return self._object_controller.get_ruler_length()[2]

    def _get_vel_unit(self):
        """
        Returns the unit of velocity.
        """
        return self._get_len_unit() + '/' + self._get_time_unit()

    def _get_acc_unit(self):
        """
        Returns the unit of acceleration.
        """
        return self._get_vel_unit() + '^2'

    def get_unit(self, measurement):
        return self._available_measurements[measurement][1]()

    def add_point(self, x, y, frame):
        """
        Adds (or changes) a point in the model, setting the one at the specified
        frame to the given x and y coordinates.

        :param x: x-coordinate of the point (px)
        :param y: y-coordinate of the point (px)
        :param frame: frame number
        """
        if not isinstance(frame, int):
            raise TypeError('Frame number must be an integer')
        self._points[frame] = (x, y)

    def _get_scale_factor(self):
        """
        Returns the scale factor (actual length / pixel distance) and
        the user-specified unit
        """
        pixels, actual, unit = self._object_controller.get_ruler_length()
        return actual / pixels, unit

    def _convert_to_true_position(self, x, y):
        """
        Converts the given position (px) to the actual position (length unit).

        :param x: x-coordinate of the position
        :param y: y-coordinate of the position
        :return: x and y coordinates of the true position
        """
        origin_x, origin_y = self._object_controller.get_origin_pos()

        scale = self._get_scale_factor()[0]

        ref_angle = radians(self._object_controller.get_reference_angle())

        move_x, move_y = x - origin_x, origin_y - y  # Opposite because in the
        # overlay widget, positive y is down, but we want positive y to be up

        rot_x = cos(ref_angle) * move_x - sin(ref_angle) * move_y
        rot_y = sin(ref_angle) * move_x + cos(ref_angle) * move_y

        true_x = scale * rot_x
        true_y = scale * rot_y

        return true_x, true_y

    def get_last_n_points(self, n):
        """
        Returns the last n points, based on the frame numbers.

        :param n: How many points to return.
        """
        return dict(sorted(self._points.items())[-n:])

    def _get_x(self):
        """
        Calculates and returns the actual x positions of all of the points.

        :return: A dict of the frames and the actual x positions.
        """
        x_positions = {}
        for frame, point in sorted(self._points.items()):
            x, _ = self._convert_to_true_position(*point)
            x_positions[frame] = x
        return x_positions

    def _get_y(self):
        """
        Calculates and returns the actual y positions of all of the points.

        :return: A dict of the frames and the actual y positions.
        """
        y_positions = {}
        for frame, point in sorted(self._points.items()):
            _, y = self._convert_to_true_position(*point)
            y_positions[frame] = y
        return y_positions

    def _calculate_derivative(self, points):
        """
        Calculates and returns the derivative (or at least approximates it),
        of the given points.

        The first point will be None, as two points are required to calculate
        the derivative.

        :param points: The x and y values of the points.
        :return: The x and y derivatives of the points.
        """
        d_values = {}
        prev_time, prev_p = None, None

        for frame, p in points.items():
            time = self._get_time(frame)
            if prev_p is None:
                d_values[frame] = None
            else:
                d_values[frame] = (p - prev_p) / (time - prev_time)

            prev_time, prev_p = time, p
        return d_values

    def _combine_values(self, x_points, y_points):
        """
        Combines a series of x values and y values into a magnitude value.
        This uses Pythagoras's Theorem on each x,y pair.

        :param x_points: The x positions of the points.
        :param y_points: The y positions of the points.
        :return: The magnitude of the points.
        """
        values = {}

        for frame, x in x_points.items():
            y = y_points[frame]

            if x is None or y is None:
                values[frame] = None
            else:
                values[frame] = sqrt(x ** 2 + y ** 2)

        return values

    def _get_r(self):
        """
        Returns the magnitude of the positions.
        """
        return self._combine_values(self._get_x(), self._get_y())

    def _get_vx(self):
        """
        Returns the x component of the velocity.
        """
        return self._calculate_derivative(self._get_x())

    def _get_vy(self):
        """
        Returns the y component of the velocity.
        """
        return self._calculate_derivative(self._get_y())

    def _get_v(self):
        """
        Returns the magnitude of the velocity.
        """
        return self._combine_values(self._get_vx(), self._get_vy())

    def _get_ax(self):
        """
        Returns the x component of the acceleration.
        """
        return self._calculate_derivative(self._get_vx())

    def _get_ay(self):
        """
        Returns the y component of the acceleration.
        """
        return self._calculate_derivative(self._get_vy())

    def _get_a(self):
        """
        Returns the magnitude of the acceleration.
        """
        return self._combine_values(self._get_ax(), self._get_ay())

    def _get_t(self):
        """
        Returns all of the times, each assigned to the time.
        """
        times = {}
        for frame in sorted(self._points.keys()):
            times[frame] = self._get_time(frame)
        return times

    def _get_frame(self):
        frames = {}
        for frame in sorted(self._points.keys()):
            frames[frame] = frame
        return frames

    def calculate_measurement(self, measurement):
        """
        Returns a given measurement for all of the points.

        :param measurement: The measurement to calculate,
        must be one of the available measurements.
        """
        if measurement not in self._available_measurements:
            raise InvalidMeasurementError(f'{measurement} is not a valid '
                                          f'measurement.')
        return self._available_measurements[measurement][0]()

    def get_available_measurements(self):
        """
        Returns all of the available measurements, and their units.
        """
        return {key: value[1]() for key, value in
                self._available_measurements.items()}

    def get_data(self, *args):
        """
        Returns the data for the provided measurements.

        :param args: The measurements to calculate and return.
        :return: A dict of the measurement names and the calculated data.
        """
        data = {}

        for arg in args:
            if arg == '':
                measurements = {frame: '' for frame in sorted(self._points.keys())}
            else:
                measurements = self.calculate_measurement(arg)
            for frame, measurement in measurements.items():
                if frame not in data:
                    data[frame] = {}
                data[frame][arg] = measurement

        return data

    def _get_time(self, frame):
        return self._object_controller.get_time(frame)

    def load(self, data):
        self._points = {int(k): v for k, v in data['points'].items()}
        self._name = data['name']

    def dump(self):
        return {
            'points': self._points,
            'name': self._name,
        }
