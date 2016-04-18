#!/usr/bin/env python

"""PySide port of the richtext/syntaxhighlighter example from Qt v4.x"""

import sys
import re
from PySide import QtCore, QtGui

import syntaxhighlighter_rc


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        
        self.highlighter = Highlighter()
        
        self.setupFileMenu()
        self.setupEditor()
    
        self.setCentralWidget(self.editor)
        self.setWindowTitle(self.tr("Syntax Highlighter"))
    
    def newFile(self):
        self.editor.clear()
    
    def openFile(self, path=""):
        fileName = path
    
        if fileName=="":
            fileName,_ = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open File"), "",
                                                         "qmake Files (*.pro *.prf *.pri)")
    
        if fileName!="":
            inFile = QtCore.QFile(fileName)
            if inFile.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                self.editor.setPlainText(unicode(inFile.readAll()))
    
    def setupEditor(self):
        variableFormat = QtGui.QTextCharFormat()
        variableFormat.setFontWeight(QtGui.QFont.Bold)
        variableFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\\b[A-Z_]+\\b", variableFormat)
    
        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setBackground(QtGui.QColor("#77ff77"))
        self.highlighter.addMapping("#[^\n]*", singleLineCommentFormat)
    
        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setBackground(QtCore.Qt.cyan)
        quotationFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\".*\"", quotationFormat)
    
        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QtCore.Qt.blue)
        self.highlighter.addMapping("\\b[a-z0-9_]+\\(.*\\)", functionFormat)
    
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(10)
    
        self.editor = QtGui.QTextEdit()
        self.editor.setFont(font)
        self.highlighter.addToDocument(self.editor.document())
    
    def setupFileMenu(self):
        fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.menuBar().addMenu(fileMenu)
        
        newFileAct = QtGui.QAction(self.tr("&New..."), self)
        newFileAct.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+N", "File|New")))
        self.connect(newFileAct, QtCore.SIGNAL("triggered()"), self.newFile)
        fileMenu.addAction(newFileAct)
        
        openFileAct = QtGui.QAction(self.tr("&Open..."), self)
        openFileAct.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+O", "File|Open")))
        self.connect(openFileAct, QtCore.SIGNAL("triggered()"), self.openFile)
        fileMenu.addAction(openFileAct)
    
        fileMenu.addAction(self.tr("E&xit"), QtGui.qApp, QtCore.SLOT("quit()"),
                           QtGui.QKeySequence(self.tr("Ctrl+Q", "File|Exit")))
                            

class Highlighter(QtCore.QObject):
    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent)
        
        self.mappings = {}
        
    def addToDocument(self, doc):
        self.connect(doc, QtCore.SIGNAL("contentsChange(int, int, int)"), self.highlight)
    
    def addMapping(self, pattern, format):
        self.mappings[pattern] = format
    
    def highlight(self, position, removed, added):
        doc = self.sender()
    
        block = doc.findBlock(position)
        if not block.isValid():
            return
    
        if added > removed:
            endBlock = doc.findBlock(position + added)
        else:
            endBlock = block
    
        while block.isValid() and not (endBlock < block):
            self.highlightBlock(block)
            block = block.next()
    
    def highlightBlock(self, block):
        layout = block.layout()
        text = block.text()
    
        overrides = []

        for pattern in self.mappings:
            for m in re.finditer(pattern,text):
                range = QtGui.QTextLayout.FormatRange()
                s,e = m.span()
                range.start = s
                range.length = e-s
                range.format = self.mappings[pattern]
                overrides.append(range)
    
        layout.setAdditionalFormats(overrides)
        block.document().markContentsDirty(block.position(), block.length())
        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.resize(640, 512)
    window.show()
    window.openFile(":/examples/example")
    sys.exit(app.exec_())
