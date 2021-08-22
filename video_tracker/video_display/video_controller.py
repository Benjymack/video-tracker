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
        """
        Returns the video display.
        """
        return self._video_display

    def open_video_file(self, video_file):
        """
        Opens a video file, and displays it.

        :param video_file: The path to the video file to open
        """
        self._video_player.set_video_file(video_file)
        self._video_display.enable_controls()

    def play_pause_toggle(self):
        """
        Toggles between playing and pausing the current video.
        """
        self._video_player.toggle_play_state()
        # TODO: Return the new status?

    def media_state_changed(self, new_state):
        """
        Changes the media state of the video.

        :param new_state: The new state of the video
        """
        print('State changed to:', new_state)
        self._video_display.set_media_state(new_state)

    def duration_changed(self, new_duration):
        """
        Changes the duration of the video.

        :param new_duration: The new duration of the video
        """
        # TODO: Decide when to convert between current units and frames
        print('Duration changed to:', new_duration)
        self._video_display.set_duration(new_duration)

    def position_changed(self, new_position):
        """
        Changes the current position in the video.

        :param new_position: The new position in the video
        """
        # TODO: Decide when to convert between current units and frames
        print('Position changed to:', new_position)
        self._video_display.set_position(new_position)
        self._video_player.set_position(new_position)
