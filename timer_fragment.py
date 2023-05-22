"""Single timer widget that can be created and added in the main window."""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
from munch import Munch
import lib
from timer_ended_dialog import TimeEndedDialog


class TimerFragment(QWidget):
    """Class for a single timer widget."""

    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    def __init__(self, onRemove=None):
        """Create state, create elements, configure them, connect them to handler functions, create timer."""
        super().__init__()

        self.state = Munch()
        self.state.count = 0
        self.state.isRunning = False
        self.state.isPaused = False

        self.setAutoFillBackground(True)

        palette = self.palette()
        r = lib.randomColorHex()
        palette.setColor(QPalette.Window, QColor(r))
        self.setPalette(palette)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.labelCountdown = QLabel("--", self)
        self.labelCountdown.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + "; background: #fff;")
        self.labelCountdown.setFont(QFont('Times', 15))
        self.labelCountdown.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.labelCountdown)

        self.buttonSet = QPushButton("Set", self)
        layout.addWidget(self.buttonSet)
        self.buttonSet.pressed.connect(self.onClickSet)

        self.buttonSetAndStart = QPushButton("Set And Start", self)
        layout.addWidget(self.buttonSetAndStart)
        self.buttonSetAndStart.pressed.connect(self.onClickSetStart)

        self.buttonStartPause = QPushButton("Start", self)
        layout.addWidget(self.buttonStartPause)
        self.buttonStartPause.pressed.connect(self.onClickStartPause)

        self.buttonReset = QPushButton("Reset", self)
        layout.addWidget(self.buttonReset)
        self.buttonReset.pressed.connect(self.onClickReset)

        self.buttonRemove = QPushButton("Remove", self)
        layout.addWidget(self.buttonRemove)

        if onRemove is not None:
            self.buttonRemove.pressed.connect(
                lambda: onRemove(self)
            )

        self.addTimer()

    def addTimer(self):
        """Add timer and connect it to handler function."""
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def onTimer(self):
        """When timer is triggered: update state and UI."""
        if self.state.isRunning and not self.state.isPaused:
            self.state.count -= 1

            if self.state.count == 0:
                self.state.isRunning = False
                self.updateLabel(True)
                TimeEndedDialog.run()
                self.updateLabel()
                self.buttonStartPause.setDisabled(True)
                self.buttonReset.setDisabled(True)

        if self.state.isRunning:
            self.updateLabel()

    def updateLabel(self, completed=False):
        """Update label text according to the state."""
        if completed:
            self.labelCountdown.setText("Completed !!!! ")
        elif self.state.isRunning:
            text = lib.countToText(self.state.count)
            if self.state.isPaused:
                text += " p"
            self.labelCountdown.setText(text)
        else:
            if self.state.count == 0:
                text = ""
            else:
                text = lib.countToText(self.state.count)
            text += " --"
            self.labelCountdown.setText(text)

    def onClickSet(self):
        """When Set button is clicked: update state and UI."""
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done:
            self.state.count = second * 10

            self.updateLabel()

            self.state.isRunning = False
            self.state.isPaused = False

            self.buttonStartPause.setDisabled(False)
            self.buttonStartPause.setText("Start")

    def onClickSetStart(self):
        """When Set and Start button is clicked: update state and UI."""
        self.state.isRunning = False

        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done and second > 0:
            self.state.count = second * 10

            self.updateLabel()

            self.state.isRunning = True
            self.state.isPaused = False

            self.buttonStartPause.setText("Pause")
            self.buttonStartPause.setDisabled(False)
            self.buttonReset.setDisabled(False)

    def onClickStartPause(self):
        """When Start/Pause button is clicked: update state, and UI."""
        if not self.state.isRunning:
            self.state.isPaused = False
            self.state.isRunning = True
            self.buttonStartPause.setText("Pause")
            self.buttonReset.setDisabled(False)
        elif not self.state.isPaused:
            self.state.isPaused = True
            self.buttonStartPause.setText("Start")
        elif self.state.isPaused:
            self.state.isPaused = False
            self.buttonStartPause.setText("Pause")

        self.updateLabel()

    def onClickReset(self):
        """When Reset button is clicked: reset state and update UI."""
        self.state.isRunning = False
        self.state.isPaused = False

        self.state.count = 0

        self.updateLabel()

        self.buttonStartPause.setDisabled(True)
