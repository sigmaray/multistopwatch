"""Multiple timers implemented in PyQT."""
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QPushButton, QScrollArea, QWidget, QDesktopWidget,
    QMessageBox, qApp
)
from PyQt5.QtCore import Qt
import lib
from timer_fragment import TimerFragment


class MultiTimer(QMainWindow):
    """Main window of PyQt the application."""

    SETTINGS_FILE = "multistopwatch.json"

    ASK_ARE_YOU_SURE_ON_DELETE = False
    ASK_ARE_YOU_SURE_ON_CLOSE = True

    def __init__(self):
        """Check if app is already running, create elements, show window."""
        super().__init__()

        if lib.isAlreadyRunning('multitimer'):
            print('Another instance is already running. Exiting')
            sys.exit()

        self.setWindowTitle("PythonMultiTimer")

        self.setGeometry(100, 100, 700, 600)

        self.uiComponents()

        self.moveWindowToCenter()

        # self.setFixedSize(self.size())

        self.show()

    def moveWindowToCenter(self):
        """
        Center PyQt window.

        https://pythonprogramminglanguage.com/pyqt5-center-window/
        """
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def onRemoveClick(self, w):
        """
        When remove timer button is clicked.

        * Ask user's confirmation
        * Delete timer widget
        """
        shouldClose = True
        if self.ASK_ARE_YOU_SURE_ON_DELETE:
            reply = QMessageBox.question(
                self,
                "Are you sure?",
                "Are you sure?",
                QMessageBox.Yes,
                QMessageBox.No,
            )
            shouldClose = reply == QMessageBox.Yes

        if shouldClose:
            self.layout.removeWidget(w)
            w.deleteLater()
            w = None

    def uiComponents(self):
        """Add UI components, configure them and connect them to handler functions."""
        self.layout = QVBoxLayout()

        b = QPushButton("Add Timer", self)
        self.layout.addWidget(b)
        b.pressed.connect(
            lambda: self.layout.addWidget(TimerFragment(self.onRemoveClick))
        )

        for _ in range(5):
            self.layout.addWidget(TimerFragment(self.onRemoveClick))

        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)

    def closeEvent(self, event):
        """
        Ask user's confirmation before exiting.

        (overriding PyQt close event)

        https://learndataanalysis.org/example-of-how-to-use-the-qwidget-close-event-pyqt5-tutorial/
        """
        if self.ASK_ARE_YOU_SURE_ON_CLOSE:
            event.ignore()
            self.areYouSureAndClose()

    def areYouSureAndClose(self):
        """Ask user's confirmation and exit."""
        quitMsg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message',
                                     quitMsg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            qApp.quit()


App = QApplication(sys.argv)
window = MultiTimer()
sys.exit(App.exec())
