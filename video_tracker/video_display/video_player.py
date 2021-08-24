# Imports
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class VideoPlayer:
    # This would be a model
    def __init__(self):
        self._media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

    def set_video_file(self, video_file):
        """
        Sets the video file for the video player.

        :param video_file: The path to the video file
        """
        url = QUrl.fromLocalFile(video_file)
        media_content = QMediaContent(url)
        self._media_player.setMedia(media_content)

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
