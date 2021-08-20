# Imports
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class VideoPlayer:
    # This would be a model
    def __init__(self):
        self._media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

    def set_video_file(self, video_file):
        url = QUrl.fromLocalFile(video_file)
        media_content = QMediaContent(url)
        self._media_player.setMedia(media_content)

    def initialise_display(self, video_display):
        self._media_player.setVideoOutput(video_display)

    def toggle_play_state(self):
        if self._media_player.state() == QMediaPlayer.PlayingState:
            self._media_player.pause()
        else:
            self._media_player.play()
