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


class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.createFirstExclusiveGroup(), 0, 0)
        grid.addWidget(self.createSecondExclusiveGroup(), 1, 0)
        grid.addWidget(self.createNonExclusiveGroup(), 0, 1)
        grid.addWidget(self.createPushButtonGroup(), 1, 1)
        self.setLayout(grid)

        self.setWindowTitle("Group Box")
        self.resize(480, 320)

    def createFirstExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("Exclusive Radio Buttons")

        radio1 = QtGui.QRadioButton("&Radio button 1")
        radio2 = QtGui.QRadioButton("R&adio button 2")
        radio3 = QtGui.QRadioButton("Ra&dio button 3")

        radio1.setChecked(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createSecondExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("E&xclusive Radio Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(False)

        radio1 = QtGui.QRadioButton("Rad&io button 1")
        radio2 = QtGui.QRadioButton("Radi&o button 2")
        radio3 = QtGui.QRadioButton("Radio &button 3")
        radio1.setChecked(True)
        checkBox = QtGui.QCheckBox("Ind&ependent checkbox")
        checkBox.setChecked(True)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(radio3)
        vbox.addWidget(checkBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createNonExclusiveGroup(self):
        groupBox = QtGui.QGroupBox("Non-Exclusive Checkboxes")
        groupBox.setFlat(True)

        checkBox1 = QtGui.QCheckBox("&Checkbox 1")
        checkBox2 = QtGui.QCheckBox("C&heckbox 2")
        checkBox2.setChecked(True)
        tristateBox = QtGui.QCheckBox("Tri-&state button")
        tristateBox.setTristate(True)
        tristateBox.setCheckState(QtCore.Qt.PartiallyChecked)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(checkBox1)
        vbox.addWidget(checkBox2)
        vbox.addWidget(tristateBox)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def createPushButtonGroup(self):
        groupBox = QtGui.QGroupBox("&Push Buttons")
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        pushButton = QtGui.QPushButton("&Normal Button")
        toggleButton = QtGui.QPushButton("&Toggle Button")
        toggleButton.setCheckable(True)
        toggleButton.setChecked(True)
        flatButton = QtGui.QPushButton("&Flat Button")
        flatButton.setFlat(True)

        popupButton = QtGui.QPushButton("Pop&up Button")
        menu = QtGui.QMenu(self)
        menu.addAction("&First Item")
        menu.addAction("&Second Item")
        menu.addAction("&Third Item")
        menu.addAction("F&ourth Item")
        popupButton.setMenu(menu)

        newAction = menu.addAction("Submenu")
        subMenu = QtGui.QMenu("Popup Submenu", self)
        subMenu.addAction("Item 1")
        subMenu.addAction("Item 2")
        subMenu.addAction("Item 3")
        newAction.setMenu(subMenu)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(pushButton)
        vbox.addWidget(toggleButton)
        vbox.addWidget(flatButton)
        vbox.addWidget(popupButton)
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())
