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

    settings = []

    def __init__(self):
        super().__init__()

        if lib.instance_already_running():
            print('Another instance is already running. Exiting')
            sys.exit()

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
            i = self.findOrCreareFragmetDictAndReturnIndex(w.id)
            # print("i " + str(i))
            del self.settings[i]
            self.textEditState.setText(str(self.settings))
            lib.writeSettingsFile(self.settings)

            self.layout.removeWidget(w)
            w.deleteLater()
            w = None

    def findOrCreareFragmetDictAndReturnIndex(self, id):
        fragmentSettingsArray = [i for i,x in enumerate(self.settings) if x["id"] == id]
        if len(fragmentSettingsArray) != 0:
            fragmentDictIndex = fragmentSettingsArray[0]
        else:
            fragmentDict = {"id": id}
            self.settings.append(fragmentDict)
            fragmentDictIndex = len(self.settings) - 1

        return fragmentDictIndex


    def onSettingsChange(self, id, newSettings):
        # fragmentSettingsArray = filter(lambda x: x["id"] == id, self.settings)

        fragmentDictIndex = self.findOrCreareFragmetDictAndReturnIndex(id)

        # print("onTimerWriteSettings")
        # print({"id": id, "self.settings": self.settings})
        # print("fragmentDictIndex " + str(fragmentDictIndex))
        self.settings[fragmentDictIndex].update(newSettings)
        lib.writeSettingsFile(self.settings)
        
        self.textEditState.setText(str(self.settings))

    def addFragment(self, id, count = 0, label = "", isRunning = False, isPaused = False):
        self.layout.addWidget(StopwatchFragment(id, count, label, isRunning, isPaused, self.onRemoveClick, self.onSettingsChange))

    def uiComponents(self):
        self.layout = QVBoxLayout()

        self.textEditState = QTextEdit()
        self.layout.addWidget(self.textEditState)

        self.settings = lib.readWriteSettings()
        self.textEditState.setText(str(self.settings))

        b = QPushButton("Add Stopwatch", self)
        self.layout.addWidget(b)
        b.pressed.connect(
            lambda: self.addFragment(str(uuid.uuid4()))
        )

        # for i in range(5):
        if len(self.settings) > 0:
            for i in range(len(self.settings)):
                self.addFragment(self.settings[i]["id"], self.settings[i].get("count", 0), self.settings[i].get("label", ""), self.settings[i].get("isRunning", False), self.settings[i].get("isPaused", False))
        else:
            self.addFragment(str(uuid.uuid4()))

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
