"""Single timer widget that can be created and added in the main window."""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QInputDialog, QTextEdit
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import QTimer
from munch import Munch
import lib
from timer_ended_dialog import TimeEndedDialog


class TimerFragment(QWidget):
    """Class for a single timer widget."""

    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    def __init__(
        self, uid, chosenInterval=0, count=0, textEditVal="", isRunning=False, color=None,
        onRemoveClick=None, onSettingsChange=None
    ):
        """Create state, create elements, configure them, connect them to handler functions, create timer."""
        super().__init__()

        # Put all inputs inside the scope
        self.widgets = Munch()

        self.state = Munch()
        self.state.textEditVal = ""
        self.state.uid = uid
        self.state.count = count
        self.state.chosenInterval = chosenInterval
        self.state.textEditVal = textEditVal
        self.state.color = color
        self.onSettingsChange = onSettingsChange
        self.onRemoveClick = onRemoveClick

        if isRunning:
            self.state.isRunning = True
            self.state.isPaused = True
        else:
            self.state.isRunning = False
            self.state.isPaused = False

        self.uiComponents()

        self.setBackgroundColor()

        self.addTimer()

        self.widgets.labelCountdown.setText(self.stateToLabelText())

    def uiComponents(self):
        """Add UI components, configure them and connect them to handler functions."""
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widgets.labelCountdown = QLabel(self.stateToLabelText(), self)
        self.widgets.labelCountdown.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + "; background: #fff;")
        self.widgets.labelCountdown.setFont(QFont('Monospace', 15))
        # self.widgets.labelCountdown.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.widgets.labelCountdown)

        self.widgets.buttonSet = QPushButton("Set", self)
        layout.addWidget(self.widgets.buttonSet)
        self.widgets.buttonSet.pressed.connect(self.onClickSet)

        self.widgets.buttonSetAndStart = QPushButton("Set And Start", self)
        layout.addWidget(self.widgets.buttonSetAndStart)
        self.widgets.buttonSetAndStart.pressed.connect(self.onClickSetStart)

        self.widgets.buttonStartPause = QPushButton("Start", self)
        layout.addWidget(self.widgets.buttonStartPause)
        self.widgets.buttonStartPause.pressed.connect(self.onClickStartPause)

        self.widgets.buttonReset = QPushButton("Reset", self)
        layout.addWidget(self.widgets.buttonReset)
        self.widgets.buttonReset.pressed.connect(self.onClickReset)

        self.widgets.buttonRemove = QPushButton("Remove", self)
        layout.addWidget(self.widgets.buttonRemove)

        if self.onRemoveClick is not None:
            self.widgets.buttonRemove.pressed.connect(
                lambda: self.onRemoveClick(self)
            )

        self.widgets.textEdit = QTextEdit()
        layout.addWidget(self.widgets.textEdit)
        self.widgets.textEdit.setText(self.state.textEditVal)
        if self.onSettingsChange is not None:
            self.widgets.textEdit.textChanged.connect(
                lambda: self.onSettingsChange(
                    self.state.uid, {"label": self.widgets.textEdit.toPlainText()})
            )

    def setBackgroundColor(self):
        """Set existing background color or generate a new one."""
        if self.state.color is None:
            self.state.color = lib.randomColorHex()
            if self.onSettingsChange is not None:
                self.onSettingsChange(self.state.uid, {"color": self.state.color})
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(self.state.color))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def stateToLabelText(self, completed=False):
        """Generate label text according to the state."""
        countdown = "--"
        if completed:
            countdown = "Completed!"
        elif self.state.isRunning:
            countdown = lib.countToText(self.state.count)
            if self.state.isPaused:
                countdown += " p"
        else:
            if self.state.count == 0:
                countdown = "--"
            else:
                countdown = lib.countToText(self.state.count)
        countdownLine = "countdown: " + countdown

        chosenInterval = "--"
        if self.state.chosenInterval > 0:
            chosenInterval = lib.countToText(self.state.chosenInterval)
        setLine = "set" + lib.genNNbsp(6) + ": " + chosenInterval

        padNum = 23
        return lib.padWithNbsp(setLine, padNum) + "<br/>" + lib.padWithNbsp(countdownLine, padNum)

    def addTimer(self):
        """Add timer and connect it to handler function."""
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def onTimer(self):
        """When timer is triggered: update state and UI."""
        if self.state.isRunning and not self.state.isPaused and self.state.chosenInterval > 0:
            self.state.count -= 1

            if self.onSettingsChange is not None:
                self.onSettingsChange(self.state.uid, {"count": self.state.count})

            if self.state.count == 0:
                self.state.isRunning = False
                self.widgets.labelCountdown.setText(self.stateToLabelText(True))
                TimeEndedDialog.run()
                self.widgets.labelCountdown.setText(self.stateToLabelText())
                self.widgets.buttonStartPause.setText("Start")

        if self.state.isRunning:
            self.widgets.labelCountdown.setText(self.stateToLabelText())

    def onClickSet(self):
        """When Set button is clicked: update state and UI."""
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done:
            self.state.chosenInterval = self.state.count = second * 10

            if self.onSettingsChange is not None:
                self.onSettingsChange(self.state.uid, {"chosenInterval": self.state.chosenInterval})

            self.widgets.labelCountdown.setText(self.stateToLabelText())

            self.state.isRunning = False
            self.state.isPaused = False

            self.widgets.buttonStartPause.setDisabled(False)
            self.widgets.buttonStartPause.setText("Start")

    def onClickSetStart(self):
        """When Set and Start button is clicked: update state and UI."""
        self.state.isRunning = False

        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done and second > 0:
            self.state.chosenInterval = self.state.count = second * 10

            if self.onSettingsChange is not None:
                self.onSettingsChange(self.state.uid, {"chosenInterval": self.state.chosenInterval})

            self.widgets.labelCountdown.setText(self.stateToLabelText())

            self.state.isRunning = True
            self.state.isPaused = False

            self.widgets.buttonStartPause.setText("Pause")
            self.widgets.buttonStartPause.setDisabled(False)
            self.widgets.buttonReset.setDisabled(False)

    def onClickStartPause(self):
        """When Start/Pause button is clicked: update state, and UI."""
        if not self.state.isRunning:
            if self.state.chosenInterval > 0:
                self.state.count = self.state.chosenInterval
                self.state.isPaused = False
                self.state.isRunning = True
                self.widgets.buttonStartPause.setText("Pause")
                self.widgets.buttonReset.setDisabled(False)
        elif not self.state.isPaused:
            self.state.isPaused = True
            self.widgets.buttonStartPause.setText("Start")
        elif self.state.isPaused:
            self.state.isPaused = False
            self.widgets.buttonStartPause.setText("Pause")

        self.widgets.labelCountdown.setText(self.stateToLabelText())

        if self.onSettingsChange is not None:
            self.onSettingsChange(self.state.uid, {"isRunning": self.state.isRunning, "isPaused": self.state.isPaused})

    def onClickReset(self):
        """When Reset button is clicked: reset state and update UI."""
        self.state.isRunning = False
        self.state.isPaused = False

        self.state.chosenInterval = self.state.count = 0

        self.widgets.labelCountdown.setText(self.stateToLabelText())

        self.widgets.buttonStartPause.setDisabled(True)
