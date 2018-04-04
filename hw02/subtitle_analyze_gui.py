"""This program is used to calculate the word frequency of subtitle files"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget,
                             QDesktopWidget, QFileDialog, QAction)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QDir, QThread, pyqtSlot, pyqtSignal)
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)


class App(QMainWindow):
    """ """

    def __init__(self):
        super().__init__()
        self.title = 'subtitle-analyze-gui'
        self.left = 10
        self.top = 10
        self.width = 512
        self.height = 400

        self.target_folder = QDir.current()
        self.create_connection()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.move_to_center()

        open_target_folder_action = QAction(
            QIcon('open_target_folder.png'), 'Open Folder...', self)
        open_target_folder_action.setShortcut('Ctrl+S')
        open_target_folder_action.setStatusTip('Open the target folder')
        open_target_folder_action.triggered.connect(self.open_target_folder)

        exit_action = QAction(QIcon('exit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(open_target_folder_action)
        file_menu.addAction(exit_action)
        help_menu = menu_bar.addMenu('&Help')

        self.show()

    def open_target_folder(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open the target folder',
                                                     QDir.currentPath())
        if directory:
            self.target_folder = QDir.current()

    def move_to_center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def create_connection(self):
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("analyze.db")
        # self.database.setUserName("root")
        # self.database.setPassword("123456")

        if not self.database.open():
            return False

        create_sql = "create table subtitle (id int primary key, name varchar(256), count int, time int, frequency int)"
        insert_sql = "insert into subtitle values (?, ?, ?, ?, ?)"
        order_sql = "select * from subtitle order by ? ?"
        drop_sql = "drop table subtitle"

        sql_query = QSqlQuery()
        sql_query.prepare(create_sql)
        sql_query.exec_()

        sql_query.prepare(insert_sql)
        sql_query.addBindValue(1)
        sql_query.addBindValue('1')
        sql_query.addBindValue(1)
        sql_query.addBindValue(1)
        sql_query.addBindValue(1)
        sql_query.exec_()
        return True


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    a = list()
    a.append(9)
    sys.exit(app.exec_())
