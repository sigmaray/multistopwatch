import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants

from TimerFragment import TimerFragment

class Window(QMainWindow):
    ASK_ARE_YOU_SURE = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PythonMultiTimer")

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

    def uiComponents(self):
        self.layout = QVBoxLayout()

        b = QPushButton("Add Timer", self)
        self.layout.addWidget(b)
        b.pressed.connect(
            lambda: self.layout.addWidget(TimerFragment(self.onRemoveClick))
        )

        for i in range(5):
            self.layout.addWidget(TimerFragment(self.onRemoveClick))        

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
