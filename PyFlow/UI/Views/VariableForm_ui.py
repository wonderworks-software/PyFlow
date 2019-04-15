# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/PyFlow/PyFlow/UI/Views\VariableForm_ui.ui',
# licensing of 'd:/GIT/PyFlow/PyFlow/UI/Views\VariableForm_ui.ui' applies.
#
# Created: Mon Apr 15 11:38:35 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(217, 28)
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
        self.pbKill = QtWidgets.QPushButton(Form)
        self.pbKill.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pbKill.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/delete_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbKill.setIcon(icon)
        self.pbKill.setObjectName("pbKill")
        self.horizontalLayout.addWidget(self.pbKill)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.labelName.setText(QtCompat.translate("Form", "var name", None, -1))

import nodes_res_rc
