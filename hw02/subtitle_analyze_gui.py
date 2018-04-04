import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QDesktopWidget, QFileDialog, QAction)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QDir, QThread, pyqtSlot, pyqtSignal)
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'subtitle-analyze-gui'
        self.left = 10
        self.top = 10
        self.width = 512
        self.height = 400

        self.targetFolder = QDir.current()
        self.createConnection()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.moveToCenter()

        openTargetFolderAction = QAction(
            QIcon('open_target_folder.png'), 'Open Folder...', self)
        openTargetFolderAction.setShortcut('Ctrl+S')
        openTargetFolderAction.setStatusTip('Open the target folder')
        openTargetFolderAction.triggered.connect(self.openTargetFolder)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openTargetFolderAction)
        fileMenu.addAction(exitAction)
        helpMenu = menuBar.addMenu('&Help')

        self.show()

    def openTargetFolder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open the target folder',
                                                     QDir.currentPath())
        if directory:
            self.targetFolder = QDir.current()

    def moveToCenter(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def createConnection(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("analyze.db")
        # self.database.setUserName("root")
        # self.database.setPassword("123456")

        if not self.database.open():
            return False

        createSql = "create table subtitle (id int primary key, name varchar(256), count int, time int, frequency int)"
        insertSql = "insert into subtitle values (?, ?, ?, ?, ?)"
        orderSql = "select * from subtitle order by ? ?"
        dropSql = "drop table subtitle"

        sqlQuery = QSqlQuery()
        sqlQuery.prepare(createSql)
        sqlQuery.exec_()

        sqlQuery.prepare(insertSql)
        sqlQuery.addBindValue(1)
        sqlQuery.addBindValue('1')
        sqlQuery.addBindValue(1)
        sqlQuery.addBindValue(1)
        sqlQuery.addBindValue(1)
        sqlQuery.exec_()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())