"""Dialog that is shown to user when timer is over."""
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QLabel, QDialogButtonBox
from PyQt5 import QtCore


class TimeEndedDialog(QDialog):
    """PyQt dialog that is shown user when timer is ended."""

    COLORS = ["white", "red"]

    def genStyle(self, color):
        """Generate CSS that changes background color of dialog window."""
        return "background-color: " + color + ";"

    def onTimer(self):
        """When timer is triggered: toggle background color."""
        if self.colorIndex == 0:
            self.colorIndex = 1
        else:
            self.colorIndex = 0
        color = self.COLORS[self.colorIndex]

        self.setStyleSheet(self.genStyle(color))

    def __init__(self):
        """Set default colorIndex, create elements, configure them, connect them to handler functions, create timer."""
        super().__init__()

        self.colorIndex = 0

        # self.setModal(True)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setWindowTitle("Time Ended")

        dlgLayout = QVBoxLayout()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.timer.start(400)

        dlgLayout.addWidget(QLabel("Time ended!"))

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        dlgLayout.addWidget(self.button_box)

        self.setLayout(dlgLayout)

    @staticmethod
    def run():
        """Create and show the dialog."""
        dialog = TimeEndedDialog()
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = TimeEndedDialog()
    dlg.show()
    sys.exit(app.exec_())
