#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
#############################################################################

from PySide import QtCore, QtGui


class PreviewWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PreviewWindow, self).__init__(parent)

        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setLineWrapMode(QtGui.QTextEdit.NoWrap)

        closeButton = QtGui.QPushButton("&Close")
        closeButton.clicked.connect(self.close)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(closeButton)
        self.setLayout(layout)

        self.setWindowTitle("Preview")

    def setWindowFlags(self, flags):
        super(PreviewWindow, self).setWindowFlags(flags)

        flag_type = (flags & QtCore.Qt.WindowType_Mask)

        if flag_type == QtCore.Qt.Window:
            text = "QtCore.Qt.Window"
        elif flag_type == QtCore.Qt.Dialog:
            text = "QtCore.Qt.Dialog"
        elif flag_type == QtCore.Qt.Sheet:
            text = "QtCore.Qt.Sheet"
        elif flag_type == QtCore.Qt.Drawer:
            text = "QtCore.Qt.Drawer"
        elif flag_type == QtCore.Qt.Popup:
            text = "QtCore.Qt.Popup"
        elif flag_type == QtCore.Qt.Tool:
            text = "QtCore.Qt.Tool"
        elif flag_type == QtCore.Qt.ToolTip:
            text = "QtCore.Qt.ToolTip"
        elif flag_type == QtCore.Qt.SplashScreen:
            text = "QtCore.Qt.SplashScreen"
        else:
            text = ""

        if flags & QtCore.Qt.MSWindowsFixedSizeDialogHint:
            text += "\n| QtCore.Qt.MSWindowsFixedSizeDialogHint"
        if flags & QtCore.Qt.X11BypassWindowManagerHint:
            text += "\n| QtCore.Qt.X11BypassWindowManagerHint"
        if flags & QtCore.Qt.FramelessWindowHint:
            text += "\n| QtCore.Qt.FramelessWindowHint"
        if flags & QtCore.Qt.WindowTitleHint:
            text += "\n| QtCore.Qt.WindowTitleHint"
        if flags & QtCore.Qt.WindowSystemMenuHint:
            text += "\n| QtCore.Qt.WindowSystemMenuHint"
        if flags & QtCore.Qt.WindowMinimizeButtonHint:
            text += "\n| QtCore.Qt.WindowMinimizeButtonHint"
        if flags & QtCore.Qt.WindowMaximizeButtonHint:
            text += "\n| QtCore.Qt.WindowMaximizeButtonHint"
        if flags & QtCore.Qt.WindowCloseButtonHint:
            text += "\n| QtCore.Qt.WindowCloseButtonHint"
        if flags & QtCore.Qt.WindowContextHelpButtonHint:
            text += "\n| QtCore.Qt.WindowContextHelpButtonHint"
        if flags & QtCore.Qt.WindowShadeButtonHint:
            text += "\n| QtCore.Qt.WindowShadeButtonHint"
        if flags & QtCore.Qt.WindowStaysOnTopHint:
            text += "\n| QtCore.Qt.WindowStaysOnTopHint"
        if flags & QtCore.Qt.WindowStaysOnBottomHint:
            text += "\n| QtCore.Qt.WindowStaysOnBottomHint"
        if flags & QtCore.Qt.CustomizeWindowHint:
            text += "\n| QtCore.Qt.CustomizeWindowHint"

        self.textEdit.setPlainText(text)


