# Imports
try:
    from object_model.object_graph import ObjectGraph
    from object_model.object_table import ObjectTable
except ImportError:
    from object_graph import ObjectGraph
    from object_table import ObjectTable

from PyQt5.QtWidgets import QWidget, QVBoxLayout


# Classes
class ObjectDisplay(QWidget):
    def __init__(self):
        super().__init__()

        self._object_graph = ObjectGraph()
        self._object_table = ObjectTable()

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._object_graph)
        self._layout.addWidget(self._object_table)
        self.setLayout(self._layout)
