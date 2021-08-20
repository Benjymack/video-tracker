############
#
# Video Tracker
# Author: Benjy Smith
# Allows users to track videos
#
############

from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


app = QApplication([])
main = MainWindow()
main.show()

app.exec_()
