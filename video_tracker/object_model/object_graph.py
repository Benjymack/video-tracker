# Imports
from pyqtgraph import PlotWidget
import pyqtgraph

from PyQt5.QtWidgets import QMenu
from PyQt5.QtCore import QPoint


# pyqtgraph configuration
pyqtgraph.setConfigOption('background', 'w')  # White background
pyqtgraph.setConfigOption('foreground', 'k')  # Black foreground


# Classes
class ObjectGraph(PlotWidget):
    def __init__(self, object_display):
        super().__init__()

        self._object_display = object_display

        self._y_measurement = None
        self._x_measurement = None

        for name, axis in self.plotItem.axes.items():
            # Disable the SI prefix, as they will already be included
            axis['item'].enableAutoSIPrefix(False)

            axis['item'].label.mousePressEvent = \
                lambda event, n=name: self._axis_label_clicked(n, event)

        self._plot_data = self.plotItem.plot()

    def _axis_label_clicked(self, name, event):
        # Create the context menu to display the available measurements
        menu = QMenu()
        text_to_measurement = {}

        for measurement, unit in self._object_display. \
                get_current_object_available_measurements().items():
            text = measurement + ' (' + unit + ')'
            text_to_measurement[text] = measurement
            menu.addAction(text)

        point = QPoint(event.scenePos().x(), event.scenePos().y())

        action = menu.exec_(self.mapToGlobal(point))

        if action is not None:
            # Change the axis to be what was selected
            selected = text_to_measurement[action.text()]

            self._set_measurement(name, selected)

    def _replot_data(self):
        if self._y_measurement is None or self._x_measurement is None:
            return

        data = self._object_display.get_data(self._x_measurement,
                                             self._y_measurement)

        x = []
        y = []

        for time, thing in sorted(data.items()):
            if self._x_measurement in thing and \
                    self._y_measurement in thing:
                x.append(thing[self._x_measurement])
                y.append(thing[self._y_measurement])

        self._plot_data.setData(x, y, symbol='o', symbolBrush='k')

    def _set_measurement(self, side, measurement):
        measurements = self._object_display. \
            get_current_object_available_measurements()

        try:
            self.plotItem.setLabel(side, measurement, measurements[measurement])
        except KeyError:
            return  # TODO: Work out what to do here

        if side == 'left':
            self._y_measurement = measurement
        elif side == 'bottom':
            self._x_measurement = measurement

        self._replot_data()

    def initialise_graph(self):
        self._x_measurement = 'x'
        self._y_measurement = 'y'
        self._update_axes()

    def _update_axes(self):
        self._set_measurement('left', self._y_measurement)
        self._set_measurement('bottom', self._x_measurement)

    def update(self):
        self._update_axes()
