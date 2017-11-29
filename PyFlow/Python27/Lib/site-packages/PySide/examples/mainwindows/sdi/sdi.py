#!/usr/bin/env python

############################################################################
# 
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
# 
#  This file is part of the example classes of the Qt Toolkit.
# 
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
# 
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
# 
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
# 
############################################################################

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui

import sdi_rc


class MainWindow(QtGui.QMainWindow):
    sequenceNumber = 1
    windowList = []

    def __init__(self, fileName=None):
        super(MainWindow, self).__init__()

        self.init()
        if fileName:
            self.loadFile(fileName)
        else:
            self.setCurrentFile('')

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.move(self.x() + 40, self.y() + 40)
        other.show()

    def open(self):
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMainWindow(fileName)
            if existing:
                existing.show()
                existing.raise_()
                existing.activateWindow()
                return

            if self.isUntitled and self.textEdit.document().isEmpty() and not self.isWindowModified():
                self.loadFile(fileName)
            else:
                other = MainWindow(fileName)
                if other.isUntitled:
                    del other
                    return

                MainWindow.windowList.append(other)
                other.move(self.x() + 40, self.y() + 40)
                other.show()

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def about(self):
        QtGui.QMessageBox.about(self, "About SDI",
                "The <b>SDI</b> example demonstrates how to write single "
                "document interface applications using Qt.")

    def documentWasModified(self):
        self.setWindowModified(True)

    def init(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.document().contentsChanged.connect(self.documentWasModified)

    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), "&New",
                self, shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(':/images/open.png'),
                "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                "&Save", self, shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction("Save &As...", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.closeAct = QtGui.QAction("&Close", self, shortcut="Ctrl+W",
                statusTip="Close this window", triggered=self.close)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QtGui.qApp.closeAllWindows)

        self.cutAct = QtGui.QAction(QtGui.QIcon(':/images/cut.png'), "Cu&t",
                self, enabled=False, shortcut=QtGui.QKeySequence.Cut,
                statusTip="Cut the current selection's contents to the clipboard",
                triggered=self.textEdit.cut)

        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
                "&Copy", self, enabled=False, shortcut=QtGui.QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.textEdit.copy)

        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
                "&Paste", self, shortcut=QtGui.QKeySequence.Paste,
                statusTip="Paste the clipboard's contents into the current selection",
                triggered=self.textEdit.paste)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

        self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QtCore.QSettings('Trolltech', 'SDI Example')
        pos = settings.value('pos', QtCore.QPoint(200, 200))
        size = settings.value('size', QtCore.QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QtCore.QSettings('Trolltech', 'SDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QtGui.QMessageBox.warning(self, "SDI",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                    QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.save()
            elif ret == QtGui.QMessageBox.Cancel:
                return False
        return True

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "SDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        instr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        self.textEdit.setPlainText(instr.readAll())
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "SDI",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.isUntitled = not fileName
        if self.isUntitled:
            self.curFile = "document%d.txt" % MainWindow.sequenceNumber
            MainWindow.sequenceNumber += 1
        else:
            self.curFile = QtCore.QFileInfo(fileName).canonicalFilePath()

        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        self.setWindowTitle("%s[*] - SDI" % self.strippedName(self.curFile))

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()

    def findMainWindow(self, fileName):
        canonicalFilePath = QtCore.QFileInfo(fileName).canonicalFilePath()

        for widget in QtGui.qApp.topLevelWidgets():
            if isinstance(widget, MainWindow) and widget.curFile == canonicalFilePath:
                return widget

        return None


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
