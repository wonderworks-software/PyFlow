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
    model.setTable("person")

    model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    model.select()

    model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
    model.setHeaderData(1, QtCore.Qt.Horizontal, "First name")
    model.setHeaderData(2, QtCore.Qt.Horizontal, "Last name")


def createView(title, model):
    view = QtGui.QTableView()
    view.setModel(model)
    view.setWindowTitle(title)
    return view


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    if not connection.createConnection():
        sys.exit(1)

    model = QtSql.QSqlTableModel()

    initializeModel(model)

    view1 = createView("Table Model (View 1)", model)
    view2 = createView("Table Model (View 2)", model)

    view1.show()
    view2.move(view1.x() + view1.width() + 20, view1.y())
    view2.show()

    sys.exit(app.exec_())
