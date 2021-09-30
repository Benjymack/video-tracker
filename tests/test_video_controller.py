from unittest import TestCase
from unittest.mock import MagicMock

from video_display.video_controller import VideoController
from video_display.exceptions import BadIncrement, UnknownUnitError, \
    NonPositiveIncrement, NonIntegerIncrement


class MockVideoWidget:
    pass


MOCK_VIDEO_WIDGET = MockVideoWidget()


class MockVideoPlayer:
    def __init__(self):
        self.register_controller = MagicMock()
        self.initialise_display = MagicMock()
        self.set_update_interval = MagicMock()
        self.toggle_play_state = MagicMock()
        self.set_video_file = MagicMock()

        self._position = 0
        self.frame_rate = 1

    def get_position(self):
        return self._position

    def set_position(self, new_position):
        self._position = new_position

    def get_duration(self):
        return 10000  # 10 seconds (1fps => 10 frames)


class MockVideoDisplay:
    def __init__(self):
        self.register_controller = MagicMock()
        self.get_video_widget = MagicMock(return_value=MOCK_VIDEO_WIDGET)
        self.set_media_state = MagicMock()
        self.enable_controls = MagicMock()


def create_test_controller(*args, **kwargs):
    kwargs['video_player'] = MockVideoPlayer
    kwargs['video_display'] = MockVideoDisplay
    return VideoController(*args, **kwargs)


class TestVideoController(TestCase):
    def setUp(self):
        self.video_controller = create_test_controller()


class TestVideoControllerInitialisation(TestCase):
    def test_frames_unit(self):
        try:
            create_test_controller('frames')
        except UnknownUnitError:
            self.fail('UnknownUnitError: frames')

    def test_ms_unit(self):
        try:
            create_test_controller('ms')
        except UnknownUnitError:
            self.fail('UnknownUnitError: ms')

    def test_unknown_unit(self):
        self.assertRaises(UnknownUnitError, create_test_controller, 'unknown')

    def test_blank_unit(self):
        self.assertRaises(UnknownUnitError, create_test_controller, '')

    def test_zero_skip(self):
        self.assertRaises(NonPositiveIncrement, create_test_controller,
                          skip_amount=0)

    def test_negative_skip(self):
        self.assertRaises(NonPositiveIncrement, create_test_controller,
                          skip_amount=-1)

    def test_one_skip(self):
        try:
            create_test_controller(skip_amount=1)
        except BadIncrement:
            self.fail('BadIncrement: 1')

    def test_large_skip(self):
        try:
            create_test_controller(skip_amount=1000)
        except BadIncrement:
            self.fail('BadIncrement: 1')

    def test_positive_float_skip(self):
        self.assertRaises(NonIntegerIncrement, create_test_controller,
                          skip_amount=1.1)

    def test_negative_float_skip(self):
        self.assertRaises(BadIncrement, create_test_controller,
                          skip_amount=-2.2)

    def test_skip_to_zero(self):
        controller = create_test_controller()
        controller.increment_position()
        controller.decrement_position()

        self.assertEqual(controller.get_current_position(), 0)

    def test_skip_to_negative(self):
        controller = create_test_controller()
        controller.decrement_position()

        self.assertEqual(0, controller.get_current_position())

    def test_skip_to_duration(self):
        controller = create_test_controller()

        for _ in range(10):
            controller.increment_position()

        self.assertEqual(10, controller.get_current_position())

    def test_skip_beyond_duration(self):
        controller = create_test_controller()

        for _ in range(11):
            controller.increment_position()

        self.assertEqual(10, controller.get_current_position())

    def test_functions_called_init(self):
        controller = create_test_controller()
        video_player = controller._video_player
        video_display = controller._video_display

        # Check whether VideoController calls register_controller
        video_player.register_controller.assert_called_once_with(controller)
        video_display.register_controller.assert_called_once_with(controller)

        video_player.initialise_display.assert_called_once_with(
            MOCK_VIDEO_WIDGET)


class TestVideoControllerFunctions(TestVideoController):
    def test_get_video_display(self):
        self.assertIs(self.video_controller._video_display,
                      self.video_controller.get_video_display())

    def test_get_video_widget(self):
        self.assertIs(self.video_controller._video_display.get_video_widget(),
                      self.video_controller.get_video_widget())

    def test_play_pause_toggle(self):
        self.video_controller.play_pause_toggle()
        self.video_controller._video_player.toggle_play_state.\
            assert_called_once()

    def test_media_state_changed(self):
        for new_state in range(3):
            self.video_controller.media_state_changed(new_state)
            self.video_controller._video_display.set_media_state.\
                assert_called_with(new_state)

    def test_open_video_file(self):
        file_path = 'C:/thing/video.mp4'
        self.video_controller.open_video_file(file_path)
        self.video_controller._video_player.set_video_file.assert_called_with(
            file_path)
        self.video_controller._video_display.enable_controls.assert_called()


