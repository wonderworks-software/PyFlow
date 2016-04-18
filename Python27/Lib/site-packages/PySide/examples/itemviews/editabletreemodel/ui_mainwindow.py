# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Dec 29 13:22:05 2011
#      by: pyside-uic 0.2.13 running on PySide 1.0.9
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(573, 468)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = QtGui.QTreeView(self.centralwidget)
        self.view.setAlternatingRowColors(True)
        self.view.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.view.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.view.setAnimated(False)
        self.view.setAllColumnsShowFocus(True)
        self.view.setObjectName("view")
        self.vboxlayout.addWidget(self.view)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 573, 31))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtGui.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.actionsMenu = QtGui.QMenu(self.menubar)
        self.actionsMenu.setObjectName("actionsMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.insertRowAction = QtGui.QAction(MainWindow)
        self.insertRowAction.setObjectName("insertRowAction")
        self.removeRowAction = QtGui.QAction(MainWindow)
        self.removeRowAction.setObjectName("removeRowAction")
        self.insertColumnAction = QtGui.QAction(MainWindow)
        self.insertColumnAction.setObjectName("insertColumnAction")
        self.removeColumnAction = QtGui.QAction(MainWindow)
        self.removeColumnAction.setObjectName("removeColumnAction")
        self.insertChildAction = QtGui.QAction(MainWindow)
        self.insertChildAction.setObjectName("insertChildAction")
        self.fileMenu.addAction(self.exitAction)
        self.actionsMenu.addAction(self.insertRowAction)
        self.actionsMenu.addAction(self.insertColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.removeRowAction)
        self.actionsMenu.addAction(self.removeColumnAction)
        self.actionsMenu.addSeparator()
        self.actionsMenu.addAction(self.insertChildAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.actionsMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Editable Tree Model", None, QtGui.QApplication.UnicodeUTF8))
        self.fileMenu.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionsMenu.setTitle(QtGui.QApplication.translate("MainWindow", "&Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.exitAction.setText(QtGui.QApplication.translate("MainWindow", "E&xit", None, QtGui.QApplication.UnicodeUTF8))
        self.exitAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.insertRowAction.setText(QtGui.QApplication.translate("MainWindow", "Insert Row", None, QtGui.QApplication.UnicodeUTF8))
        self.insertRowAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+I, R", None, QtGui.QApplication.UnicodeUTF8))
        self.removeRowAction.setText(QtGui.QApplication.translate("MainWindow", "Remove Row", None, QtGui.QApplication.UnicodeUTF8))
        self.removeRowAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R, R", None, QtGui.QApplication.UnicodeUTF8))
        self.insertColumnAction.setText(QtGui.QApplication.translate("MainWindow", "Insert Column", None, QtGui.QApplication.UnicodeUTF8))
        self.insertColumnAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+I, C", None, QtGui.QApplication.UnicodeUTF8))
        self.removeColumnAction.setText(QtGui.QApplication.translate("MainWindow", "Remove Column", None, QtGui.QApplication.UnicodeUTF8))
        self.removeColumnAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R, C", None, QtGui.QApplication.UnicodeUTF8))
        self.insertChildAction.setText(QtGui.QApplication.translate("MainWindow", "Insert Child", None, QtGui.QApplication.UnicodeUTF8))
        self.insertChildAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))

import editabletreemodel_rc
