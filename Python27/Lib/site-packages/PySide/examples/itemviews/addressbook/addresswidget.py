#!/usr/bin/python

"""**************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the examples of the Qt Toolkit.
**
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
**     the names of its contributors may be used to endorse or promote
**     products derived from this software without specific prior written
**     permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
*****************************************************************************
** February 2011
** - addressbook example ported to PySide by Arun Srinivasan 
**   <rulfzid@gmail.com>
**************************************************************************"""

try:
    import cpickle as pickle
except ImportError:
    import pickle

from PySide.QtCore import (Qt, Signal, QRegExp, QModelIndex)
from PySide.QtGui import (QWidget, QTabWidget, QItemSelectionModel, 
                          QMessageBox, QTableView, QSortFilterProxyModel,
                          QAbstractItemView, QItemSelection)

from tablemodel import TableModel
from newaddresstab import NewAddressTab
from adddialogwidget import AddDialogWidget


class AddressWidget(QTabWidget):
    """ The central widget of the application. Most of the addressbook's
        functionality is contained in this class.
    """

    selectionChanged = Signal(QItemSelection)

    def __init__(self, parent=None):
        """ Initialize the AddressWidget. """
        super(AddressWidget, self).__init__(parent)

        self.tableModel = TableModel()
        self.newAddressTab = NewAddressTab()
        self.newAddressTab.sendDetails.connect(self.addEntry)

        self.addTab(self.newAddressTab, "Address Book")

        self.setupTabs()

    def addEntry(self, name=None, address=None):
        """ Add an entry to the addressbook. """
        if name is None and address is None:
            addDialog = AddDialogWidget()

            if addDialog.exec_():
                name = addDialog.name
                address = addDialog.address
                
        address = {"name": name, "address": address}
        addresses = self.tableModel.addresses[:]

        # The QT docs for this example state that what we're doing here
        # is checking if the entered name already exists. What they 
        # (and we here) are actually doing is checking if the whole 
        # name/address pair exists already - ok for the purposes of this 
        # example, but obviously not how a real addressbook application
        # should behave.
        try:
            addresses.remove(address)
            QMessageBox.information(self, "Duplicate Name", 
                                    "The name \"%s\" already exists." % name)
        except ValueError:
            # The address didn't already exist, so let's add it to the model.

            # Step 1: create the  row
            self.tableModel.insertRows(0)

            # Step 2: get the index of the newly created row and use it.
            # to set the name
            ix = self.tableModel.index(0, 0, QModelIndex())
            self.tableModel.setData(ix, address["name"], Qt.EditRole)

            # Step 3: lather, rinse, repeat for the address.
            ix = self.tableModel.index(0, 1, QModelIndex())
            self.tableModel.setData(ix, address["address"], Qt.EditRole)

            # Remove the newAddressTab, as we now have at least one
            # address in the model.
            self.removeTab(self.indexOf(self.newAddressTab))
            
            # The screenshot for the QT example shows nicely formatted
            # multiline cells, but the actual application doesn't behave
            # quite so nicely, at least on Ubuntu. Here we resize the newly
            # created row so that multiline addresses look reasonable.
            tableView = self.currentWidget()
            tableView.resizeRowToContents(ix.row())            

    def editEntry(self):
        """ Edit an entry in the addressbook. """
        tableView = self.currentWidget()
        proxyModel = tableView.model()
        selectionModel = tableView.selectionModel()

        # Get the name and address of the currently selected row.
        indexes = selectionModel.selectedRows()

        for index in indexes:
            row = proxyModel.mapToSource(index).row()
            ix = self.tableModel.index(row, 0, QModelIndex())
            name = self.tableModel.data(ix, Qt.DisplayRole)
            ix = self.tableModel.index(row, 1, QModelIndex())
            address = self.tableModel.data(ix, Qt.DisplayRole)

        # Open an addDialogWidget, and only allow the user to edit the address.
        addDialog = AddDialogWidget()
        addDialog.setWindowTitle("Edit a Contact")

        addDialog.nameText.setReadOnly(True)
        addDialog.nameText.setText(name)
        addDialog.addressText.setText(address)

        # If the address is different, add it to the model.
        if addDialog.exec_():
            newAddress = addDialog.address
            if newAddress != address:
                ix = self.tableModel.index(row, 1, QModelIndex())
                self.tableModel.setData(ix, newAddress, Qt.EditRole)

    def removeEntry(self):
        """ Remove an entry from the addressbook. """
        tableView = self.currentWidget()
        proxyModel = tableView.model()
        selectionModel = tableView.selectionModel()

        # Just like editEntry, but this time remove the selected row.
        indexes = selectionModel.selectedRows()

        for index in indexes:
            row = proxyModel.mapToSource(index).row()
            self.tableModel.removeRows(row)

        # If we've removed the last address in the model, display the 
        # newAddressTab
        if self.tableModel.rowCount() == 0:
            self.insertTab(0, self.newAddressTab, "Address Book")

    def setupTabs(self):
        """ Setup the various tabs in the AddressWidget. """
        groups = ["ABC", "DEF", "GHI", "JKL", "MNO", "PQR", "STU", "VW", "XYZ"]

        for group in groups:
            proxyModel = QSortFilterProxyModel(self)
            proxyModel.setSourceModel(self.tableModel)
            proxyModel.setDynamicSortFilter(True)

            tableView = QTableView()
            tableView.setModel(proxyModel)
            tableView.setSortingEnabled(True)
            tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
            tableView.horizontalHeader().setStretchLastSection(True)
            tableView.verticalHeader().hide()
            tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tableView.setSelectionMode(QAbstractItemView.SingleSelection)

            # This here be the magic: we use the group name (e.g. "ABC") to
            # build the regex for the QSortFilterProxyModel for the group's
            # tab. The regex will end up looking like "^[ABC].*", only 
            # allowing this tab to display items where the name starts with 
            # "A", "B", or "C". Notice that we set it to be case-insensitive.
            reFilter = "^[%s].*" % group

            proxyModel.setFilterRegExp(QRegExp(reFilter, Qt.CaseInsensitive))
            proxyModel.setFilterKeyColumn(0) # Filter on the "name" column
            proxyModel.sort(0, Qt.AscendingOrder)

            tableView.selectionModel().selectionChanged.connect(self.selectionChanged)

            self.addTab(tableView, group)

    # Note: the QT example uses a QDataStream for the saving and loading.
    # Here we're using a python dictionary to store the addresses, which
    # can't be streamed using QDataStream, so we just use cpickle for this
    # example.
    def readFromFile(self, filename):
        """ Read contacts in from a file. """
        try:
            f = open(filename, "rb")
            addresses = pickle.load(f)
        except IOError:
            QMessageBox.information(self, "Unable to open file: %s" % filename)
        finally:
            f.close()

        if len(addresses) == 0:
            QMessageBox.information(self, "No contacts in file: %s" % filename)
        else:
            for address in addresses:
                self.addEntry(address["name"], address["address"])        

    def writeToFile(self, filename):
        """ Save all contacts in the model to a file. """
        try:
            f = open(filename, "wb")
            pickle.dump(self.tableModel.addresses, f)

        except IOError:
            QMessageBox.information(self, "Unable to open file: %s" % filename)
        finally:
            f.close()       


if __name__ == "__main__":
    import sys
    from PySide.QtGui import QApplication

    app = QApplication(sys.argv)
    addressWidget = AddressWidget()
    addressWidget.show()
    sys.exit(app.exec_())
