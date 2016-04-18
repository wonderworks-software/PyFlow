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

from PySide.QtGui import (QMainWindow, QAction, QFileDialog, QApplication)

from addresswidget import AddressWidget


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.addressWidget = AddressWidget()
        self.setCentralWidget(self.addressWidget)
        self.createMenus()
        self.setWindowTitle("Address Book")

    def createMenus(self):
        # Create the main menuBar menu items
        fileMenu = self.menuBar().addMenu("&File")
        toolMenu = self.menuBar().addMenu("&Tools")

        # Populate the File menu
        openAction = self.createAction("&Open...", fileMenu, self.openFile)
        saveAction = self.createAction("&Save As...", fileMenu, self.saveFile)
        fileMenu.addSeparator()
        exitAction = self.createAction("E&xit", fileMenu, self.close)

        # Populate the Tools menu
        addAction = self.createAction("&Add Entry...", toolMenu, self.addressWidget.addEntry)
        self.editAction = self.createAction("&Edit Entry...", toolMenu, self.addressWidget.editEntry)
        toolMenu.addSeparator()
        self.removeAction = self.createAction("&Remove Entry", toolMenu, self.addressWidget.removeEntry)
        
        # Disable the edit and remove menu items initally, as there are
        # no items yet.
        self.editAction.setEnabled(False)
        self.removeAction.setEnabled(False)

        # Wire up the updateActions slot
        self.addressWidget.selectionChanged.connect(self.updateActions)

    def createAction(self, text, menu, slot):
        """ Helper function to save typing when populating menus 
            with action. 
        """
        action = QAction(text, self)
        menu.addAction(action)
        action.triggered.connect(slot)
        return action

    # Quick  gotcha: 
    # 
    # QFiledialog.getOpenFilename and QFileDialog.get.SaveFileName don't 
    # behave in PySide as they do in QT, where they return a QString
    # containing the filename.
    # 
    # In PySide (and, I believe, PyQT), these functions return a tuple:
    # (filename, filter)
    #
    # http://www.pyside.org/docs/pyside/PySide/QtGui/QFileDialog.html

    def openFile(self):
        filename, _ = QFileDialog.getOpenFileName(self)
        if filename:
            self.addressWidget.readFromFile(filename)

    def saveFile(self):
        filename, _ = QFileDialog.getSaveFileName(self)
        if filename:
            self.addressWidget.writeToFile(filename)

    def updateActions(self, selection):
        """ Only allow the user to remove or edit an item if an item
            is actually selected.
        """
        indexes = selection.indexes()

        if len(indexes) > 0:
            self.removeAction.setEnabled(True)
            self.editAction.setEnabled(True)
        else:
            self.removeAction.setEnabled(False)
            self.editAction.setEnabled(False)


if __name__ == "__main__":
    """ Run the application. """
    import sys
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
