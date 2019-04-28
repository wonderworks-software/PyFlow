# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\GIT\PyFlow\PyFlow\UI\Widgets\CollapsibleWidget.ui',
# licensing of 'e:\GIT\PyFlow\PyFlow\UI\Widgets\CollapsibleWidget.ui' applies.
#
# Created: Fri Apr 26 13:04:56 2019
#      by: pyside2-uic  running on PySide2 5.12.0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(460, 192)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pbHead = QtWidgets.QPushButton(Form)
        self.pbHead.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.pbHead.setChecked(False)
        self.pbHead.setFlat(False)
        self.pbHead.setObjectName("pbHead")
        self.verticalLayout_2.addWidget(self.pbHead)
        self.ContentWidget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContentWidget.sizePolicy().hasHeightForWidth())
        self.ContentWidget.setSizePolicy(sizePolicy)
        self.ContentWidget.setObjectName("ContentWidget")
        self.verticalLayout_2.addWidget(self.ContentWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.pbHead.setText(QtWidgets.QApplication.translate("Form", "Default", None, -1))
