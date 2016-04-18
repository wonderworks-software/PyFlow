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


class SortedDict(dict):
    class Iterator(object):
        def __init__(self, sorted_dict):
            self._dict = sorted_dict
            self._keys = sorted(self._dict.keys())
            self._nr_items = len(self._keys)
            self._idx = 0

        def __iter__(self):
            return self

        def next(self):
            if self._idx >= self._nr_items:
                raise StopIteration

            key = self._keys[self._idx]
            value = self._dict[key]
            self._idx += 1

            return key, value

        __next__ = next

    def __iter__(self):
        return SortedDict.Iterator(self)

    iterkeys = __iter__


class AddressBook(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        self.contacts = SortedDict()
        self.oldName = ''
        self.oldAddress = ''

        nameLabel = QtGui.QLabel("Name:")
        self.nameLine = QtGui.QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QtGui.QLabel("Address:")
        self.addressText = QtGui.QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QtGui.QPushButton("&Add")
        self.addButton.show()
        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.hide()
        self.cancelButton = QtGui.QPushButton("&Cancel")
        self.cancelButton.hide()

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.cancelButton.clicked.connect(self.cancel)

        buttonLayout1 = QtGui.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton, QtCore.Qt.AlignTop)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addStretch()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.nameLine.setReadOnly(False)
        self.nameLine.setFocus(QtCore.Qt.OtherFocusReason)
        self.addressText.setReadOnly(False)

        self.addButton.setEnabled(False)
        self.submitButton.show()
        self.cancelButton.show()

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a name and address.")
            return

        if name not in self.contacts:
            self.contacts[name] = address
            QtGui.QMessageBox.information(self, "Add Successful",
                    "\"%s\" has been added to your address book." % name)
        else:
            QtGui.QMessageBox.information(self, "Add Unsuccessful",
                    "Sorry, \"%s\" is already in your address book." % name)
            return

        if not self.contacts:
            self.nameLine.clear()
            self.addressText.clear()

        self.nameLine.setReadOnly(True)
        self.addressText.setReadOnly(True)
        self.addButton.setEnabled(True)
        self.submitButton.hide()
        self.cancelButton.hide()

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.nameLine.setReadOnly(True)

        self.addressText.setText(self.oldAddress)
        self.addressText.setReadOnly(True)

        self.addButton.setEnabled(True)
        self.submitButton.hide()
        self.cancelButton.hide()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
