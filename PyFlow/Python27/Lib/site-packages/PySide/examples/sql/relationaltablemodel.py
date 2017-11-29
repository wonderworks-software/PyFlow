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


def initializeModel(model):
    model.setTable("employee")

    model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    model.setRelation(2, QtSql.QSqlRelation('city', 'id', 'name'))
    model.setRelation(3, QtSql.QSqlRelation('country', 'id', 'name'))

    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "Name")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "City")
    model.setHeaderData(3, QtCore.Qt.Horizontal, "Country")

    model.select()


def createView(title, model):
    view = QtGui.QTableView()
    view.setModel(model)
    view.setItemDelegate(QtSql.QSqlRelationalDelegate(view))
    view.setWindowTitle(title)

    return view


def createRelationalTables():
    query = QtSql.QSqlQuery()

    query.exec_("create table employee(id int, name varchar(20), city int, country int)")
    query.exec_("insert into employee values(1, 'Espen', 5000, 47)")
    query.exec_("insert into employee values(2, 'Harald', 80000, 49)")
    query.exec_("insert into employee values(3, 'Sam', 100, 41)")

    query.exec_("create table city(id int, name varchar(20))")
    query.exec_("insert into city values(100, 'San Jose')")
    query.exec_("insert into city values(5000, 'Oslo')")
    query.exec_("insert into city values(80000, 'Munich')")

    query.exec_("create table country(id int, name varchar(20))")
    query.exec_("insert into country values(41, 'USA')")
    query.exec_("insert into country values(47, 'Norway')")
    query.exec_("insert into country values(49, 'Germany')")


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    createRelationalTables()

    model = QtSql.QSqlRelationalTableModel()

    initializeModel(model)

    view = createView("Relational Table Model", model)

    view.show()

    sys.exit(app.exec_())
