# Imports
from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint, Qt
from pyqtgraph import TableWidget


# Constants
REMOVE_ACTION = 'Remove column'
INSERT_RIGHT_ACTION = 'Insert new column to right'
CHANGE_ACTION = 'Change type'


# Classes
class ObjectTable(TableWidget):
    def __init__(self, object_display):
        super().__init__(sortable=False)

        self._object_display = object_display

        # Start with just time
        self._columns = ['t']

        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(self._header_section_clicked)
        self.verticalHeader().hide()

        self.update()

    def update(self):
        self.setColumnCount(len(self._columns))

        self._tabulate_data()

        self.setHorizontalHeaderLabels(self._columns)  # TODO: Get nice names

    def _tabulate_data(self):
        data = self._object_display.get_data(*self._columns)

        if data is None:
            final_data = None
        else:
            final_data = {}

            for time, data_line in data.items():
                final_data[time] = [data_line[col] for col in self._columns]

        self.setData(final_data)

    def _header_section_clicked(self, pos):
        menu = QMenu()

        index = self.horizontalHeader().logicalIndexAt(pos)

        if index < 0:  # The user didn't actually click on a column
            return

        if index != 0:  # Can't delete the time column
            menu.addAction(REMOVE_ACTION)
        menu.addAction(INSERT_RIGHT_ACTION)

        # Choose a new column type
        if index != 0:
            type_menu = QMenu(CHANGE_ACTION)

            text_to_measurement = {}
            for measurement, unit in self._object_display. \
                    get_current_object_available_measurements().items():
                text = measurement + ' (' + unit + ')'
                text_to_measurement[text] = measurement
                type_menu.addAction(text)

            menu.addMenu(type_menu)

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
        elif action_text in text_to_measurement:
            self._columns[index] = text_to_measurement[action_text]

        self.update()