class ControllerWindow(QtGui.QWidget):
    def __init__(self):
        super(ControllerWindow, self).__init__()

        self.previewWindow = PreviewWindow(self)

        self.createTypeGroupBox()
        self.createHintsGroupBox()

        quitButton = QtGui.QPushButton("&Quit")
        quitButton.clicked.connect(self.close)

        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addStretch()
        bottomLayout.addWidget(quitButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.typeGroupBox)
        mainLayout.addWidget(self.hintsGroupBox)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)

        self.setWindowTitle("Window Flags")
        self.updatePreview()

    def updatePreview(self):
        flags = QtCore.Qt.WindowFlags()

        if self.windowRadioButton.isChecked():
            flags = QtCore.Qt.Window
        elif self.dialogRadioButton.isChecked():
            flags = QtCore.Qt.Dialog
        elif self.sheetRadioButton.isChecked():
            flags = QtCore.Qt.Sheet
        elif self.drawerRadioButton.isChecked():
            flags = QtCore.Qt.Drawer
        elif self.popupRadioButton.isChecked():
            flags = QtCore.Qt.Popup
        elif self.toolRadioButton.isChecked():
            flags = QtCore.Qt.Tool
        elif self.toolTipRadioButton.isChecked():
            flags = QtCore.Qt.ToolTip
        elif self.splashScreenRadioButton.isChecked():
            flags = QtCore.Qt.SplashScreen

        if self.msWindowsFixedSizeDialogCheckBox.isChecked():
            flags |= QtCore.Qt.MSWindowsFixedSizeDialogHint            
        if self.x11BypassWindowManagerCheckBox.isChecked():
            flags |= QtCore.Qt.X11BypassWindowManagerHint
        if self.framelessWindowCheckBox.isChecked():
            flags |= QtCore.Qt.FramelessWindowHint
        if self.windowTitleCheckBox.isChecked():
            flags |= QtCore.Qt.WindowTitleHint
        if self.windowSystemMenuCheckBox.isChecked():
            flags |= QtCore.Qt.WindowSystemMenuHint
        if self.windowMinimizeButtonCheckBox.isChecked():
            flags |= QtCore.Qt.WindowMinimizeButtonHint
        if self.windowMaximizeButtonCheckBox.isChecked():
            flags |= QtCore.Qt.WindowMaximizeButtonHint
        if self.windowCloseButtonCheckBox.isChecked():
            flags |= QtCore.Qt.WindowCloseButtonHint
        if self.windowContextHelpButtonCheckBox.isChecked():
            flags |= QtCore.Qt.WindowContextHelpButtonHint
        if self.windowShadeButtonCheckBox.isChecked():
            flags |= QtCore.Qt.WindowShadeButtonHint
        if self.windowStaysOnTopCheckBox.isChecked():
            flags |= QtCore.Qt.WindowStaysOnTopHint
        if self.windowStaysOnBottomCheckBox.isChecked():
            flags |= QtCore.Qt.WindowStaysOnBottomHint
        if self.customizeWindowHintCheckBox.isChecked():
            flags |= QtCore.Qt.CustomizeWindowHint

        self.previewWindow.setWindowFlags(flags)

        pos = self.previewWindow.pos()

        if pos.x() < 0:
            pos.setX(0)

        if pos.y() < 0:
            pos.setY(0)

        self.previewWindow.move(pos)
        self.previewWindow.show()

    def createTypeGroupBox(self):
        self.typeGroupBox = QtGui.QGroupBox("Type")

        self.windowRadioButton = self.createRadioButton("Window")
        self.dialogRadioButton = self.createRadioButton("Dialog")
        self.sheetRadioButton = self.createRadioButton("Sheet")
        self.drawerRadioButton = self.createRadioButton("Drawer")
        self.popupRadioButton = self.createRadioButton("Popup")
        self.toolRadioButton = self.createRadioButton("Tool")
        self.toolTipRadioButton = self.createRadioButton("Tooltip")
        self.splashScreenRadioButton = self.createRadioButton("Splash screen")
        self.windowRadioButton.setChecked(True)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.windowRadioButton, 0, 0)
        layout.addWidget(self.dialogRadioButton, 1, 0)
        layout.addWidget(self.sheetRadioButton, 2, 0)
        layout.addWidget(self.drawerRadioButton, 3, 0)
        layout.addWidget(self.popupRadioButton, 0, 1)
        layout.addWidget(self.toolRadioButton, 1, 1)
        layout.addWidget(self.toolTipRadioButton, 2, 1)
        layout.addWidget(self.splashScreenRadioButton, 3, 1)
        self.typeGroupBox.setLayout(layout)

    def createHintsGroupBox(self):
        self.hintsGroupBox = QtGui.QGroupBox("Hints")

        self.msWindowsFixedSizeDialogCheckBox = self.createCheckBox("MS Windows fixed size dialog")
        self.x11BypassWindowManagerCheckBox = self.createCheckBox("X11 bypass window manager")
        self.framelessWindowCheckBox = self.createCheckBox("Frameless window")
        self.windowTitleCheckBox = self.createCheckBox("Window title")
        self.windowSystemMenuCheckBox = self.createCheckBox("Window system menu")
        self.windowMinimizeButtonCheckBox = self.createCheckBox("Window minimize button")
        self.windowMaximizeButtonCheckBox = self.createCheckBox("Window maximize button")
        self.windowCloseButtonCheckBox = self.createCheckBox("Window close button")
        self.windowContextHelpButtonCheckBox = self.createCheckBox("Window context help button")
        self.windowShadeButtonCheckBox = self.createCheckBox("Window shade button")
        self.windowStaysOnTopCheckBox = self.createCheckBox("Window stays on top")
        self.windowStaysOnBottomCheckBox = self.createCheckBox("Window stays on bottom")
        self.customizeWindowHintCheckBox = self.createCheckBox("Customize window")

        layout = QtGui.QGridLayout()
        layout.addWidget(self.msWindowsFixedSizeDialogCheckBox, 0, 0)
        layout.addWidget(self.x11BypassWindowManagerCheckBox, 1, 0)
        layout.addWidget(self.framelessWindowCheckBox, 2, 0)
        layout.addWidget(self.windowTitleCheckBox, 3, 0)
        layout.addWidget(self.windowSystemMenuCheckBox, 4, 0)
        layout.addWidget(self.windowMinimizeButtonCheckBox, 0, 1)
        layout.addWidget(self.windowMaximizeButtonCheckBox, 1, 1)
        layout.addWidget(self.windowCloseButtonCheckBox, 2, 1)
        layout.addWidget(self.windowContextHelpButtonCheckBox, 3, 1)
        layout.addWidget(self.windowShadeButtonCheckBox, 4, 1)
        layout.addWidget(self.windowStaysOnTopCheckBox, 5, 1)
        layout.addWidget(self.windowStaysOnBottomCheckBox, 6, 1)
        layout.addWidget(self.customizeWindowHintCheckBox, 5, 0)
        self.hintsGroupBox.setLayout(layout)

    def createCheckBox(self, text):
        checkBox = QtGui.QCheckBox(text)
        checkBox.clicked.connect(self.updatePreview)
        return checkBox

    def createRadioButton(self, text):
        button = QtGui.QRadioButton(text)
        button.clicked.connect(self.updatePreview)
        return button


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    controller = ControllerWindow()
    controller.show()
    sys.exit(app.exec_())
