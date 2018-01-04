# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/nodes/PyFlow/PinWidget_ui.ui'
#
# Created: Thu Jan 04 21:58:47 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(168, 72)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lePinName = QtGui.QLineEdit(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lePinName.sizePolicy().hasHeightForWidth())
        self.lePinName.setSizePolicy(sizePolicy)
        self.lePinName.setMinimumSize(QtCore.QSize(0, 0))
        self.lePinName.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lePinName.setObjectName("lePinName")
        self.horizontalLayout.addWidget(self.lePinName)
        self.cbType = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbType.sizePolicy().hasHeightForWidth())
        self.cbType.setSizePolicy(sizePolicy)
        self.cbType.setObjectName("cbType")
        self.horizontalLayout.addWidget(self.cbType)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbHideLabel = QtGui.QCheckBox(Form)
        self.cbHideLabel.setObjectName("cbHideLabel")
        self.horizontalLayout_2.addWidget(self.cbHideLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lePinName.setText(QtGui.QApplication.translate("Form", "pinName", None, QtGui.QApplication.UnicodeUTF8))
        self.cbHideLabel.setToolTip(QtGui.QApplication.translate("Form", "should hide label", None, QtGui.QApplication.UnicodeUTF8))
        self.cbHideLabel.setText(QtGui.QApplication.translate("Form", "hide label", None, QtGui.QApplication.UnicodeUTF8))

import nodes_res_rc
