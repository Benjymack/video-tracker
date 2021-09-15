# Classes
class ObjectModel:
    # Model
    def __init__(self, object_controller, points=None):
        if points is None:
            points = {}
        self._points = points
        self._object_controller = object_controller

    def add_point(self, x, y, frame):
        if not isinstance(frame, int):
            raise TypeError('Frame number must be an integer')
        self._points[frame] = (x, y)

    def _get_scale_factor(self):
        pixels, actual, unit = self._object_controller.get_ruler_length()
        return actual / pixels, unit

    def _convert_to_true_position(self, x, y):
        # TODO: Account for reference angle
        origin_x, origin_y = self._object_controller.get_origin_pos()

        scale = self._get_scale_factor()[0]

        true_x = scale * (x - origin_x)
        true_y = scale * (y - origin_y)

        return true_x, true_y

    def get_last_n_points(self, n):
        return dict(sorted(self._points.items())[-n:])
