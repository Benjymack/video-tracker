from unittest import TestCase

from video_tracker.video_display.video_player import VideoPlayer

from PyQt5.QtMultimedia import QMediaPlayer


class TestVideoPlayer(TestCase):
    def setUp(self):
        self.video_player = VideoPlayer()


class TestInit(TestVideoPlayer):
    def test_initial_media_player_type(self):
        self.assertIsInstance(self.video_player._media_player, QMediaPlayer)

    def test_initial_play_state(self):
        self.assertEqual(self.video_player._media_player.state(),
                         QMediaPlayer.StoppedState)


# TODO: Test different video formats
class TestSetVideoFile(TestVideoPlayer):
    pass


class TestToggle(TestVideoPlayer):
    pass
