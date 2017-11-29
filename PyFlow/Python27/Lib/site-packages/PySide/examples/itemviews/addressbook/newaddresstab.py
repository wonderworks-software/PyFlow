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

from PySide.QtCore import (Qt, Signal)
from PySide.QtGui import (QWidget, QLabel, QPushButton, QVBoxLayout)

from adddialogwidget import AddDialogWidget

class NewAddressTab(QWidget):
    """ An extra tab that prompts the user to add new contacts.
        To be displayed only when there are no contacts in the model.
    """

    sendDetails = Signal(str, str)

    def __init__(self, parent=None):
        super(NewAddressTab, self).__init__(parent)

        descriptionLabel = QLabel("There are no contacts in your address book."
                                   "\nClick Add to add new contacts.")

        addButton = QPushButton("Add")

        layout = QVBoxLayout()
        layout.addWidget(descriptionLabel)
        layout.addWidget(addButton, 0, Qt.AlignCenter)

        self.setLayout(layout)

        addButton.clicked.connect(self.addEntry)

    def addEntry(self):
        addDialog = AddDialogWidget()

        if addDialog.exec_():
            name = addDialog.name
            address = addDialog.address
            self.sendDetails.emit(name, address)


if __name__ == "__main__":

    def printAddress(name, address):
        print("Name:" + name)
        print("Address:" + address)

    import sys
    from PySide.QtGui import QApplication
    
    app = QApplication(sys.argv)
    newAddressTab = NewAddressTab()
    newAddressTab.sendDetails.connect(printAddress)
    newAddressTab.show()
    sys.exit(app.exec_())
