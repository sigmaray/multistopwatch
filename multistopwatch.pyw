import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColorConstants

# import lib
from color import Color 
from StopwatchFragment import StopwatchFragment


class Window(QMainWindow):
    ASK_ARE_YOU_SURE = False

    COLOR1 = "#fff"
    COLOR2 = "#6495ED"

    count = 0
    isRunning = False
    isPaused = False

    def __init__(self):
        super().__init__()

        self.setWindowTitle("PythonMultiStopwatch")

        # self.setGeometry(100, 100, 400, 500)
        # self.setGeometry(100, 100, 700, 500)
        self.setGeometry(100, 100, 700, 600)

        self.uiComponents()

        self.moveWindowToCenter()

        # self.setFixedSize(self.size())

        # self.addTimer()

        self.show()

    # def setTrayText(self, str="--"):
    #     self.tray.setIcon(lib.drawIcon(str, self.COLOR1, self.COLOR2))

    # def addTrayIcon(self):
    #     self.tray = QSystemTrayIcon()

    #     actionShow = QAction("Show", self)
    #     actionQuit = QAction("Exit", self)
    #     actionHide = QAction("Hide", self)
    #     actionShow.triggered.connect(self.show)
    #     actionHide.triggered.connect(self.hide)
    #     actionQuit.triggered.connect(qApp.quit)
    #     menu = QMenu()
    #     menu.addAction(actionShow)
    #     menu.addAction(actionHide)
    #     menu.addAction(actionQuit)
    #     self.tray.setContextMenu(menu)

    #     self.setTrayText("--")

    #     self.tray.activated.connect(self.onTrayIconActivated)

    #     self.tray.setVisible(True)

    # def onTrayIconActivated(self, reason):
    #     # if reason == QSystemTrayIcon.DoubleClick:
    #     if reason == QSystemTrayIcon.Trigger:
    #         self.show()
    #         # if self.windowState() == QtCore.Qt.WindowMinimized:
    #         self.setWindowState(QtCore.Qt.WindowActive)
    #         self.activateWindow()

    def moveWindowToCenter(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    # def uiComponents(self):
    #     self.addTrayIcon()

    #     self.label = QLabel(self)
    #     self.label.setGeometry(75, 100, 250, 70)
    #     self.label.setStyleSheet(
    #         "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
    #     self.label.setText("--")
    #     self.label.setFont(QFont('Arial', 25))
    #     self.label.setAlignment(Qt.AlignCenter)

    #     self.buttonStartPause = QPushButton("Start", self)
    #     self.buttonStartPause.setGeometry(125, 250, 150, 40)
    #     self.buttonStartPause.pressed.connect(self.onClickStartPause)

    #     self.buttonReset = QPushButton("Reset", self)
    #     self.buttonReset.setGeometry(125, 325, 150, 40)
    #     self.buttonReset.pressed.connect(self.onClickReset)
    #     self.buttonReset.setDisabled(True)

    #     buttonMinimize = QPushButton("Minimize to tray", self)
    #     buttonMinimize.setGeometry(125, 425, 150, 40)
    #     buttonMinimize.pressed.connect(self.hide)


    def onRemoveClick(self, w):
        # print("L102 " + str(i))
        # pass

        # qm = QtGui.QMessageBox

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
        # self.label = QLabel(self)
        # self.label.setGeometry(75, 100, 250, 70)
        # self.label.setStyleSheet(
        #     "border : 4px solid " + self.COLOR2 + "; color: " + self.COLOR2 + ";")
        # self.label.setText("--")
        # self.label.setFont(QFont('Arial', 25))
        # self.label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        # layout.addWidget(Color('red'))
        # layout.addWidget(Color('green'))
        # layout.addWidget(Color('blue'))

        b = QPushButton("Add Stopwatch", self)
        self.layout.addWidget(b)
        b.pressed.connect(
            lambda: self.layout.addWidget(StopwatchFragment(self.onRemoveClick))
        )

        for i in range(5):
            self.layout.addWidget(StopwatchFragment(self.onRemoveClick))        

        # widget = QWidget()
        # widget.setLayout(self.layout)
        # self.setCentralWidget(widget)

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)





    # def addTimer(self):
    #     timer = QTimer(self)
    #     timer.timeout.connect(self.onTimer)
    #     timer.start(100)

    # def updateTexts(self):
    #     if self.isRunning:
    #         text = lib.genTextFull(self.count)
    #         if self.isPaused:
    #             text += " p"
    #         self.label.setText(text)
    #         if not self.isPaused:
    #             self.setTrayText(lib.genTextShort(self.count))
    #         else:
    #             self.setTrayText("p")
    #     else:
    #         self.setTrayText("--")
    #         self.label.setText("--")

    # def onTimer(self):
    #     if self.isRunning and not(self.isPaused):
    #         self.count += 1
 
    #     self.updateTexts()

    # def onClickStartPause(self):
    #     if self.isRunning == False:
    #         self.isPaused = False
    #         self.isRunning = True
    #         self.buttonStartPause.setText("Pause")
    #         self.buttonReset.setDisabled(False)
    #     elif not(self.isPaused):
    #         self.isPaused = True
    #         self.buttonStartPause.setText("Start")
    #     elif self.isPaused:
    #         self.isPaused = False
    #         self.buttonStartPause.setText("Pause")

    #     self.updateTexts()

    # def onClickReset(self):
    #     self.isRunning = False
    #     self.isPaused = False

    #     self.count = 0

    #     self.updateTexts()

    #     self.buttonStartPause.setText("Start")

    #     self.buttonReset.setDisabled(True)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())