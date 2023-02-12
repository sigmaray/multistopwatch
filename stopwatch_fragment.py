"""Single stopwatch widget that can be created and added in the main window."""
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
from munch import Munch
import lib


class StopwatchFragment(QWidget):
    """Class for a single stopwatch widget."""

    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    EMPTY_TEXT = "<html>" + \
                 "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
                 "--" + \
                 "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + \
                 "</html>"

    def __init__(
        self, uid, count=0, textEditVal="", isRunning=False,
        onRemoveClick=None, onTimerWriteSettings=None
    ):
        """Create state, create elements, configure them, connect them to handler functions, create timer."""
        super().__init__()

        self.state = Munch()
        self.state.textEditVal = ""
        self.state.uid = uid
        self.state.count = count

        if isRunning:
            self.state.isRunning = True
            self.state.isPaused = True
        else:
            self.state.isRunning = False
            self.state.isPaused = False

        self.onSettingsChange = onTimerWriteSettings
        self.state.textEditVal = textEditVal

        self.setAutoFillBackground(True)

        palette = self.palette()
        r = lib.randomColorHex()
        palette.setColor(QPalette.Window, QColor(r))
        self.setPalette(palette)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(self)
        self.label.setGeometry(75, 100, 250, 70)
        self.label.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + "; background: #fff;")
        # self.label.setText(self.EMPTY_TEXT)
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.buttonStartPause = QPushButton("Start", self)
        layout.addWidget(self.buttonStartPause)
        self.buttonStartPause.pressed.connect(self.onClickStartPause)

        self.buttonReset = QPushButton("Reset", self)
        layout.addWidget(self.buttonReset)
        self.buttonReset.pressed.connect(self.onClickReset)

        self.buttonRemove = QPushButton("Remove", self)
        layout.addWidget(self.buttonRemove)

        if onRemoveClick is not None:
            self.buttonRemove.pressed.connect(
                lambda: onRemoveClick(self)
            )

        self.textEdit = QTextEdit()
        layout.addWidget(self.textEdit)
        self.textEdit.setText(textEditVal)
        if self.onSettingsChange is not None:
            self.textEdit.textChanged.connect(
                lambda: self.onSettingsChange(
                    self.state.uid, {"label": self.textEdit.toPlainText()})
            )

        self.addTimer()

        self.updateLabel()

    def addTimer(self):
        """Add timer and connect it to handler function."""
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def onTimer(self):
        """When timer is triggered."""
        if self.state.isRunning and not self.state.isPaused:
            self.changeTimeAndUpdate(self.state.count + 1)
            # self.state.count += 1

        # self.updateTexts()

    def changeTimeAndUpdate(self, newVal):
        """Update state, UI and settings file."""
        if newVal < 0:
            return

        # self.settings.count = self.state.count = newVal
        self.state.count = newVal

        # lib.writeSettingsFile(self.settings)

        self.updateLabel()

        if self.onSettingsChange is not None:
            self.onSettingsChange(self.state.uid, {"count": self.state.count})

    def updateLabel(self):
        """Update label text according to the state."""
        if self.state.isRunning:
            text = "<html>"
            text += "&nbsp;&nbsp;"
            text += lib.countToText(self.state.count)
            if self.state.isPaused:
                text += " p"
            else:
                text += "&nbsp;&nbsp;&nbsp;"
            text += "&nbsp;&nbsp;"
            text += "</html>"
            self.label.setText(text)
        else:
            self.label.setText(self.EMPTY_TEXT)

    def onClickStartPause(self):
        """When Start/Pause button is clicked: update state, UI and settings file."""
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

        if self.onSettingsChange is not None:
            self.onSettingsChange(
                self.state.uid, {"isPaused": self.state.isPaused, "isRunning": self.state.isRunning})

    def onClickReset(self):
        """When Reset button is clicked: reset state, update UI and settings file."""
        self.state.isRunning = False
        self.state.isPaused = False

        self.state.count = 0

        self.updateLabel()

        self.buttonStartPause.setText("Start")

        self.buttonReset.setDisabled(True)

        if self.onSettingsChange is not None:
            self.onSettingsChange(
                self.state.uid, {"isPaused": self.state.isPaused, "isRunning": self.state.isRunning})
