# Imports
from video_player import VideoPlayer
from video_display import VideoDisplay


# Classes
class VideoController:
    def __init__(self):
        # Create the video player
        self._video_player = VideoPlayer()

        # Create the video display
        self._video_display = VideoDisplay()

        # Link the display and the player
        self._video_player.initialise_display(self._video_display._video_widget)

    def get_video_display(self):
        return self._video_display

    def open_video_file(self, video_file):
        self._video_player.set_video_file(video_file)

    def toggle_play_state(self):
        self._video_player.toggle_play_state()
