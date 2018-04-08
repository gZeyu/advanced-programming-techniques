import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow)

from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.act
    

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
