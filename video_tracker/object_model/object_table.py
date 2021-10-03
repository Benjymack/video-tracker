# Imports
from PyQt5.QtWidgets import QMenu, QHeaderView, QAction
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
        self._columns = ['t', 'x', 'y']

        self.horizontalHeader().setSectionsMovable(True)
        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            self._header_section_clicked)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

        self.update()

    def update(self):
        """
        Update the column names, and retabulate the data.
        """
        self.setColumnCount(len(self._columns))

        self._tabulate_data()

        available_measurements = self._object_display. \
            get_current_object_available_measurements()

        if available_measurements == {}:
            return

        display_cols = [x + ' (' + available_measurements[x] + ')'
                        if x != '' else '' for x in self._columns]

        self.setHorizontalHeaderLabels(display_cols)

    def _tabulate_data(self):
        """
        Get data from the object display, and put it into the table.
        """
        data = self._object_display.get_data(*self._columns)

        if data is None:
            final_data = None
        else:
            final_data = {}

            for time, data_line in data.items():
                final_data[time] = [
                    data_line[col] if data_line[col] is not None
                    else '' for col in self._columns]

        self.setData(final_data)

    def _header_section_clicked(self, pos):
        """
        Show the context menu for when a header is clicked,
        and perform the action that the user chooses.
        """
        menu = QMenu()

        index = self.horizontalHeader().logicalIndexAt(pos)

        if index < 0:  # The user didn't actually click on a column
            return  # TODO: Add menu to add a particular type of column

        if index != 0:  # Can't delete the time column
            menu.addAction(REMOVE_ACTION)

        action_to_measurement_type = {}

        insert_menu = QMenu(INSERT_RIGHT_ACTION)
        for measurement, unit in self._object_display. \
                get_current_object_available_measurements().items():
            text = measurement + ' (' + unit + ')'
            action = QAction(text)
            action_to_measurement_type[action] = (measurement, 'new')
            insert_menu.addAction(action)

        menu.addMenu(insert_menu)

        # Choose a new column type
        if index != 0:
            type_menu = QMenu(CHANGE_ACTION)

            for measurement, unit in self._object_display. \
                    get_current_object_available_measurements().items():
                text = measurement + ' (' + unit + ')'
                action = QAction(text)
                action_to_measurement_type[action] = (measurement, 'same')
                type_menu.addAction(action)

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
        elif action in action_to_measurement_type:
            if action_to_measurement_type[action][1] == 'new':
                self._columns.insert(index + 1,
                                     action_to_measurement_type[action][0])
            else:  # Same
                self._columns[index] = action_to_measurement_type[action][0]

        self.update()
