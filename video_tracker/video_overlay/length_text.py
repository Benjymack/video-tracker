# Imports
from PyQt5.QtWidgets import QGraphicsTextItem, QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt


# Constants
# Will accept a integer/decimal and a unit (any unit, including made-up ones are
# allowed, provided that they are only alphabetical characters
LENGTH_REGEXP = r'(\d+(\.\d+)?)\s*([a-zA-Z]*)'  # TODO: Add tests for this


# Classes
class LengthText(QGraphicsTextItem):
    def __init__(self, text, parent):
        super().__init__(text, parent)

        self._regexp = QRegExp(LENGTH_REGEXP)
        self._validator = QRegExpValidator(self._regexp)

    def focus_in(self):
        # Enable text interation
        self.setTextInteractionFlags(Qt.TextEditorInteraction)

        self.setFocus()

    def focus_out(self):
        # Disable text interation
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        cursor = self.textCursor()
        cursor.clearSelection()
        self.setTextCursor(cursor)

        # Validate the text
        text = self.document().toPlainText()

        is_valid = self._validator.validate(text, 0)[0]

        if is_valid != QRegExpValidator.Acceptable:
            # The length is not valid, so notify the user and set the focus
            # back to this widget for them to fix their mistake
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText('The ruler length specified is not valid.\n'
                                'Please enter a number, '
                                'optionally followed by a unit.')
            message_box.setWindowTitle('Ruler Length')
            message_box.exec()

            self.focus_in()
