import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import random
import lib

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

class StopwatchFragment(QWidget):
    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    count = 0
    isRunning = False
    isPaused = False
    textEditVal = ""

    EMPTY_TEXT = "<html>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</html>"

    onSettingsChange = None
    id = None

    def __init__(self, id, count = 0, textEditVal = "", isRunning = False, isPaused = False, onRemoveClick = None, onTimerWriteSettings = None):
        super().__init__()

        self.id = id
        self.count = count

        if isRunning:
            self.isRunning = True
            self.isPaused = True
        else:
            self.isRunning = False
            self.isPaused = False

        self.onSettingsChange = onTimerWriteSettings
        self.textEditVal = textEditVal

        self.setAutoFillBackground(True)

        palette = self.palette()
        r = random_color()
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
                lambda: self.onSettingsChange(self.id, {"label": self.textEdit.toPlainText()})
            )

        self.addTimer()

        self.updateTexts()

    def addTimer(self):
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def onTimer(self):
        if self.isRunning and not(self.isPaused):
            self.changeTimeAndUpdate(self.count + 1)
            # self.count += 1
 
        # self.updateTexts()

    def changeTimeAndUpdate(self, newVal):
        if newVal < 0:
            return

        # self.settings.count = self.count = newVal
        self.count = newVal

        # lib.writeSettingsFile(self.settings)

        self.updateTexts()

        if self.onSettingsChange is not None:
            self.onSettingsChange(self.id, {"count": self.count})

    def updateTexts(self):
        if self.isRunning:
            text = "<html>"
            text += "&nbsp;&nbsp;"
            text += lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            else:
                text += "&nbsp;&nbsp;&nbsp;"
            text += "&nbsp;&nbsp;"
            text += "</html>"
            self.label.setText(text)
        else:
            self.label.setText(self.EMPTY_TEXT)

    def onClickStartPause(self):
        if self.isRunning == False:
            self.isPaused = False
            self.isRunning = True
            self.buttonStartPause.setText("Pause")
            self.buttonReset.setDisabled(False)
        elif not(self.isPaused):
            self.isPaused = True
            self.buttonStartPause.setText("Start")
        elif self.isPaused:
            self.isPaused = False
            self.buttonStartPause.setText("Pause")

        self.updateTexts()

        if self.onSettingsChange is not None:
            self.onSettingsChange(self.id, {"isPaused": self.isPaused, "isRunning": self.isRunning})

    def onClickReset(self):
        self.isRunning = False
        self.isPaused = False

        self.count = 0

        self.updateTexts()

        self.buttonStartPause.setText("Start")

        self.buttonReset.setDisabled(True)

        if self.onSettingsChange is not None:
            self.onSettingsChange(self.id, {"isPaused": self.isPaused, "isRunning": self.isRunning})
