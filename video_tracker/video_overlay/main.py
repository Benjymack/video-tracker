# Imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from overlay_canvas import OverlayCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 500, 500)

        self._main_widget = QLabel('This is the background')
        self._main_widget.resizeEvent = self.resize_event
        self._main_widget.setStyleSheet('background-color: rgb(255, 0, 0)')

        self._overlay_canvas = OverlayCanvas(self._main_widget)

        self.setCentralWidget(self._main_widget)

    def resize_event(self, event):
        self._overlay_canvas.resizeEvent(event)


if __name__ == '__main__':
    app = QApplication([])
    main = MainWindow()
    main.show()

    app.exec_()
