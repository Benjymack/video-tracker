# Imports
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from pymediainfo import MediaInfo

try:
    from video_display.exceptions import TrackCountError
except ImportError:
    from exceptions import TrackCountError


# Classes
class VideoPlayer:
    # This would be a model
    def __init__(self):
        self._media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self._media_info = None

    def _process_media_info(self):
        """
        Processes the _media_info object,
        extracting the number of frames and the frame rate.
        """
        if len(self._media_info.video_tracks) != 1:
            raise TrackCountError('Invalid number of video tracks: %d' %
                                  len(self._media_info.tracks))

        track = self._media_info.video_tracks[0]

        self.frame_count = int(track.frame_count)
        self.frame_rate = float(track.frame_rate)

    def set_video_file(self, video_file):
        """
        Sets the video file for the video player.

        :param video_file: The path to the video file
        """
        url = QUrl.fromLocalFile(video_file)
        media_content = QMediaContent(url)
        self._media_player.setMedia(media_content)

        self._media_info = MediaInfo.parse(video_file)
        self._process_media_info()

    def initialise_display(self, video_display):
        """
        Sets the output of the video player to be the provided display.

        :param video_display: The display for the video
        """
        self._media_player.setVideoOutput(video_display)

    def toggle_play_state(self):
        """
        Toggles the play state from play to pause and vice versa.
        """
        if self._media_player.state() == QMediaPlayer.PlayingState:
            self._media_player.pause()
        else:
            self._media_player.play()

    def register_controller(self, controller):
        """
        Registers a controller to the video player.
        Expects the following methods to be defined:

            media_state_changed(new_state)
            position_changed(new_position)
            duration_changed(new_duration)

        :param controller: The controller to connect the signals to
        """
        self._media_player.stateChanged.connect(controller.media_state_changed)
        self._media_player.positionChanged.connect(controller.position_changed)
        self._media_player.durationChanged.connect(controller.duration_changed)
        # TODO: Connect error

    def set_position(self, new_position):
        """
        Sets the position of the video player to the specified position.

        :param new_position: The new position (ms)
        """
        self._media_player.setPosition(new_position)

    def get_position(self):
        """
        Gets the current position of the video player.

        :return: The current position (ms)
        """
        return self._media_player.position()

    def get_duration(self):
        """
        Gets the total duration of the video.

        :return: The total duration (ms)
        """
        return self._media_player.duration()

    def set_update_interval(self, interval):
        """
        Sets the notify/update interval of the video player.

        :param interval: The interval (ms)
        """
        self._media_player.setNotifyInterval(interval)
