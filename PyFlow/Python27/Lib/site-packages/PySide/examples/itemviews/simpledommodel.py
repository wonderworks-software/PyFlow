#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

from PySide import QtCore, QtGui, QtXml


class DomItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        # Record the item's location within its parent.
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}

    def node(self):
        return self.domNode

    def parent(self):
        return self.parentItem

    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]

        if i >= 0 and i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = DomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem

        return None

    def row(self):
        return self.rowNumber


class DomModel(QtCore.QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(DomModel, self).__init__(parent)

        self.domDocument = document

        self.rootItem = DomItem(self.domDocument, 0)

    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        node = item.node()
        attributes = []
        attributeMap = node.attributes()

        if index.column() == 0:
            return node.nodeName()
        
        elif index.column() == 1:
            for i in range(0, attributeMap.count()):
                attribute = attributeMap.item(i)
                attributes.append(attribute.nodeName() + '="' +
                                  attribute.nodeValue() + '"')

            return " ".join(attributes)

        if index.column() == 2:
            value = node.nodeValue()
            if value is None:
                return ''

            return ' '.join(node.nodeValue().split('\n'))

        return None

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"

            if section == 1:
                return "Attributes"

            if section == 2:
                return "Value"

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()

        childItem = child.internalPointer()
        parentItem = childItem.parent()

        if not parentItem or parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.node().childNodes().count()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction("&Open...", self.openFile, "Ctrl+O")
        self.fileMenu.addAction("E&xit", self.close, "Ctrl+Q")

        self.xmlPath = ""
        self.model = DomModel(QtXml.QDomDocument(), self)
        self.view = QtGui.QTreeView(self)
        self.view.setModel(self.model)

        self.setCentralWidget(self.view)
        self.setWindowTitle("Simple DOM Model")

    def openFile(self):
        filePath,_ = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                self.xmlPath, "XML files (*.xml);;HTML files (*.html);;"
                "SVG files (*.svg);;User Interface files (*.ui)")

        if filePath:
            f = QtCore.QFile(filePath)
            if f.open(QtCore.QIODevice.ReadOnly):
                document = QtXml.QDomDocument()
                if document.setContent(f):
                    newModel = DomModel(document, self)
                    self.view.setModel(newModel)
                    self.model = newModel
                    self.xmlPath = filePath

                f.close()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 480)
    window.show()
    sys.exit(app.exec_())
