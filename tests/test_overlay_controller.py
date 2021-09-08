from unittest import TestCase
from unittest.mock import MagicMock

from video_overlay.overlay_controller import OverlayController


class MockVideoController:
    def __init__(self):
        self.add_overlay = MagicMock()


class MockReferenceAxes:
    def __init__(self):
        self.get_origin_pos = MagicMock()


class MockRuler:
    def __init__(self):
        pass


class MockOverlayCanvas:
    def __init__(self):
        self._reference_axes = MockReferenceAxes()
        self._ruler = MockRuler()

        self.get_reference_axes = MagicMock(return_value=self._reference_axes)
        self.get_ruler = MagicMock(return_value=self._ruler)


def create_test_controller():
    video_controller = MockVideoController()
    overlay_controller = OverlayController(video_controller, MockOverlayCanvas)
    return video_controller, overlay_controller


class TestOverlayController(TestCase):
    def setUp(self):
        self.video_controller, self.overlay_controller = create_test_controller()


class TestOverlayControllerInitialisation(TestCase):
    def test_overlay_call(self):
        video, overlay = create_test_controller()
        video.add_overlay.assert_called_once_with(overlay._overlay_canvas,
                                                  overlay._mouse_press,
                                                  overlay._mouse_move,
                                                  overlay._mouse_release)


class TestOverlayControllerFunctions(TestOverlayController):
    def test_get_origin_pos(self):
        self.overlay_controller.get_origin_pos()
