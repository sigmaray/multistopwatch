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

class My(QWidget):
    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    count = 0
    isRunning = False
    isPaused = False

    def __init__(self, onRemove = None):
        super().__init__()
        # super(My, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        # palette.setColor(QPalette.Window, QColor(color))
        r = random_color()
        # r = 'red'
        # print(r)
        palette.setColor(QPalette.Window, QColor(r))        
        self.setPalette(palette)


        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(self)
        self.label.setGeometry(75, 100, 250, 70)
        self.label.setStyleSheet(
            "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        self.label.setText("--")
        self.label.setFont(QFont('Arial', 25))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)


        self.buttonStartPause = QPushButton("Start", self)
        layout.addWidget(self.buttonStartPause)
        self.buttonStartPause.pressed.connect(self.onClickStartPause)

        # b2 = QPushButton("Stop", self)
        # layout.addWidget(b2)
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
        # print("L66")
        # pass
        if self.isRunning and not(self.isPaused):
            self.count += 1
 
        self.updateTexts()

    def updateTexts(self):
        if self.isRunning:
            text = lib.genTextFull(self.count)
            if self.isPaused:
                text += " p"
            self.label.setText(text)
            # if not self.isPaused:
            #     self.setTrayText(lib.genTextShort(self.count))
            # else:
            #     self.setTrayText("p")
        else:
            # self.setTrayText("--")
            self.label.setText("--")

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

        self.buttonStartPause.setText("Start")

        self.buttonReset.setDisabled(True)
