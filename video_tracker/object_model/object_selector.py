# Imports
from PyQt5.QtWidgets import QToolBar, QComboBox


# Classes
class ObjectSelector(QToolBar):
    def __init__(self, object_controller):
        super().__init__()

        self._object_controller = object_controller

        self.addAction('New Object')
        self.addAction('Hide Calibration Ruler')
        self.addAction('Hide Reference Axes')

        self._object_list = QComboBox()
        self._update_object_names()

        self.addWidget(self._object_list)

    def _update_object_names(self):
        self._object_list.addItems(self._object_controller.get_object_names())

    def update(self):
        print('Object selector updating')
        self._update_object_names()
