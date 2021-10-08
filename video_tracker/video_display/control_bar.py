# Imports
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QStyle, QHBoxLayout, \
    QSlider, QSizePolicy, QSpinBox, QLineEdit, QLabel
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QIntValidator

# Constants
ICON_SIZE = QSize(16, 16)
INITIAL_NUM_CHARACTERS = 4
# TODO: Decide on font


# Classes
class ControlBar(QWidget):
    # This is another view
    def __init__(self):
        super().__init__()

        self._controller = None

        # Also based off: https://stackoverflow.com/a/57842233

        # Play/pause button
        self._play_pause_button = QPushButton()
        self._play_pause_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))

        # Scrubber
        self._scrubber = QSlider(Qt.Horizontal)
        self._scrubber.setRange(0, 0)

        # TODO: Add helpful tooltips

        # Frame decrement button
        self._frame_decrement_button = QPushButton()
        self._frame_decrement_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        # Frame increment button
        self._frame_increment_button = QPushButton()
        self._frame_increment_button.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekForward))

        # Frame display button
        self._current_position_box = QLineEdit()
        self._current_position_box.setValidator(QIntValidator())
        self._current_position_box.setMaxLength(INITIAL_NUM_CHARACTERS)
        self._current_position_box.setMaximumWidth(10 * (INITIAL_NUM_CHARACTERS + 1))

        self._divider = QLabel('/')

        # TODO: Add functionality for this being a button (change units, fps)
        self._total_length_button = QLabel()
        self._total_length_button.setMaximumWidth(10 * (INITIAL_NUM_CHARACTERS + 1))
        self._total_length_button.setSizePolicy(QSizePolicy.Fixed,
                                                QSizePolicy.MinimumExpanding)

        # Frame skip amount chooser
        self._frame_skip_amount_button = QSpinBox()
        self._frame_skip_amount_button.setMinimum(1)
        self._frame_skip_amount_button.setMaximum(10**INITIAL_NUM_CHARACTERS)

        self._layout = QHBoxLayout()
        self._layout.addWidget(self._play_pause_button)
        self._layout.addWidget(self._frame_decrement_button)
        self._layout.addWidget(self._frame_skip_amount_button)
        self._layout.addWidget(self._frame_increment_button)
        self._layout.addWidget(self._scrubber)
        self._layout.addWidget(self._current_position_box)
        self._layout.addWidget(self._divider)
        self._layout.addWidget(self._total_length_button)

        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        self._controls = (
            self._play_pause_button,
            self._frame_decrement_button,
            self._frame_increment_button,
            self._scrubber,
            self._total_length_button,
            self._current_position_box,
            self._frame_skip_amount_button,
        )

        self.set_enabled_controls(False)
        # Disable the buttons until a video is opened

    def register_controller(self, controller):
        """
        Registers a controller to the control bar.
        Expects the following methods to be defined:

            play_pause_toggle()
            position_changed(new_position)
            increment_position()
            decrement_position()
            increment_changed(new_increment)

        :param controller: The controller to connect the signals to
        """

        self._controller = controller

        self._play_pause_button.clicked.connect(controller.play_pause_toggle)
        self._scrubber.sliderMoved.connect(controller.position_changed)
        self._frame_increment_button.clicked.connect(
            controller.increment_position)
        self._frame_decrement_button.clicked.connect(
            controller.decrement_position)
        self._frame_skip_amount_button.valueChanged.connect(
            controller.increment_changed)
        self._current_position_box.textEdited.connect(
            self._position_changed)

    def _position_changed(self, new_position):
        """
        Slot for when the user has changed the current position.
        Updates the current position in the control bar, etc.

        :param new_position: The new position (units)
        """
        try:
            new_position = int(new_position)
        except ValueError:
            new_position = 0

        self._controller.position_changed(
            self._controller.position_to_ms(new_position))

    def set_enabled_controls(self, are_enabled):
        """
        Changes whether the controls (buttons, scrubber, etc) are enabled.

        :param are_enabled: The new enabled status of the controls.
        """
        for control in self._controls:
            control.setEnabled(are_enabled)

    def set_duration(self, new_duration):
        """
        Sets the duration of the scrubber bar.

        :param new_duration: The new duration (ms)
        """
        self._scrubber.setRange(0, new_duration)

        duration_unit = self._controller.ms_to_position(new_duration)

        unit_characters = len(str(duration_unit))

        self._set_position_sizes(unit_characters)

        self._total_length_button.setText(str(duration_unit))

        self._frame_skip_amount_button.setMaximum(duration_unit)

    def _set_position_sizes(self, num_characters):
        """
        Sets the reserved length of the position and duration buttons/labels.

        :param num_characters: The number of characters wide to make the items.
        """
        self._current_position_box.setMaxLength(num_characters)
        self._current_position_box.setMaximumWidth(10 * (num_characters + 1))

        self._total_length_button.setMaximumWidth(10 * (num_characters + 1))

    def set_position(self, new_position):
        """
        Sets the position of the scrubber bar.

        :param new_position: The new position (ms)
        """
        self._scrubber.setValue(new_position)
        self._current_position_box.setText(str(
            self._controller.get_current_position()))

    def set_media_state(self, new_state):
        """
        Sets the media state of the control bar (for the play/pause button)

        :param new_state: The new state to use
        """
        if new_state == QMediaPlayer.PlayingState:
            self._play_pause_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self._play_pause_button.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
