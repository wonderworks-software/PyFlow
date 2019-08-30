# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:/GIT/PyFlow/PyFlow/UI/Views\PinWidget_ui.ui',
# licensing of 'd:/GIT/PyFlow/PyFlow/UI/Views\PinWidget_ui.ui' applies.
#
# Created: Tue Jun 11 12:28:18 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCompat, QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(168, 75)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(7)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lePinName = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lePinName.sizePolicy().hasHeightForWidth())
        self.lePinName.setSizePolicy(sizePolicy)
        self.lePinName.setMinimumSize(QtCore.QSize(0, 0))
        self.lePinName.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lePinName.setObjectName("lePinName")
        self.horizontalLayout.addWidget(self.lePinName)
        self.cbType = QtWidgets.QComboBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbType.sizePolicy().hasHeightForWidth())
        self.cbType.setSizePolicy(sizePolicy)
        self.cbType.setObjectName("cbType")
        self.horizontalLayout.addWidget(self.cbType)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbHideLabel = QtWidgets.QCheckBox(Form)
        self.cbHideLabel.setObjectName("cbHideLabel")
        self.horizontalLayout_2.addWidget(self.cbHideLabel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCompat.translate("Form", "Form", None, -1))
        self.lePinName.setText(QtCompat.translate("Form", "pinName", None, -1))
        self.cbHideLabel.setToolTip(QtCompat.translate("Form", "should hide label", None, -1))
        self.cbHideLabel.setText(QtCompat.translate("Form", "hide label", None, -1))

