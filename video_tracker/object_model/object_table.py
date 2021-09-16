# Imports
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView


# Constants
NUM_COLUMNS = 2


# Classes
class ObjectTable(QTableWidget):
    def __init__(self):
        super().__init__()

        self.setColumnCount(NUM_COLUMNS)
