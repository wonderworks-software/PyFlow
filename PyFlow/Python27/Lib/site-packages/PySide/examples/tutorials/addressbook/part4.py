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
    NavigationMode, AddingMode, EditingMode = range(3)

    def __init__(self, parent=None):
        super(AddressBook, self).__init__(parent)

        self.contacts = SortedDict()
        self.oldName = ''
        self.oldAddress = ''
        self.currentMode = self.NavigationMode

        nameLabel = QtGui.QLabel("Name:")
        self.nameLine = QtGui.QLineEdit()
        self.nameLine.setReadOnly(True)

        addressLabel = QtGui.QLabel("Address:")
        self.addressText = QtGui.QTextEdit()
        self.addressText.setReadOnly(True)

        self.addButton = QtGui.QPushButton("&Add")
        self.addButton.show()
        self.editButton = QtGui.QPushButton("&Edit")
        self.editButton.setEnabled(False)
        self.removeButton = QtGui.QPushButton("&Remove")
        self.removeButton.setEnabled(False)
        self.submitButton = QtGui.QPushButton("&Submit")
        self.submitButton.hide()
        self.cancelButton = QtGui.QPushButton("&Cancel")
        self.cancelButton.hide()

        self.nextButton = QtGui.QPushButton("&Next")
        self.nextButton.setEnabled(False)
        self.previousButton = QtGui.QPushButton("&Previous")
        self.previousButton.setEnabled(False)

        self.addButton.clicked.connect(self.addContact)
        self.submitButton.clicked.connect(self.submitContact)
        self.editButton.clicked.connect(self.editContact)
        self.removeButton.clicked.connect(self.removeContact)
        self.cancelButton.clicked.connect(self.cancel)
        self.nextButton.clicked.connect(self.next)
        self.previousButton.clicked.connect(self.previous)

        buttonLayout1 = QtGui.QVBoxLayout()
        buttonLayout1.addWidget(self.addButton)
        buttonLayout1.addWidget(self.editButton)
        buttonLayout1.addWidget(self.removeButton)
        buttonLayout1.addWidget(self.submitButton)
        buttonLayout1.addWidget(self.cancelButton)
        buttonLayout1.addStretch()

        buttonLayout2 = QtGui.QHBoxLayout()
        buttonLayout2.addWidget(self.previousButton)
        buttonLayout2.addWidget(self.nextButton)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addWidget(self.nameLine, 0, 1)
        mainLayout.addWidget(addressLabel, 1, 0, QtCore.Qt.AlignTop)
        mainLayout.addWidget(self.addressText, 1, 1)
        mainLayout.addLayout(buttonLayout1, 1, 2)
        mainLayout.addLayout(buttonLayout2, 3, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Simple Address Book")

    def addContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.nameLine.clear()
        self.addressText.clear()

        self.updateInterface(self.AddingMode)

    def editContact(self):
        self.oldName = self.nameLine.text()
        self.oldAddress = self.addressText.toPlainText()

        self.updateInterface(self.EditingMode)

    def submitContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name == "" or address == "":
            QtGui.QMessageBox.information(self, "Empty Field",
                    "Please enter a name and address.")
            return

        if self.currentMode == self.AddingMode:
            if name not in self.contacts:
                self.contacts[name] = address
                QtGui.QMessageBox.information(self, "Add Successful",
                        "\"%s\" has been added to your address book." % name)
            else:
                QtGui.QMessageBox.information(self, "Add Unsuccessful",
                        "Sorry, \"%s\" is already in your address book." % name)
                return

        elif self.currentMode == self.EditingMode:
            if self.oldName != name:
                if name not in self.contacts:
                    QtGui.QMessageBox.information(self, "Edit Successful",
                            "\"%s\" has been edited in your address book." % self.oldName)
                    del self.contacts[self.oldName]
                    self.contacts[name] = address
                else:
                    QtGui.QMessageBox.information(self, "Edit Unsuccessful",
                            "Sorry, \"%s\" is already in your address book." % name)
                    return
            elif self.oldAddress != address:
                QtGui.QMessageBox.information(self, "Edit Successful",
                        "\"%s\" has been edited in your address book." % name)
                self.contacts[name] = address

        self.updateInterface(self.NavigationMode)

    def cancel(self):
        self.nameLine.setText(self.oldName)
        self.addressText.setText(self.oldAddress)
        self.updateInterface(self.NavigationMode)

    def removeContact(self):
        name = self.nameLine.text()
        address = self.addressText.toPlainText()

        if name in self.contacts:
            button = QtGui.QMessageBox.question(self, "Confirm Remove",
                    "Are you sure you want to remove \"%s\"?" % name,
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if button == QtGui.QMessageBox.Yes:
                self.previous()
                del self.contacts[name]

                QtGui.QMessageBox.information(self, "Remove Successful",
                        "\"%s\" has been removed from your address book." % name)

        self.updateInterface(self.NavigationMode)

    def next(self):
        name = self.nameLine.text()
        it = iter(self.contacts)

        try:
            while True:
                this_name, _ = it.next()

                if this_name == name:
                    next_name, next_address = it.next()
                    break
        except StopIteration:
            next_name, next_address = iter(self.contacts).next()

        self.nameLine.setText(next_name)
        self.addressText.setText(next_address)

    def previous(self):
        name = self.nameLine.text()

        prev_name = prev_address = None
        for this_name, this_address in self.contacts:
            if this_name == name:
                break

            prev_name = this_name
            prev_address = this_address
        else:
            self.nameLine.clear()
            self.addressText.clear()
            return

        if prev_name is None:
            for prev_name, prev_address in self.contacts:
                pass

        self.nameLine.setText(prev_name)
        self.addressText.setText(prev_address)

    def updateInterface(self, mode):
        self.currentMode = mode

        if self.currentMode in (self.AddingMode, self.EditingMode):
            self.nameLine.setReadOnly(False)
            self.nameLine.setFocus(QtCore.Qt.OtherFocusReason)
            self.addressText.setReadOnly(False)

            self.addButton.setEnabled(False)
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)

            self.nextButton.setEnabled(False)
            self.previousButton.setEnabled(False)

            self.submitButton.show()
            self.cancelButton.show()

        elif self.currentMode == self.NavigationMode:
            if not self.contacts:
                self.nameLine.clear()
                self.addressText.clear()

            self.nameLine.setReadOnly(True)
            self.addressText.setReadOnly(True)
            self.addButton.setEnabled(True)

            number = len(self.contacts)
            self.editButton.setEnabled(number >= 1)
            self.removeButton.setEnabled(number >= 1)
            self.nextButton.setEnabled(number > 1)
            self.previousButton.setEnabled(number >1 )

            self.submitButton.hide()
            self.cancelButton.hide()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    addressBook = AddressBook()
    addressBook.show()

    sys.exit(app.exec_())
