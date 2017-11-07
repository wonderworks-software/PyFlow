# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/BaseNode.ui'
#
# Created: Tue Nov 07 11:52:07 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_BaseNodeUI(object):
    def setupUi(self, BaseNodeUI):
        BaseNodeUI.setObjectName("BaseNodeUI")
        BaseNodeUI.resize(249, 393)
        self.gridLayout = QtGui.QGridLayout(BaseNodeUI)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lytExecsIn = QtGui.QVBoxLayout()
        self.lytExecsIn.setObjectName("lytExecsIn")
        self.widget_3 = QtGui.QWidget(BaseNodeUI)
        self.widget_3.setMinimumSize(QtCore.QSize(30, 0))
        self.widget_3.setObjectName("widget_3")
        self.lytExecsIn.addWidget(self.widget_3)
        self.horizontalLayout_3.addLayout(self.lytExecsIn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.lytExecsOut = QtGui.QVBoxLayout()
        self.lytExecsOut.setObjectName("lytExecsOut")
        self.widget_4 = QtGui.QWidget(BaseNodeUI)
        self.widget_4.setMinimumSize(QtCore.QSize(30, 0))
        self.widget_4.setObjectName("widget_4")
        self.lytExecsOut.addWidget(self.widget_4)
        self.horizontalLayout_3.addLayout(self.lytExecsOut)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtGui.QWidget(BaseNodeUI)
        self.widget.setMinimumSize(QtCore.QSize(0, 30))
        self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.widget)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtGui.QWidget(BaseNodeUI)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 30))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2.addWidget(self.widget_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)

        self.retranslateUi(BaseNodeUI)
        QtCore.QMetaObject.connectSlotsByName(BaseNodeUI)

    def retranslateUi(self, BaseNodeUI):
        BaseNodeUI.setWindowTitle(QtGui.QApplication.translate("BaseNodeUI", "Form", None, QtGui.QApplication.UnicodeUTF8))

