# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/CodeEditor_ui.ui'
#
# Created: Sun Dec 17 22:56:35 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(727, 391)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbAddInput = QtGui.QPushButton(Form)
        self.pbAddInput.setObjectName("pbAddInput")
        self.horizontalLayout.addWidget(self.pbAddInput)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pbAddOutput = QtGui.QPushButton(Form)
        self.pbAddOutput.setObjectName("pbAddOutput")
        self.horizontalLayout.addWidget(self.pbAddOutput)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lwInputs = QtGui.QListWidget(Form)
        self.lwInputs.setMaximumSize(QtCore.QSize(130, 16777215))
        self.lwInputs.setObjectName("lwInputs")
        self.horizontalLayout_3.addWidget(self.lwInputs)
        self.plainTextEdit = QtGui.QPlainTextEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plainTextEdit.sizePolicy().hasHeightForWidth())
        self.plainTextEdit.setSizePolicy(sizePolicy)
        self.plainTextEdit.setTabStopWidth(20)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_3.addWidget(self.plainTextEdit)
        self.lwOutputs = QtGui.QListWidget(Form)
        self.lwOutputs.setMaximumSize(QtCore.QSize(130, 16777215))
        self.lwOutputs.setObjectName("lwOutputs")
        self.horizontalLayout_3.addWidget(self.lwOutputs)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pbSave = QtGui.QPushButton(Form)
        self.pbSave.setMaximumSize(QtCore.QSize(45, 16777215))
        self.pbSave.setObjectName("pbSave")
        self.horizontalLayout_4.addWidget(self.pbSave)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sbFontSize = QtGui.QSpinBox(Form)
        self.sbFontSize.setProperty("value", 14)
        self.sbFontSize.setObjectName("sbFontSize")
        self.horizontalLayout_2.addWidget(self.sbFontSize)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pbAddInput.setText(QtGui.QApplication.translate("Form", "add input", None, QtGui.QApplication.UnicodeUTF8))
        self.pbAddOutput.setText(QtGui.QApplication.translate("Form", "add output", None, QtGui.QApplication.UnicodeUTF8))
        self.pbSave.setText(QtGui.QApplication.translate("Form", "save", None, QtGui.QApplication.UnicodeUTF8))

