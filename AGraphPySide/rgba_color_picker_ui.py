# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\GIT\Nodes\AGraphPySide\rgba_color_picker_ui.ui'
#
# Created: Fri Aug 14 16:40:02 2015
#      by: pyside-uic 0.2.14 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_rgba_color_picker_ui(object):
    def setupUi(self, rgba_color_picker_ui):
        rgba_color_picker_ui.setObjectName("rgba_color_picker_ui")
        rgba_color_picker_ui.resize(255, 99)
        self.gridLayout = QtGui.QGridLayout(rgba_color_picker_ui)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.rgbLabel = QtGui.QLabel(rgba_color_picker_ui)
        self.rgbLabel.setObjectName("rgbLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.rgbLabel)
        self.alphaLabel = QtGui.QLabel(rgba_color_picker_ui)
        self.alphaLabel.setObjectName("alphaLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.alphaLabel)
        self.pb_color = QtGui.QPushButton(rgba_color_picker_ui)
        self.pb_color.setStyleSheet("")
        self.pb_color.setText("")
        self.pb_color.setObjectName("pb_color")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.pb_color)
        self.hs_alpha = QtGui.QSlider(rgba_color_picker_ui)
        self.hs_alpha.setMinimum(0)
        self.hs_alpha.setMaximum(255)
        self.hs_alpha.setSingleStep(15)
        self.hs_alpha.setProperty("value", 255)
        self.hs_alpha.setOrientation(QtCore.Qt.Horizontal)
        self.hs_alpha.setTickPosition(QtGui.QSlider.TicksBelow)
        self.hs_alpha.setTickInterval(15)
        self.hs_alpha.setObjectName("hs_alpha")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.hs_alpha)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.pb_apply = QtGui.QPushButton(rgba_color_picker_ui)
        self.pb_apply.setObjectName("pb_apply")
        self.gridLayout.addWidget(self.pb_apply, 1, 0, 1, 1)

        self.retranslateUi(rgba_color_picker_ui)
        QtCore.QMetaObject.connectSlotsByName(rgba_color_picker_ui)

    def retranslateUi(self, rgba_color_picker_ui):
        rgba_color_picker_ui.setWindowTitle(QtGui.QApplication.translate("rgba_color_picker_ui", "RGBA color picker", None, QtGui.QApplication.UnicodeUTF8))
        self.rgbLabel.setText(QtGui.QApplication.translate("rgba_color_picker_ui", "rgb", None, QtGui.QApplication.UnicodeUTF8))
        self.alphaLabel.setText(QtGui.QApplication.translate("rgba_color_picker_ui", "alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_apply.setText(QtGui.QApplication.translate("rgba_color_picker_ui", "apply", None, QtGui.QApplication.UnicodeUTF8))

