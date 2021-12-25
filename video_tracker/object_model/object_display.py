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
        """
        Returns the current object from the object controller.
        """
        return self._object_controller.get_current_object()

    def get_current_object_available_measurements(self):
        """
        Returns a list of the current measurements and their units from the
        current object.
        """
        current_object = self.get_current_object()
        if current_object is None:
            return {}
        return current_object.get_available_measurements()

    def initialise_display(self):
        """
        Initialises the graph and table.
        """
        self._object_graph.initialise_graph()

    def get_data(self, *args):
        """
        Returns the data from the object controller.
        """
        return self._object_controller.get_data(*args)

    def update(self):
        """
        Updates the graph and table.
        """
        self._object_graph.update()
        self._object_table.update()

    def load(self, data):
        self._object_graph.load(data['graph'])
        self._object_table.load(data['table'])

    def dump(self):
        return {
            'graph': self._object_graph.dump(),
            'table': self._object_table.dump(),
        }
