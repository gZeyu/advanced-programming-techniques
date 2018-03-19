import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QWidget, QFileSystemModel, QAbstractItemView,
    QTreeView, QFileDialog, QHBoxLayout, QPushButton, QLabel, QAction)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (QDir, QFile, QModelIndex, QItemSelectionModel,
                          QThread, pyqtSlot, pyqtSignal)
import os
import re
import xlsxwriter
from logextractor import (parseFile, saveToExcel)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'logextracter-gui'
        self.left = 10
        self.top = 10
        self.width = 1024
        self.height = 400
        self.initUI()

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        openSrcFolderAction = QAction(
            QIcon('opensrcfolder.png'), 'SRC Folder', self)
        openSrcFolderAction.setShortcut('Ctrl+S')
        openSrcFolderAction.setStatusTip('Open the source folder')
        openSrcFolderAction.triggered.connect(self.browseSrcFolder)

        openDestFolderAction = QAction(
            QIcon('opendestfolder.png'), 'DEST Folder', self)
        openDestFolderAction.setShortcut('Ctrl+D')
        openDestFolderAction.setStatusTip('Open the destination folder')
        openDestFolderAction.triggered.connect(self.browseDestFolder)

        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openSrcFolderAction)
        fileMenu.addAction(openDestFolderAction)
        fileMenu.addAction(exitAction)
        helpMenu = menuBar.addMenu('&Help')

        self.srcModel = QFileSystemModel()
        self.srcModel.setRootPath(QDir.currentPath())
        self.srcTree = QTreeView()
        self.srcTree.setModel(self.srcModel)
        self.srcTree.setRootIndex(self.srcModel.index(QDir.currentPath()))
        self.srcTree.setAnimated(False)
        self.srcTree.setIndentation(20)
        self.srcTree.setSortingEnabled(True)
        self.srcTree.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.destModel = QFileSystemModel()
        self.destModel.setRootPath(QDir.currentPath())
        self.destTree = QTreeView()
        self.destTree.setModel(self.destModel)
        self.destTree.setRootIndex(self.destModel.index(QDir.currentPath()))
        self.destTree.setAnimated(False)
        self.destTree.setIndentation(20)
        self.destTree.setSortingEnabled(True)

        self.extractButton = QPushButton()
        self.extractButton.setText('====>')
        self.extractButton.clicked.connect(self.extract)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.srcTree)
        mainLayout.addWidget(self.extractButton)
        mainLayout.addWidget(self.destTree)
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(mainLayout)
        self.setCentralWidget(self.centralWidget)

        self.show()

    def browseSrcFolder(self):

        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open the source folder',
                                                     QDir.currentPath())

        if directory:
            self.srcTree.setRootIndex(self.srcModel.index(directory))

    def browseDestFolder(self):

        directory = QFileDialog.getExistingDirectory(self,
                                                     'Open the source folder',
                                                     QDir.currentPath())

        if directory:
            self.destTree.setRootIndex(self.destModel.index(directory))

    def extract(self):

        selectionModel = self.srcTree.selectionModel()
        indexes = selectionModel.selectedRows(0)
        logFilenameList = []
        excelFilenameList = []
        for index in indexes:
            logFilename = self.srcModel.filePath(index)
            excelFilename = QDir(
                self.destModel.filePath(
                    self.destTree.rootIndex())).absoluteFilePath(
                        self.srcModel.fileName(index).replace('.log', '.xlsx'))
            logFilenameList.append(logFilename)
            excelFilenameList.append(excelFilename)
        self.extractThread = ExtractThread()
        self.extractThread.setLogFilenameList(logFilenameList)
        self.extractThread.setExcelFilenameList(excelFilenameList)
        self.extractThread.completed.connect(self.updateStatusBar)
        self.extractThread.start()

        # for index in indexes:
        #     logFilename = self.srcModel.filePath(index)
        #     excelFilename = QDir(self.destModel.filePath(self.destTree.rootIndex())).absoluteFilePath(self.srcModel.fileName(index).replace('.log', '.xlsx'))
        #     data = parseFile(logFilename)
        #     saveToExcel(excelFilename, data)

    def updateStatusBar(self, message):
        self.statusBar().showMessage(message)


class ExtractThread(QThread):

    completed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExtractThread, self).__init__(parent)
        self.logFilenameList = None
        self.excelFilenameList = None

    def setLogFilenameList(self, logFilenameList):
        self.logFilenameList = logFilenameList

    def setExcelFilenameList(self, excelFilenameList):
        self.excelFilenameList = excelFilenameList

    def run(self):

        i = 0
        total = len(self.logFilenameList)
        for (logFilename, excelFilename) in zip(self.logFilenameList,
                                                self.excelFilenameList):
            data = parseFile(logFilename)
            saveToExcel(excelFilename, data)
            i = i + 1
            self.completed.emit(
                logFilename +
                ' was successfully extracted! - - - - - - %d/%d' % (i, total))
        self.quit()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
