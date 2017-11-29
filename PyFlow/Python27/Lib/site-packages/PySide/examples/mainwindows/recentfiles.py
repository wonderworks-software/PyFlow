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
#sip.setapi('QString', 2)
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    MaxRecentFiles = 5
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.statusBar()

        self.setWindowTitle("Recent Files")
        self.resize(400, 300)

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def save(self):
        if self.curFile:
            self.saveFile(self.curFile)
        else:
            self.saveAs()

    def saveAs(self):
        fileName, filtr = QtGui.QFileDialog.getSaveFileName(self)
        if fileName:
            self.saveFile(fileName)

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        QtGui.QMessageBox.about(self, "About Recent Files",
                "The <b>Recent Files</b> example demonstrates how to provide "
                "a recently used file menu in a Qt application.")

    def createActions(self):
        self.newAct = QtGui.QAction("&New", self,
                shortcut=QtGui.QKeySequence.New,
                statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction("&Open...", self,
                shortcut=QtGui.QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction("&Save", self,
                shortcut=QtGui.QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction("Save &As...", self,
                shortcut=QtGui.QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                    QtGui.QAction(self, visible=False,
                            triggered=self.openRecentFile))

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application",
                triggered=QtGui.qApp.closeAllWindows)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def loadFile(self, fileName):
        file = QtCore.QFile(fileName)
        if not file.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Recent Files",
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
        if not file.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
            QtGui.QMessageBox.warning(self, "Recent Files",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return

        outstr = QtCore.QTextStream(file)
        QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QtGui.QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        if self.curFile:
            self.setWindowTitle("%s - Recent Files" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QtCore.QSettings('Trolltech', 'Recent Files Example')
        files = list(settings.value('recentFileList', []))

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QtGui.QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QtCore.QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList')

        files_no = 0
        if files:
            files_no = len(files)

        numRecentFiles = min(files_no, MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QtCore.QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
