# Imports
try:
    from object_model.object_graph import ObjectGraph
    from object_model.object_table import ObjectTable
except ImportError:
    from object_graph import ObjectGraph
    from object_table import ObjectTable

from PyQt5.QtWidgets import QSplitter
from PyQt5.QtCore import Qt


# Classes
class ObjectDisplay(QSplitter):
    def __init__(self, object_controller):
        super().__init__()

        self._object_controller = object_controller

        self._object_graph = ObjectGraph(self)
        self._object_table = ObjectTable(self)

        self.setOrientation(Qt.Vertical)
        self.addWidget(self._object_graph)
        self.addWidget(self._object_table)

        equal_height = max(self._object_graph.minimumSizeHint().height(),
                           self._object_table.minimumSizeHint().height())

        self.setSizes([1, equal_height])

    def get_current_object(self):
        return self._object_controller.get_current_object()

    def get_current_object_available_measurements(self):
        current_object = self.get_current_object()
        if current_object is None:
            return {}
        return current_object.get_available_measurements()

    def initialise_display(self):
        self._object_graph.initialise_graph()

    def get_data(self, *args):
        return self._object_controller.get_data(*args)

    def update(self):
        self._object_graph.update()
        self._object_table.update()
