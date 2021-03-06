from unittest import TestCase
from unittest.mock import MagicMock

from video_overlay.overlay_controller import OverlayController


class MockVideoController:
    def __init__(self):
        self.add_overlay = MagicMock()


class MockReferenceAxes:
    def __init__(self):
        self.get_origin_pos = MagicMock()
        self.register_controller = MagicMock()
        self.get_reference_angle = MagicMock()
        self.set_reference_angle = MagicMock()


class MockRuler:
    pass


class MockMagnifyingGlass:
    pass


class MockOverlayCanvas:
    def __init__(self, video_controller):
        self._reference_axes = MockReferenceAxes()
        self._ruler = MockRuler()
        self._magnifying_glass = MockMagnifyingGlass()

        self.get_reference_axes = MagicMock(return_value=self._reference_axes)
        self.get_ruler = MagicMock(return_value=self._ruler)
        self.get_magnifying_glass = MagicMock(
            return_value=self._magnifying_glass)


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

        self.overlay_controller._reference_axes.get_origin_pos. \
            assert_called_once()

    def test_get_reference_angle(self):
        self.overlay_controller.get_reference_angle()

        self.overlay_controller._reference_axes.get_reference_angle. \
            assert_called_once()

    def test_set_reference_angle(self):
        angle = 90.1
        self.overlay_controller.set_reference_angle(angle)

        self.overlay_controller._reference_axes.set_reference_angle. \
            assert_called_once_with(angle)
