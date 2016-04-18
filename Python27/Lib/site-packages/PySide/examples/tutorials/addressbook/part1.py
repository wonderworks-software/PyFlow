#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
## Contact: Qt Software Information (qt-info@nokia.com)
##
## This file is part of the example classes of the Qt Toolkit.
##
#############################################################################

from PySide import QtCore, QtGui


class AddressBook(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        nameLabel = QtGui.QLabel("Name:")
        self.nameLine = QtGui.QLineEdit()

        addressLabel = QtGui.QLabel("Address:")
        self.addressText = QtGui.QTextEdit()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
