#!/usr/bin/env python

#############################################################################
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
#############################################################################

from PySide import QtCore, QtGui


class CharacterWidget(QtGui.QWidget):

    characterSelected = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(CharacterWidget, self).__init__(parent)

        self.displayFont = QtGui.QFont()
        self.squareSize = 24
        self.columns = 16
        self.lastKey = -1
        self.setMouseTracking(True)

    def updateFont(self, fontFamily):
        self.displayFont.setFamily(fontFamily)
        self.squareSize = max(24, QtGui.QFontMetrics(self.displayFont).xHeight() * 3)
        self.adjustSize()
        self.update()

    def updateSize(self, fontSize):
        fontSize = int(fontSize)
        self.displayFont.setPointSize(fontSize)
        self.squareSize = max(24, QtGui.QFontMetrics(self.displayFont).xHeight() * 3)
        self.adjustSize()
        self.update()

    def updateStyle(self, fontStyle):
        fontDatabase = QtGui.QFontDatabase()
        oldStrategy = self.displayFont.styleStrategy()
        self.displayFont = fontDatabase.font(self.displayFont.family(),
                fontStyle, self.displayFont.pointSize())
        self.displayFont.setStyleStrategy(oldStrategy)
        self.squareSize = max(24, QtGui.QFontMetrics(self.displayFont).xHeight() * 3)
        self.adjustSize()
        self.update()

    def updateFontMerging(self, enable):
        if enable:
            self.displayFont.setStyleStrategy(QtGui.QFont.PreferDefault)
        else:
            self.displayFont.setStyleStrategy(QtGui.QFont.NoFontMerging)
        self.adjustSize()
        self.update()

    def sizeHint(self):
        return QtCore.QSize(self.columns * self.squareSize,
                (65536 / self.columns) * self.squareSize)

    def mouseMoveEvent(self, event):
        widgetPosition = self.mapFromGlobal(event.globalPos())
        key = (widgetPosition.y() / self.squareSize) * self.columns + widgetPosition.x() / self.squareSize


        ch = unichr(key)
        text = '<p>Character: <span style="font-size: 24pt; font-family: %s">%s</span><p>Value: %s' % \
                (self.displayFont.family(), ch, hex(key))
        QtGui.QToolTip.showText(event.globalPos(), text, self)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastKey = (event.y() / self.squareSize) * self.columns + event.x() / self.squareSize
            c = unichr(self.lastKey)
            self.characterSelected.emit(c)
            #try:
                #c = chr(self.lastKey)
                #self.characterSelected.emit(c)
            #except:
                #pass
            self.update()
        else:
            super(CharacterWidget, self).mousePressEvent(event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)
        painter.setFont(self.displayFont)

        redrawRect = event.rect()
        beginRow = redrawRect.top() // self.squareSize
        endRow = redrawRect.bottom() // self.squareSize
        beginColumn = redrawRect.left() // self.squareSize
        endColumn = redrawRect.right() // self.squareSize

        painter.setPen(QtCore.Qt.gray)
        for row in range(beginRow, endRow + 1):
            for column in range(beginColumn, endColumn + 1):
                painter.drawRect(column * self.squareSize,
                        row * self.squareSize, self.squareSize,
                        self.squareSize)

        fontMetrics = QtGui.QFontMetrics(self.displayFont)
        painter.setPen(QtCore.Qt.black)
        for row in range(beginRow, endRow + 1):
            for column in range(beginColumn, endColumn + 1):
                key = row * self.columns + column
                painter.setClipRect(column * self.squareSize,
                        row * self.squareSize, self.squareSize,
                        self.squareSize)

                if key == self.lastKey:
                    painter.fillRect(column * self.squareSize + 1,
                            row * self.squareSize + 1, self.squareSize,
                            self.squareSize, QtCore.Qt.red)

                ch = unichr(key)

                x = column * self.squareSize + (self.squareSize / 2) - fontMetrics.width(ch) / 2
                y = row * self.squareSize + 4 + fontMetrics.ascent()
                painter.drawText(x, y, ch)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        centralWidget = QtGui.QWidget()

        fontLabel = QtGui.QLabel("Font:")
        self.fontCombo = QtGui.QFontComboBox()
        sizeLabel = QtGui.QLabel("Size:")
        self.sizeCombo = QtGui.QComboBox()
        styleLabel = QtGui.QLabel("Style:")
        self.styleCombo = QtGui.QComboBox()
        fontMergingLabel = QtGui.QLabel("Automatic Font Merging:")
        self.fontMerging = QtGui.QCheckBox()
        self.fontMerging.setChecked(True)

        self.scrollArea = QtGui.QScrollArea()
        self.characterWidget = CharacterWidget()
        self.scrollArea.setWidget(self.characterWidget)

        self.findStyles(self.fontCombo.currentFont())
        self.findSizes(self.fontCombo.currentFont())

        self.lineEdit = QtGui.QLineEdit()
        clipboardButton = QtGui.QPushButton("&To clipboard")

        self.clipboard = QtGui.QApplication.clipboard()

        self.fontCombo.currentFontChanged.connect(self.findStyles)
        self.fontCombo.currentFontChanged.connect(self.findSizes)
        self.fontCombo.activated[str].connect(self.characterWidget.updateFont)
        self.styleCombo.activated[str].connect(self.characterWidget.updateStyle)
        self.sizeCombo.currentIndexChanged[str].connect(self.characterWidget.updateSize)
        self.characterWidget.characterSelected.connect(self.insertCharacter)
        clipboardButton.clicked.connect(self.updateClipboard)

        controlsLayout = QtGui.QHBoxLayout()
        controlsLayout.addWidget(fontLabel)
        controlsLayout.addWidget(self.fontCombo, 1)
        controlsLayout.addWidget(sizeLabel)
        controlsLayout.addWidget(self.sizeCombo, 1)
        controlsLayout.addWidget(styleLabel)
        controlsLayout.addWidget(self.styleCombo, 1)
        controlsLayout.addWidget(fontMergingLabel)
        controlsLayout.addWidget(self.fontMerging, 1)
        controlsLayout.addStretch(1)

        lineLayout = QtGui.QHBoxLayout()
        lineLayout.addWidget(self.lineEdit, 1)
        lineLayout.addSpacing(12)
        lineLayout.addWidget(clipboardButton)

        centralLayout = QtGui.QVBoxLayout()
        centralLayout.addLayout(controlsLayout)
        centralLayout.addWidget(self.scrollArea, 1)
        centralLayout.addSpacing(4)
        centralLayout.addLayout(lineLayout)
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)
        self.setWindowTitle("Character Map")

    def findStyles(self, font):
        fontDatabase = QtGui.QFontDatabase()
        currentItem = self.styleCombo.currentText()
        self.styleCombo.clear()

        for style in fontDatabase.styles(font.family()):
            self.styleCombo.addItem(style)

        styleIndex = self.styleCombo.findText(currentItem)
        if styleIndex == -1:
            self.styleCombo.setCurrentIndex(0)
        else:
            self.styleCombo.setCurrentIndex(styleIndex)

    def findSizes(self, font):
        fontDatabase = QtGui.QFontDatabase()
        currentSize = self.sizeCombo.currentText()
        self.sizeCombo.blockSignals(True)
        self.sizeCombo.clear()

        if fontDatabase.isSmoothlyScalable(font.family(), fontDatabase.styleString(font)):
            for size in QtGui.QFontDatabase.standardSizes():
                self.sizeCombo.addItem(str(size))
                self.sizeCombo.setEditable(True)
        else:
            for size in fontDatabase.smoothSizes(font.family(), fontDatabase.styleString(font)):
                self.sizeCombo.addItem(str(size))
                self.sizeCombo.setEditable(False)

        self.sizeCombo.blockSignals(False)

        sizeIndex = self.sizeCombo.findText(currentSize)
        if sizeIndex == -1:
            self.sizeCombo.setCurrentIndex(max(0, self.sizeCombo.count() / 3))
        else:
            self.sizeCombo.setCurrentIndex(sizeIndex)

    def insertCharacter(self, character):
        self.lineEdit.insert(character)

    def updateClipboard(self):
        self.clipboard.setText(self.lineEdit.text(), QtGui.QClipboard.Clipboard)
        self.clipboard.setText(self.lineEdit.text(), QtGui.QClipboard.Selection)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
