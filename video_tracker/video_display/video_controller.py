# Imports
try:
    from video_display.video_player import VideoPlayer
    from video_display.video_display import VideoDisplay
    from video_display.exceptions import UnknownUnitError, \
        NonPositiveIncrement, NonIntegerIncrement
except ImportError:
    from video_player import VideoPlayer
    from video_display import VideoDisplay
    from exceptions import UnknownUnitError, NonPositiveIncrement, \
        NonIntegerIncrement


# Classes
class VideoController:
    def __init__(self, unit='frames', skip_amount=1,
                 video_player=VideoPlayer, video_display=VideoDisplay):
        self._unit = unit
        self._skip_amount = skip_amount

        # Create the video player
        self._video_player = video_player()
        self._video_player.register_controller(self)

        # Create the video display
        self._video_display = video_display()
        self._video_display.register_controller(self)

        # Link the display and the player
        self._video_player.initialise_display(
            self._video_display.get_video_widget())

        self.set_unit(unit)
        self.increment_changed(skip_amount)

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
        print('Duration changed to:', new_duration)
        self._video_display.set_duration(new_duration)

    def position_changed(self, new_position):
        """
        Changes the current position in the video.

        :param new_position: The new position in the video
        """
        self._video_display.set_position(new_position)
        self._video_player.set_position(new_position)

    def position_to_ms(self, position, unit):
        """
        Converts a position in the specified unit to a number of milliseconds.

        :param position: The position to convert
        :param unit: The unit that the position is in (frames, ms)
        :return: The position in milliseconds (ms)
        """
        if unit == 'frames':
            return round(position / self._video_player.frame_rate * 1000)
        elif unit == 'ms':
            return position
        else:
            raise UnknownUnitError('Unit %s is unknown.' % unit)

    def ms_to_position(self, ms, unit):
        """
        Converts a position in milliseconds to a position in the specified unit.

        :param ms: The position in milliseconds (ms)
        :param unit: The unit to convert to (frames, ms)
        :return: The position in the specified unit
        """
        if unit == 'frames':
            try:
                return round(ms * self._video_player.frame_rate / 1000.0)
            except AttributeError:
                return 0
        elif unit == 'ms':
            return ms
        else:
            raise UnknownUnitError('Unit %s is unknown.' % unit)

    def get_current_position(self, unit):
        """
        Returns the current position in the specified unit.

        :param unit: The unit to return the position in (frames, ms)
        :return: The position in the specified unit
        """
        return self.ms_to_position(self._video_player.get_position(), unit)

    def _change_position(self, change, unit):
        """
        Changes the position by the specified amount in the specified unit.

        :param change: The amount to change the current position by
        :param unit: The unit of the change amount (frames, ms)
        """
        current_position = self.get_current_position(unit)

        new_position = current_position + change
        ms_position = self.position_to_ms(new_position, unit)

        self._video_player.set_position(ms_position)

    def increment_changed(self, new_increment):
        """
        Changes the amount of the increment/decrement.

        :param new_increment: The new increment/decrement value.
        """

        if new_increment <= 0:
            raise NonPositiveIncrement(f'{new_increment} is not positive.')

        if not isinstance(new_increment, int):
            raise NonIntegerIncrement(f'{new_increment} is not an integer.')

        self._skip_amount = new_increment

    def increment_position(self):
        """
        Increments the position, using the current unit, by the skip amount.
        """
        self._change_position(self._skip_amount, self._unit)

    def decrement_position(self):
        """
        Decrements the position, using the current unit, by the skip amount.
        """
        self._change_position(-self._skip_amount, self._unit)

    def set_unit(self, new_unit):
        if new_unit not in ('frames', 'ms'):  # TODO: Move this into a constant
            raise UnknownUnitError('Unit %s is unknown' % new_unit)

        self._unit = new_unit

        if self._unit == 'frames':
            interval = 100  # TODO: Move this into a constant
        else:
            interval = self.position_to_ms(1, self._unit)

        self._video_player.set_update_interval(interval)

    def get_unit(self):
        return self._unit
