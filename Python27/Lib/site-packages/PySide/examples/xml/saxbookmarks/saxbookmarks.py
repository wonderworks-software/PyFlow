#!/usr/bin/python

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

from PySide import QtCore, QtGui, QtXml


class XbelGenerator(object):
    def __init__(self, treeWidget):
        self.treeWidget = treeWidget
        self.out = QtCore.QTextStream()

    def write(self, device):
        self.out.setDevice(device)
        self.out.setCodec('UTF-8')
        self.out << '<?xml version="1.0" encoding="UTF-8"?>\n' \
                 << '<!DOCTYPE xbel>\n' \
                 << '<xbel version="1.0">\n'

        for i in range(self.treeWidget.topLevelItemCount()):
            self.generateItem(self.treeWidget.topLevelItem(i), 1)

        self.out << '</xbel>\n'
        return True

    def indent(self, depth):
        IndentSize = 4

        return IndentSize * depth * ' '

    def escapedText(self, txt):
        result = txt
        result.replace('&', '&amp;')
        result.replace('<', '&lt;')
        result.replace('>', '&gt;')
        return result

    def escapedAttribute(self, txt):
        result = self.escapedText(txt)
        result.replace('"', '&quot;')
        return '"' + result + '"'

    def generateItem(self, item, depth):
        tagName = item.data(0, QtCore.Qt.UserRole)
        if tagName == 'folder':
            folded = (not self.treeWidget.isItemExpanded(item))
            self.out << self.indent(depth) << '<folder folded="'
            if folded:
                self.out << 'yes'
            else:
                self.out << 'no'
            self.out << '">\n' \
                     << self.indent(depth + 1) << '<title>' \
                     << self.escapedText(item.text(0)) \
                     << '</title>\n'

            for i in range(item.childCount()):
                self.generateItem(item.child(i), depth + 1)

            self.out << self.indent(depth) << '</folder>\n'
        elif tagName == 'bookmark':
            self.out << self.indent(depth) << '<bookmark'
            if item.text(1):
                self.out << ' href=' \
                         << self.escapedAttribute(item.text(1))
            self.out << '>\n' \
                     << self.indent(depth + 1) << '<title>' \
                     << self.escapedText(item.text(0)) \
                     << '</title>\n' \
                     << self.indent(depth) << '</bookmark>\n'
        elif tagName == 'separator':
            self.out << self.indent(depth) << '<separator/>\n'


class XbelHandler(QtXml.QXmlDefaultHandler):
    def __init__(self, treeWidget):
        super(XbelHandler, self).__init__()

        self.treeWidget = treeWidget
        self.folderIcon = QtGui.QIcon()
        self.bookmarkIcon = QtGui.QIcon()
        self.currentText = ''
        self.errorStr = ''

        self.item = None
        self.metXbelTag = False

        style = self.treeWidget.style()

        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirClosedIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_DirOpenIcon),
                QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.bookmarkIcon.addPixmap(style.standardPixmap(QtGui.QStyle.SP_FileIcon))

    def startElement(self, namespaceURI, localName, qName, attributes):
        if not self.metXbelTag and qName != 'xbel':
            self.errorStr = "The file is not an XBEL file."
            return False

        if qName == 'xbel':
            version = attributes.value('version')
            if version and version != '1.0':
                self.errorStr = "The File is not an XBEL version 1.0 file."
                return False
            self.metXbelTag = True
        elif qName == 'folder':
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
            self.item.setIcon(0, self.folderIcon)
            self.item.setText(0, "Folder")
            folded = (attributes.value('folded') != 'no')
            self.treeWidget.setItemExpanded(self.item, (not folded))
        elif qName == 'bookmark':
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() | QtCore.Qt.ItemIsEditable)
            self.item.setIcon(0, self.bookmarkIcon)
            self.item.setText(0, "Unkown title")
            self.item.setText(1, attributes.value('href'))
        elif qName == 'separator':
            self.item = self.createChildItem(qName)
            self.item.setFlags(self.item.flags() & ~QtCore.Qt.ItemIsSelectable)
            self.item.setText(0, 30 * "\xb7")

        self.currentText = ''
        return True

    def endElement(self, namespaceURI, localName, qName):
        if qName == 'title':
            if self.item:
                self.item.setText(0, self.currentText)
        elif qName in ('folder', 'bookmark', 'separator'):
            self.item = self.item.parent()

        return True

    def characters(self, txt):
        self.currentText += txt
        return True

    def fatalError(self, exception):
        QtGui.QMessageBox.information(self.treeWidget.window(),
                "SAX Bookmarks",
                "Parse error at line %d, column %d:\n%s" % (exception.lineNumber(), exception.columnNumber(), exception.message()))
        return False

    def errorString(self):
        return self.errorStr

    def createChildItem(self, tagName):
        if self.item:
            childItem = QtGui.QTreeWidgetItem(self.item)
        else:
            childItem = QtGui.QTreeWidgetItem(self.treeWidget)

        childItem.setData(0, QtCore.Qt.UserRole, tagName)
        return childItem


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.header().setResizeMode(QtGui.QHeaderView.Stretch)
        self.treeWidget.setHeaderLabels(("Title", "Location"))
        self.setCentralWidget(self.treeWidget)

        self.createActions()
        self.createMenus()

        self.statusBar().showMessage("Ready")

        self.setWindowTitle("SAX Bookmarks")
        self.resize(480, 320)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "Open Bookmark File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        self.treeWidget.clear()

        handler = XbelHandler(self.treeWidget)
        reader = QtXml.QXmlSimpleReader()
        reader.setContentHandler(handler)
        reader.setErrorHandler(handler)

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "SAX Bookmarks",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        xmlInputSource = QtXml.QXmlInputSource(file)
        if reader.parse(xmlInputSource):
            self.statusBar().showMessage("File loaded", 2000)

    def saveAs(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,
                "Save Bookmark File", QtCore.QDir.currentPath(),
                "XBEL Files (*.xbel *.xml)")[0]

        if not fileName:
            return

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "SAX Bookmarks",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

        generator = XbelGenerator(self.treeWidget)
        if generator.write(file):
            self.statusBar().showMessage("File saved", 2000)

    def about(self):
         QtGui.QMessageBox.about(self, "About SAX Bookmarks",
                "The <b>SAX Bookmarks</b> example demonstrates how to use "
                "Qt's SAX classes to read XML documents and how to generate "
                "XML by hand.")

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveAsAct = QtGui.QAction("&Save As...", self, shortcut="Ctrl+S",
                triggered=self.saveAs)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    mainWin.open()
    sys.exit(app.exec_())
