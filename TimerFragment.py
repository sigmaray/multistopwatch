import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import random
import lib
from timerEndedDialog import TimeEndedDialog

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

class TimerFragment(QWidget):
    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    count = 0
    isRunning = False
    isPaused = False

    def __init__(self, onRemove = None):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        r = random_color()
        palette.setColor(QPalette.Window, QColor(r))        
        self.setPalette(palette)


        layout = QHBoxLayout()
        self.setLayout(layout)

        self.labelCountdown = QLabel("--", self)
        self.labelCountdown.setStyleSheet("border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + "; background: #fff;")
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
        timer = QTimer(self)
        timer.timeout.connect(self.onTimer)
        timer.start(100)

    def onTimer(self):
        if self.isRunning and not self.isPaused:
            self.count -= 1

            if self.count == 0:
                self.isRunning = False
                self.updateTexts(True)
                TimeEndedDialog.run()
                self.updateTexts()
                self.buttonStartPause.setDisabled(True)
                self.buttonReset.setDisabled(True)

        if self.isRunning:
            self.updateTexts()

    def updateTexts(self, completed=False):
        if completed:
            self.labelCountdown.setText("Completed !!!! ")
            # self.setTrayText("!")
        elif self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.labelCountdown.setText(text)
        else:
            if self.count == 0:
                text = ""
            else:
                text = lib.genTextFull(self.count)
            text += " --"
            self.labelCountdown.setText(text)

    def onClickSet(self):
        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done:
            self.count = second * 10

            self.updateTexts()

            self.isRunning = False
            self.isPaused = False

            self.buttonStartPause.setDisabled(False)
            self.buttonStartPause.setText("Start")

    def onClickSetStart(self):
        self.isRunning = False

        second, done = QInputDialog.getInt(self, 'Seconds', 'Enter Seconds:')

        if done and second > 0:
            self.count = second * 10

            self.updateTexts()

            self.isRunning = True
            self.isPaused = False

            self.buttonStartPause.setText("Pause")
            self.buttonStartPause.setDisabled(False)
            self.buttonReset.setDisabled(False)

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

    def onClickReset(self):
        self.isRunning = False
        self.isPaused = False

        self.count = 0

        self.updateTexts()

        self.buttonStartPause.setDisabled(True)
