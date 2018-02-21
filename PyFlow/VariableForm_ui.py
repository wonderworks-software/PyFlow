# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/VariableForm_ui.ui'
#
# Created: Wed Feb 21 14:51:10 2018
#      by: pyside2-uic 2.0.0 running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(94, 26)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout.addWidget(self.widget)
        self.labelName = QtWidgets.QLabel(Form)
        self.labelName.setObjectName("labelName")
        self.horizontalLayout.addWidget(self.labelName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
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
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.labelName.setText(QtCompat.translate("Form", "var name", None, -1))

import nodes_res_rc
