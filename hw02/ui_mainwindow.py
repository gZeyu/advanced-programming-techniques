# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/bigding/Code/advanced-programming-techniques/hw02/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(608, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(456, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.refreshPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshPushButton.setObjectName("refreshPushButton")
        self.horizontalLayout.addWidget(self.refreshPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 608, 22))
        self.menubar.setObjectName("menubar")
        self.menuOpen_Folder = QtWidgets.QMenu(self.menubar)
        self.menuOpen_Folder.setObjectName("menuOpen_Folder")
        self.menu_Help = QtWidgets.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuOpen_Folder.addAction(self.actionOpen_Folder)
        self.menuOpen_Folder.addAction(self.actionSave_As)
        self.menuOpen_Folder.addSeparator()
        self.menuOpen_Folder.addAction(self.actionExit)
        self.menu_Help.addSeparator()
        self.menu_Help.addSeparator()
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.actionAbout)
        self.menubar.addAction(self.menuOpen_Folder.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.refreshPushButton.setText(_translate("MainWindow", "Refresh"))
        self.menuOpen_Folder.setTitle(_translate("MainWindow", "&File"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Open Folder..."))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As..."))
        self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+S"))

