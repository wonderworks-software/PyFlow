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

# This is only needed for Python v2 but is harmless for Python v3.
from PySide import QtCore, QtGui, QtSql

import connection


class CustomSqlModel(QtSql.QSqlQueryModel):
    def data(self, index, role):
        value = super(CustomSqlModel, self).data(index, role)
        if value is not None and role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return '#%d' % value
            elif index.column() == 2:
                return value.upper()

        if role == QtCore.Qt.TextColorRole and index.column() == 1:
            return QtGui.QColor(QtCore.Qt.blue)

        return value


class EditableSqlModel(QtSql.QSqlQueryModel):
    def flags(self, index):
        flags = super(EditableSqlModel, self).flags(index)

        if index.column() in (1, 2):
            flags |= QtCore.Qt.ItemIsEditable

        return flags

    def setData(self, index, value, role):
        if index.column() not in (1, 2):
            return False

        primaryKeyIndex = self.index(index.row(), 0)
        id = self.data(primaryKeyIndex)

        self.clear()

        if index.column() == 1:
            ok = self.setFirstName(id, value)
        else:
            ok = self.setLastName(id, value)

        self.refresh()
        return ok

    def refresh(self):
        self.setQuery('select * from person')
        self.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
        self.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")

    def setFirstName(self, personId, firstName):
        query = QtSql.QSqlQuery()
        query.prepare('update person set firstname = ? where id = ?')
        query.addBindValue(firstName)
        query.addBindValue(personId)
        return query.exec_()

    def setLastName(self, personId, lastName):
        query = QtSql.QSqlQuery()
        query.prepare('update person set lastname = ? where id = ?')
        query.addBindValue(lastName)
        query.addBindValue(personId)
        return query.exec_()


def initializeModel(model):
    model.setQuery('select * from person')
    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")


offset = 0
views = []

def createView(title, model):
    global offset, views

    view = QtGui.QTableView()
    views.append(view)
    view.setModel(model)
    view.setWindowTitle(title)
    view.move(100 + offset, 100 + offset)
    offset += 20
    view.show()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    plainModel = QtSql.QSqlQueryModel()
    editableModel = EditableSqlModel()
    customModel = CustomSqlModel()

    initializeModel(plainModel)
    initializeModel(editableModel)
    initializeModel(customModel)

    createView("Plain Query Model", plainModel)
    createView("Editable Query Model", editableModel)
    createView("Custom Query Model", customModel)

    sys.exit(app.exec_())
