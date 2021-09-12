# Classes
class ObjectModel:
    # Model
    def __init__(self, points=None):
        if points is None:
            points = {}
        self._points = points

    def add_point(self, x, y, frame):
        self._points[frame] = (x, y)

    def get_last_n_points(self, n):
        return dict(sorted(self._points.items())[-n:])
