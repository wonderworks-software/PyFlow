#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
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


from PySide import QtCore, QtGui


class SpinBoxDelegate(QtGui.QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QtGui.QSpinBox(parent)
        editor.setMinimum(0)
        editor.setMaximum(100)

        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, QtCore.Qt.EditRole)

        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    model = QtGui.QStandardItemModel(4, 2)
    tableView = QtGui.QTableView()
    tableView.setModel(model)

    delegate = SpinBoxDelegate()
    tableView.setItemDelegate(delegate)

    for row in range(4):
        for column in range(2):
            index = model.index(row, column, QtCore.QModelIndex())
            model.setData(index, (row + 1) * (column + 1))

    tableView.setWindowTitle("Spin Box Delegate")
    tableView.show()
    sys.exit(app.exec_())
