# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/VariableForm_ui.ui'
#
# Created: Fri Feb 02 22:36:17 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(94, 26)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.labelName = QtGui.QLabel(Form)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/delete_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.labelName.setText(QtGui.QApplication.translate("Form", "var name", None, QtGui.QApplication.UnicodeUTF8))

import nodes_res_rc
