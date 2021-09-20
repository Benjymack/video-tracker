# Imports
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint
from pyqtgraph import TableWidget


# Constants
REMOVE_ACTION = 'Remove'
INSERT_RIGHT_ACTION = 'Insert new column to right'


# Classes
class ObjectTable(TableWidget):
    def __init__(self, object_display):
        super().__init__(sortable=False)

        self._object_display = object_display

        # Start with just time
        self._columns = ['t']

        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().sectionClicked.connect(
            self._header_section_clicked)

        self.update()

    def update(self):
        self.setColumnCount(len(self._columns))
        self.setHorizontalHeaderLabels(self._columns)  # TODO: Get nice names

        self._tabulate_data()

    def _tabulate_data(self):
        data = self._object_display.get_data(*self._columns)

        self.setData(data)

    def _header_section_clicked(self, index):
        menu = QMenu()

        if index != 0:  # Can't delete the time column
            menu.addAction(REMOVE_ACTION)
        menu.addAction(INSERT_RIGHT_ACTION)

        # TODO: Account for when there is a scrollbar
        x = self.horizontalHeader().sectionPosition(index)
        y = self.horizontalHeader().height()

        action = menu.exec_(self.mapToGlobal(QPoint(x, y)))

        if action is None:
            return

        action_text = action.text()

        if action_text == REMOVE_ACTION:
            del self._columns[index]
        elif action_text == INSERT_RIGHT_ACTION:
            self._columns.insert(index+1, '')

        self.update()
