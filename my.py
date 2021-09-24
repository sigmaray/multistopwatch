import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
import random

def random_color():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())

class My(QWidget):
    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    def __init__(self, onRemove = None):
        super().__init__()
        # super(My, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        # palette.setColor(QPalette.Window, QColor(color))
        r = random_color()
        # r = 'red'
        print(r)
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


        b1 = QPushButton("Start/Pause", self)
        layout.addWidget(b1)
        # b2 = QPushButton("Stop", self)
        # layout.addWidget(b2)
        b2 = QPushButton("Reset", self)
        layout.addWidget(b2)
        b3 = QPushButton("Remove", self)
        layout.addWidget(b3)

        if onRemove is not None:
            b3.pressed.connect(
                lambda: onRemove(self)
            )
