# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'embeddeddialog.ui'
#
# Created: Wed May 28 15:07:08 2008
#      by: PyQt4 UI code generator 4.4.3-snapshot-20080526
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_embeddedDialog(object):
    def setupUi(self, embeddedDialog):
        embeddedDialog.setObjectName("embeddedDialog")
        embeddedDialog.resize(407,134)
        self.formLayout = QtGui.QFormLayout(embeddedDialog)
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(embeddedDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0,QtGui.QFormLayout.LabelRole,self.label)
        self.layoutDirection = QtGui.QComboBox(embeddedDialog)
        self.layoutDirection.setObjectName("layoutDirection")
        self.formLayout.setWidget(0,QtGui.QFormLayout.FieldRole,self.layoutDirection)
        self.label_2 = QtGui.QLabel(embeddedDialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1,QtGui.QFormLayout.LabelRole,self.label_2)
        self.fontComboBox = QtGui.QFontComboBox(embeddedDialog)
        self.fontComboBox.setObjectName("fontComboBox")
        self.formLayout.setWidget(1,QtGui.QFormLayout.FieldRole,self.fontComboBox)
        self.label_3 = QtGui.QLabel(embeddedDialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2,QtGui.QFormLayout.LabelRole,self.label_3)
        self.style = QtGui.QComboBox(embeddedDialog)
        self.style.setObjectName("style")
        self.formLayout.setWidget(2,QtGui.QFormLayout.FieldRole,self.style)
        self.label_4 = QtGui.QLabel(embeddedDialog)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3,QtGui.QFormLayout.LabelRole,self.label_4)
        self.spacing = QtGui.QSlider(embeddedDialog)
        self.spacing.setOrientation(QtCore.Qt.Horizontal)
        self.spacing.setObjectName("spacing")
        self.formLayout.setWidget(3,QtGui.QFormLayout.FieldRole,self.spacing)
        self.label.setBuddy(self.layoutDirection)
        self.label_2.setBuddy(self.fontComboBox)
        self.label_3.setBuddy(self.style)
        self.label_4.setBuddy(self.spacing)

        self.retranslateUi(embeddedDialog)
        QtCore.QMetaObject.connectSlotsByName(embeddedDialog)

    def retranslateUi(self, embeddedDialog):
        embeddedDialog.setWindowTitle(QtGui.QApplication.translate("embeddedDialog", "Embedded Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("embeddedDialog", "Layout Direction:", None, QtGui.QApplication.UnicodeUTF8))
        self.layoutDirection.addItem(QtGui.QApplication.translate("embeddedDialog", "Left to Right", None, QtGui.QApplication.UnicodeUTF8))
        self.layoutDirection.addItem(QtGui.QApplication.translate("embeddedDialog", "Right to Left", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("embeddedDialog", "Select Font:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("embeddedDialog", "Style:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("embeddedDialog", "Layout spacing:", None, QtGui.QApplication.UnicodeUTF8))

