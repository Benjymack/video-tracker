# Imports
from PyQt5.QtWidgets import QToolBar, QComboBox


# Classes
class ObjectSelector(QToolBar):
    def __init__(self, object_controller):
        super().__init__()

        self._object_controller = object_controller

        self._ignore_change = False

        self.addAction('New Object')
        self.addAction('Hide Calibration Ruler')
        self.addAction('Hide Reference Axes')

        self._object_list = QComboBox()
        self._object_list.currentTextChanged.connect(self._text_changed)
        self._update_object_names()

        self.addWidget(self._object_list)

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
            print('Setting object')
            self._object_controller.set_current_object(object_names[0], False)

    def update(self):
        self._update_object_names()

    def _text_changed(self, new_text):
        if not self._ignore_change:
            self._object_controller.set_current_object(new_text)
