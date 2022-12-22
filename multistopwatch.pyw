import sys
import uuid
import lib
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants
from munch import munchify

from StopwatchFragment import StopwatchFragment

class Window(QMainWindow):
    ASK_ARE_YOU_SURE = False

    settings = {}

    def __init__(self):
        super().__init__()

        if lib.instance_already_running():
            print('Another instance is already running. Exiting')
            sys.exit()

        self.settings = munchify(lib.readWriteSettings())

        self.setWindowTitle("PythonMultiStopwatch")

        # self.setGeometry(100, 100, 400, 500)
        # self.setGeometry(100, 100, 700, 500)
        self.setGeometry(100, 100, 700, 600)

        self.uiComponents()

        self.moveWindowToCenter()

        # self.setFixedSize(self.size())

        self.show()

    def moveWindowToCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def onRemoveClick(self, w):
        to_close = True
        if self.ASK_ARE_YOU_SURE:
            reply = QMessageBox.question(
                self,
                "Are you sure?",
                "Are you sure?",
                QMessageBox.Yes,
                QMessageBox.No,
            )
            to_close = (reply == QMessageBox.Yes)

        if to_close:
            self.layout.removeWidget(w)
            w.deleteLater()
            w = None
    def onTimerWriteSettings(self, id, count):
        print("onTimerWriteSettings")

    def addFragment(self):
        self.layout.addWidget(StopwatchFragment(uuid.uuid4(), self.onRemoveClick, self.onTimerWriteSettings))

    def uiComponents(self):
        self.layout = QVBoxLayout()

        b = QPushButton("Add Stopwatch", self)
        self.layout.addWidget(b)
        b.pressed.connect(
            lambda: self.addFragment()
        )

        # for i in range(5):
        for i in range(1):
            self.addFragment()

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
