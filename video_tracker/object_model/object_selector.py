# Imports
from PyQt5.QtWidgets import QToolBar, QComboBox, QAction, QLineEdit
from PyQt5.QtGui import QDoubleValidator


# Classes
class ObjectSelector(QToolBar):
    def __init__(self, object_controller, overlay_controller):
        super().__init__()

        self._object_controller = object_controller
        self._overlay_controller = overlay_controller
        self._overlay_controller.register_toolbar(self)

        self._ignore_change = False

        self._create_actions()

    def _create_actions(self):
        """
        Create and display all of the toolbar actions.
        """
        self._new_object_action = QAction('New Object')
        self._new_object_action.triggered.connect(self._create_object)
        self.addAction(self._new_object_action)

        self._object_list = QComboBox()
        self._object_list.currentTextChanged.connect(self._text_changed)
        self._update_object_names()
        self.addWidget(self._object_list)

        self.addSeparator()

        self._ruler_action = QAction('Calibration Ruler')
        self._ruler_action.setCheckable(True)
        self._ruler_action.toggled.connect(
            self._overlay_controller.set_ruler_visibility)
        self._ruler_action.setChecked(True)
        self.addAction(self._ruler_action)

        self._axes_action = QAction('Reference Axes')
        self._axes_action.setCheckable(True)
        self._axes_action.toggled.connect(
            self._overlay_controller.set_axes_visibility)
        self._axes_action.setChecked(True)
        self.addAction(self._axes_action)

        self._axes_angle = QLineEdit()
        double_validator = QDoubleValidator()
        self._axes_angle.setValidator(double_validator)
        self._axes_angle.setFixedWidth(75)
        self._axes_angle.editingFinished.connect(self._set_reference_angle)
        self._axes_angle.setText('0.0')
        self.addWidget(self._axes_angle)

        self._zoom_action = QAction('Magnifying Glass')
        self._zoom_action.setCheckable(True)
        self._zoom_action.toggled.connect(
            self._overlay_controller.set_zoom_visibility)
        self._zoom_action.setChecked(True)
        self.addAction(self._zoom_action)

        self._inc_action = QAction('Auto-Increment')
        self._inc_action.setCheckable(True)
        self._inc_action.toggled.connect(
            self._overlay_controller.set_auto_increment)
        self._inc_action.setChecked(True)
        self.addAction(self._inc_action)

    def _set_reference_angle(self):
        """
        Sets the reference angle to the one in the textbox.
        """
        angle = round(float(self._axes_angle.text()), 2)
        self._overlay_controller.set_reference_angle(-angle)
        self._axes_angle.setText(str(angle))

    def update_reference_angle(self, angle):
        """
        Changes the textbox to be the given angle.

        :param angle: The angle (deg) to set the angle textbox to.
        """
        self._axes_angle.setText(str(round(angle, 2)))

    def _create_object(self, triggered):
        """
        Creates a new object in the object controller.
        """
        self._object_controller.create_object()

    def _update_object_names(self):
        """
        Updates all of the available objects in the combobox to match the ones
        in the object controller.
        """
        self._ignore_change = True
        current_object = self._object_list.currentText()
        self._object_list.clear()
        object_names = self._object_controller.get_object_names()
        self._object_list.addItems(object_names)

        try:
            self._object_list.setCurrentIndex(object_names.index(current_object))
        except ValueError:
            pass  # The object no longer exists (it was deleted)

        self._ignore_change = False

        if self._object_controller.get_current_object() is None and \
                len(object_names) > 0:
            self._object_controller.set_current_object(object_names[0], False)

    def update(self):
        """
        Updates the toolbar.
        """
        self._update_object_names()

    def _text_changed(self, new_text):
        """
        Sets the current object to the new text.

        :param new_text: The name of the current object to set.
        """
        if not self._ignore_change:
            self._object_controller.set_current_object(new_text)
