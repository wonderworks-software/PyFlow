#!/usr/bin/env python

############################################################################
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
############################################################################

from PySide import QtCore, QtGui, QtSql

import connection


class TableEditor(QtGui.QDialog):
    def __init__(self, tableName, parent=None):
        super(TableEditor, self).__init__(parent)

        self.model = QtSql.QSqlTableModel(self)
        self.model.setTable(tableName)
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()

        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")

        view = QtGui.QTableView()
        view.setModel(self.model)

        submitButton = QtGui.QPushButton("Submit")
        submitButton.setDefault(True)
        revertButton = QtGui.QPushButton("&Revert")
        quitButton = QtGui.QPushButton("Quit")

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Vertical)
        buttonBox.addButton(submitButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(revertButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(quitButton, QtGui.QDialogButtonBox.RejectRole)

        submitButton.clicked.connect(self.submit)
        revertButton.clicked.connect(self.model.revertAll)
        quitButton.clicked.connect(self.close)

        mainLayout = QtGui.QHBoxLayout()
        mainLayout.addWidget(view)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Cached Table")

    def submit(self):
        self.model.database().transaction()
        if self.model.submitAll():
            self.model.database().commit()
        else:
            self.model.database().rollback()
            QtGui.QMessageBox.warning(self, "Cached Table",
                        "The database reported an error: %s" % self.model.lastError().text())


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    editor = TableEditor('person')
    editor.show()
    sys.exit(editor.exec_())
