# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/VariablesWidget_ui.ui'
#
# Created: Sun Mar 11 16:56:55 2018
#      by: pyside2-uic 2.0.0 running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(367, 437)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbNewVar = QtWidgets.QPushButton(Form)
        self.pbNewVar.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pbNewVar.setObjectName("pbNewVar")
        self.horizontalLayout.addWidget(self.pbNewVar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setSelectionRectVisible(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pbKillVar = QtWidgets.QPushButton(Form)
        self.pbKillVar.setMaximumSize(QtCore.QSize(50, 16777215))
        self.pbKillVar.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/delete_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbKillVar.setIcon(icon)
        self.pbKillVar.setObjectName("pbKillVar")
        self.horizontalLayout_2.addWidget(self.pbKillVar)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.label.setText(QtCompat.translate("Form", "Create var", None, -1))
        self.pbNewVar.setText(QtCompat.translate("Form", "+", None, -1))
        self.label_2.setText(QtCompat.translate("Form", "Kill selected var", None, -1))

import nodes_res_rc
