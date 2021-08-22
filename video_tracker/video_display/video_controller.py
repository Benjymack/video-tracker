# Imports
from video_player import VideoPlayer
from video_display import VideoDisplay


# Classes
class VideoController:
    def __init__(self):
        # Create the video player
        self._video_player = VideoPlayer()
        self._video_player.register_controller(self)

        # Create the video display
        self._video_display = VideoDisplay()
        self._video_display.register_controller(self)

        # Link the display and the player
        self._video_player.initialise_display(self._video_display._video_widget)

    def get_video_display(self):
        return self._video_display

    def open_video_file(self, video_file):
        self._video_player.set_video_file(video_file)
        self._video_display.enable_controls()

    def play_pause_toggle(self):
        self._video_player.toggle_play_state()

    def media_state_changed(self, new_state):
        print('State changed to:', new_state)
        self._video_display.set_media_state(new_state)

    def duration_changed(self, new_duration):
        print('Duration changed to:', new_duration)
        self._video_display.set_duration(new_duration)

    def position_changed(self, new_position):
        print('Position changed to:', new_position)
        self._video_display.set_position(new_position)
        self._video_player.set_position(new_position)
