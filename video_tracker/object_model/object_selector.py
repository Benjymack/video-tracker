# Imports
from PyQt5.QtWidgets import QToolBar, QComboBox, QAction


# Classes
class ObjectSelector(QToolBar):
    def __init__(self, object_controller, overlay_controller):
        super().__init__()

        self._object_controller = object_controller
        self._overlay_controller = overlay_controller

        self._ignore_change = False

        self._create_actions()

        self._object_list = QComboBox()
        self._object_list.currentTextChanged.connect(self._text_changed)
        self._update_object_names()

        self.addWidget(self._object_list)

    def _create_actions(self):
        self._new_object_action = QAction('New Object')
        self._new_object_action.triggered.connect(self._create_object)
        self.addAction(self._new_object_action)

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

    def _create_object(self, triggered):
        self._object_controller.create_object()

    def _update_object_names(self):
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
        self._update_object_names()

    def _text_changed(self, new_text):
        if not self._ignore_change:
            self._object_controller.set_current_object(new_text)
