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
        self, uid, count=0, textEditVal="", isRunning=False, color=None,
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
        self.state.color = color

        if isRunning:
            self.state.isRunning = True
            self.state.isPaused = True
        else:
            self.state.isRunning = False
            self.state.isPaused = False

        self.state.textEditVal = textEditVal

        self.onSettingsChange = onSettingsChange
        self.onRemoveClick = onRemoveClick

        self.uiComponents()

        self.setBackgroundColor()

        self.addTimer()

        self.updateLabel()

    def uiComponents(self):
        """Add UI components, configure them and connect them to handler functions."""
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.widgets.label = QLabel(self)
        self.widgets.label.setGeometry(75, 100, 250, 70)
        self.widgets.label.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + "; background: #fff;")
        # self.widgets.label.setText(self.EMPTY_TEXT)
        self.widgets.label.setFont(QFont('Arial', 25))
        self.widgets.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.widgets.label)

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
            self.widgets.label.setText(text)
        else:
            self.widgets.label.setText(self.EMPTY_TEXT)

    def onClickStartPause(self):
        """When Start/Pause button is clicked: update state, UI and settings file."""
        if not self.state.isRunning:
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

        self.widgets.buttonStartPause.setText("Start")

        self.widgets.buttonReset.setDisabled(True)

        if self.onSettingsChange is not None:
            self.onSettingsChange(
                self.state.uid, {"isPaused": self.state.isPaused, "isRunning": self.state.isRunning})
