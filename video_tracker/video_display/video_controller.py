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

        self._fps = 1
        self._frame_offset = 0
        self._time_offset = 0.0

        self._object_controller = None

        self.ignore_changes = False

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

    def get_video_player(self):
        """
        Returns the video player.
        """
        return self._video_player

    def get_video_display(self):
        """
        Returns the video display.
        """
        return self._video_display

    def get_video_widget(self):
        """
        Returns the video widget.
        """
        return self._video_display.get_video_widget()

    def add_overlay(self, overlay, mouse_press, mouse_move, mouse_release):
        """
        Adds an overlay to the video display, as well as binding the mouse
        press, movement and release events to the provided functions.

        :param overlay: The overlay (QGraphicsItem) to add
        :param mouse_press: Function for when the mouse is pressed on the scene.
        :param mouse_move: Function for when the mouse is moved on the scene.
        :param mouse_release: Function for when the mouse is released on the
        scene.
        """
        self._video_display.add_overlay(overlay, mouse_press, mouse_move,
                                        mouse_release)

    def open_video_file(self, video_file):
        """
        Opens a video file, and displays it.

        :param video_file: The path to the video file to open
        """
        self._video_player.set_video_file(video_file)
        self._video_display.enable_controls()
        self.set_fps(self._video_player.frame_rate)

        # Display the first frame of the video, as it doesn't display without
        # 'playing' the video
        self.play_pause_toggle()
        self.play_pause_toggle()

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
        if self.ignore_changes:
            return

        self.ignore_changes = True
        self._video_display.set_media_state(new_state)
        self.ignore_changes = False

    def duration_changed(self, new_duration):
        """
        Changes the duration of the video.

        :param new_duration: The new duration of the video (ms)
        """
        if self.ignore_changes:
            return

        self.ignore_changes = True
        self._video_display.set_duration(new_duration)
        self.ignore_changes = False

    def position_changed(self, new_position):
        """
        Changes the current position in the video.

        :param new_position: The new position in the video
        """
        if self.ignore_changes:
            return

        if new_position < 0:
            new_position = 0

        if new_position > self._video_player.get_duration():
            new_position = self._video_player.get_duration()

        self.ignore_changes = True
        self._video_display.set_position(new_position)
        self._video_player.set_position(new_position)
        self.ignore_changes = False

    def position_to_ms(self, position, unit=None):
        """
        Converts a position in the specified unit to a number of milliseconds.

        :param position: The position to convert
        :param unit: The unit that the position is in (frames, ms).
        Default: current unit
        :return: The position in milliseconds (ms)
        """

        if unit is None:
            unit = self.get_unit()

        if unit == 'frames':
            # This has to be int() rather than round(), otherwise there are
            # issues with frames being skipped, and others doubled, as when
            # PyQt5 converts the ms back to frames, it floors.
            return int(position / self._video_player.frame_rate * 1000)
        elif unit == 'ms':
            return position
        else:
            raise UnknownUnitError('Unit %s is unknown.' % unit)

    def ms_to_position(self, ms, unit=None):
        """
        Converts a position in milliseconds to a position in the specified unit.

        :param ms: The position in milliseconds (ms)
        :param unit: The unit to convert to (frames, ms)
        Default: current unit
        :return: The position in the specified unit
        """

        if unit is None:
            unit = self.get_unit()

        if unit == 'frames':
            try:
                return round(ms * self._video_player.frame_rate / 1000.0)
            except AttributeError:
                return 0
        elif unit == 'ms':
            return ms
        else:
            raise UnknownUnitError('Unit %s is unknown.' % unit)

    def get_current_position(self, unit=None):
        """
        Returns the current position in the specified unit.

        :param unit: The unit to return the position in (frames, ms)
        Default: current unit
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

        self._set_position(new_position, unit)

    def _set_position(self, new_position, unit):
        ms_position = self.position_to_ms(new_position, unit)

        if ms_position < 0:
            ms_position = 0

        if ms_position > self._video_player.get_duration():
            ms_position = self._video_player.get_duration()

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
        """
        Sets the current unit to be the one specified (frames, ms)
        """
        if new_unit not in ('frames', 'ms'):  # TODO: Move this into a constant
            raise UnknownUnitError('Unit %s is unknown' % new_unit)

        self._unit = new_unit

        if self._unit == 'frames':
            interval = 100  # TODO: Move this into a constant
        else:
            interval = self.position_to_ms(1, self._unit)

        self._video_player.set_update_interval(interval)

    def get_unit(self):
        """
        Returns the current unit.
        """
        return self._unit

    def is_video_imported(self):
        """
        Returns whether or not a video has been imported.
        """
        return self._video_player.is_video_imported()

    def get_time(self, frame):
        return (frame - self._frame_offset)/self._fps + self._time_offset

    def get_fps(self):
        return self._fps

    def set_time(self, frame, time):
        self._frame_offset = frame
        self._time_offset = time
        if self._object_controller is not None:
            self._object_controller.update()

    def set_fps(self, fps):
        self._fps = fps
        if self._object_controller is not None:
            self._object_controller.update()

    def set_object_controller(self, object_controller):
        self._object_controller = object_controller

    def load(self, data):
        self.open_video_file(data['video_file'])
        self.set_unit(data['unit'])
        self.set_fps(data['fps'])
        self._skip_amount = data['skip_amount']
        self.set_time(data['frame_offset'], data['time_offset'])
        self._set_position(data['current_frame'], 'frames')

    def dump(self):
        return {
            'unit': self._unit,
            'fps': self._fps,
            'skip_amount': self._skip_amount,
            'frame_offset': self._frame_offset,
            'time_offset': self._time_offset,
            'video_file': self._video_player.get_video_file(),
            'current_frame': self.get_current_position('frames'),
        }
