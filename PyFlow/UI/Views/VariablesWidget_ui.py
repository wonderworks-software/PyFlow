# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/PyFlow/PyFlow/UI/Views\VariablesWidget_ui.ui',
# licensing of 'd:/GIT/PyFlow/PyFlow/UI/Views\VariablesWidget_ui.ui' applies.
#
# Created: Mon Apr 15 11:38:35 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(342, 385)
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
        self.wListWidget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wListWidget.sizePolicy().hasHeightForWidth())
        self.wListWidget.setSizePolicy(sizePolicy)
        self.wListWidget.setObjectName("wListWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.wListWidget)
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.gridLayout.setObjectName("gridLayout")
        self.lytListWidget = QtWidgets.QVBoxLayout()
        self.lytListWidget.setContentsMargins(0, 0, 0, 0)
        self.lytListWidget.setObjectName("lytListWidget")
        self.gridLayout.addLayout(self.lytListWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.wListWidget)
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
