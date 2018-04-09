import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDesktopWidget, QFileDialog)
from PyQt5.QtCore import (QDir)
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        

        self.folder = QDir.current()

        self.init_ui()

    def init_ui(self):
        self.setupUi(self)
        self.move_to_center()

        self.actionOpen_Folder.triggered.connect(self.open_folder)
        self.actionExit.triggered.connect(self.close)

    def move_to_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
    def open_folder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open the folder',
                                                     QDir.currentPath())
        if directory:
            self.folder = QDir.current()
    

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(a.exec_())
