# Imports
from PyQt5.QtWidgets import QDialog, QGridLayout, QCheckBox, QFrame, QLabel, \
    QWidget, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt


# Constants
ITEMS_BEFORE_TABLE = 3
AVAILABLE_EXPORT_FORMATS = (
    ('Comma separated values', 'csv'),
)
EXPORT_FORMATS_DICT = {x[0]+' (*.'+x[1]+')': x[1] for x in
                       AVAILABLE_EXPORT_FORMATS}
FORMATTED_EXPORT_FORMATS = ';;'.join(EXPORT_FORMATS_DICT.keys())


# Classes
# QHLine and QVLine from https://stackoverflow.com/a/41068447
class HLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class ExportTable(QWidget):
    def __init__(self, object_controller):
        super().__init__()

        self._object_controller = object_controller

        self._layout = QGridLayout()

        # Columns are the objects, rows are the measurements
        self._possible_measurements = self._object_controller. \
            get_all_possible_measurements()
        self._object_measurements = self._object_controller. \
            get_measurements_per_object()
        self._objects = list(self._object_measurements.keys())

        # Prepare storage of the checkboxes
        self._checkboxes = {}
        self._all_object_checkboxes = {}
        self._all_measurement_checkboxes = {}

        # Add the dividing lines between the headers and the main checkboxes
        self._layout.addWidget(HLine(), ITEMS_BEFORE_TABLE - 1,
                               ITEMS_BEFORE_TABLE, 1, len(self._objects))
        self._layout.addWidget(VLine(), ITEMS_BEFORE_TABLE,
                               ITEMS_BEFORE_TABLE - 1,
                               len(self._possible_measurements),
                               1)

        self._create_selection_checkboxes()
        self._create_measurement_headers()
        self._create_object_headers()

        self.setLayout(self._layout)

        self._updating_checkboxes = False

    def _create_selection_checkboxes(self):
        for row, measurement in enumerate(self._possible_measurements):
            for col, o in enumerate(self._objects):
                if measurement in self._object_measurements[o]:
                    checkbox = QCheckBox()
                    if o not in self._checkboxes:
                        self._checkboxes[o] = {}
                    self._checkboxes[o][measurement] = checkbox

                    checkbox.setChecked(True)
                    checkbox.stateChanged.connect(
                        lambda state, o=o, m=measurement:
                        self._measurement_checkbox_changed(o, m, state))

                    self._layout.addWidget(checkbox, row + ITEMS_BEFORE_TABLE,
                                           col + ITEMS_BEFORE_TABLE,
                                           Qt.AlignCenter)

    def _create_measurement_headers(self):
        for row, measurement in enumerate(self._possible_measurements):
            checkbox = QCheckBox()
            checkbox.setLayoutDirection(Qt.RightToLeft)
            self._all_measurement_checkboxes[measurement] = checkbox
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                lambda state, m=measurement:
                self._all_checkbox_changed(m, False, state))

            self._layout.addWidget(checkbox, row + ITEMS_BEFORE_TABLE,
                                   1, Qt.AlignCenter)
            self._layout.addWidget(QLabel(measurement),
                                   row + ITEMS_BEFORE_TABLE,
                                   0, Qt.AlignCenter)

    def _create_object_headers(self):
        for col, o in enumerate(self._objects):
            checkbox = QCheckBox()
            self._all_object_checkboxes[o] = checkbox
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(
                lambda state, o=o:
                self._all_checkbox_changed(o, True, state))

            self._layout.addWidget(checkbox, 1, col + ITEMS_BEFORE_TABLE,
                                   Qt.AlignCenter)
            self._layout.addWidget(QLabel(o), 0, col + ITEMS_BEFORE_TABLE,
                                   Qt.AlignCenter)

    def _get_boxes(self, thing, is_object):
        if is_object:
            boxes = list(self._checkboxes[thing].values())
        else:
            boxes = [x[thing] for x in self._checkboxes.values()]
        return boxes

    def _update_all_checkbox(self, thing, is_object):
        self._updating_checkboxes = True
        if is_object:
            all_checkbox = self._all_object_checkboxes[thing]
        else:
            all_checkbox = self._all_measurement_checkboxes[thing]

        boxes = self._get_boxes(thing, is_object)

        all_on = True
        all_off = True

        for checkbox in boxes:
            if checkbox.isChecked():
                all_off = False
            else:
                all_on = False

        if all_on:
            all_checkbox.setCheckState(Qt.Checked)
        elif all_off:
            all_checkbox.setCheckState(Qt.Unchecked)
        else:  # There is a mix: indeterminate
            all_checkbox.setCheckState(Qt.PartiallyChecked)

        self._updating_checkboxes = False

    def _measurement_checkbox_changed(self, o, measurement, state):
        self._update_all_checkbox(o, True)
        self._update_all_checkbox(measurement, False)

    def _all_checkbox_changed(self, thing, is_object, state):
        if self._updating_checkboxes:
            return

        for checkbox in self._get_boxes(thing, is_object):
            checkbox.setChecked(state)

    def get_selected_checkboxes(self):
        selected = []
        for measurement, checkboxes in self._checkboxes.items():
            for o, checkbox in checkboxes.items():
                if checkbox.isChecked():
                    selected.append((measurement, o))

        return selected


class ExportDialog(QDialog):
    def __init__(self, parent, object_controller):
        super().__init__(parent)

        self.setWindowTitle('Export Data')

        self._object_controller = object_controller

        self._layout = QVBoxLayout()

        self._export_table = ExportTable(self._object_controller)
        self._layout.addWidget(self._export_table)

        self._export_button = QPushButton('Export to file')
        self._export_button.clicked.connect(self._export_to_file)
        self._layout.addWidget(self._export_button)

        self.setLayout(self._layout)

    def _export_to_file(self):
        data_to_export = self._export_table.get_selected_checkboxes()

        file_name, long_format = QFileDialog.getSaveFileName(
            caption='Export Data', filter=FORMATTED_EXPORT_FORMATS)

        format_ = EXPORT_FORMATS_DICT[long_format]

        self._object_controller.export_to_file(data_to_export, file_name,
                                               format_)

        self.accept()
