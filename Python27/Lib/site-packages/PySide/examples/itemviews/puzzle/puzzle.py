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

import random
from PySide import QtCore, QtGui

import puzzle_rc


class PuzzleWidget(QtGui.QWidget):

    puzzleCompleted = QtCore.Signal()

    def __init__(self, parent=None):
        super(PuzzleWidget, self).__init__(parent)

        self.piecePixmaps = []
        self.pieceRects = []
        self.pieceLocations = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        self.pieceLocations = []
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QtCore.QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.unite(self.targetSquare(event.pos()))

        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-puzzle-piece') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-puzzle-piece')
            stream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QtGui.QPixmap()
            location = QtCore.QPoint()
            stream >> pixmap >> location

            self.pieceLocations.append(location)
            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QtCore.QRect()
            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

            if location == QtCore.QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1
                if self.inPlace == 25:
                    self.puzzleCompleted.emit()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            return self.pieceRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos())
        found = self.findPiece(square)

        if found == -1:
            return

        location = self.pieceLocations[found]
        pixmap = self.piecePixmaps[found]

        del self.pieceLocations[found]
        del self.piecePixmaps[found]
        del self.pieceRects[found]

        if location == QtCore.QPoint(square.x() + 80, square.y() + 80):
            self.inPlace -= 1

        self.update(square)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)

        dataStream << pixmap << location

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-puzzle-piece', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.start(QtCore.Qt.MoveAction) == 0:
            self.pieceLocations.insert(found, location)
            self.piecePixmaps.insert(found, pixmap)
            self.pieceRects.insert(found, square)
            self.update(self.targetSquare(event.pos()))

            if location == QtCore.QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)

        if self.highlightedRect.isValid():
            painter.setBrush(QtGui.QColor("#ffcccc"))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for i, pieceRect in enumerate(self.pieceRects):
            painter.drawPixmap(pieceRect, self.piecePixmaps[i])

        painter.end()

    def targetSquare(self, position):
        return QtCore.QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80)


class PiecesModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(PiecesModel, self).__init__(parent)

        self.locations = []
        self.pixmaps = []

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(self.pixmaps[index.row()].scaled(
                    60, 60, QtCore.Qt.KeepAspectRatio,
                    QtCore.Qt.SmoothTransformation))

        if role == QtCore.Qt.UserRole:
            return self.pixmaps[index.row()]

        if role == QtCore.Qt.UserRole + 1:
            return self.locations[index.row()]

        return None

    def addPiece(self, pixmap, location):
        if random.random() < 0.5:
            row = 0
        else:
            row = len(self.pixmaps)

        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.pixmaps.insert(row, pixmap)
        self.locations.insert(row, location)
        self.endInsertRows()

    def flags(self,index):
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsDragEnabled)

        return QtCore.Qt.ItemIsDropEnabled

    def removeRows(self,row, count, parent):
        if parent.isValid():
            return False

        if row >= len(self.pixmaps) or row + count <= 0:
            return False

        beginRow = max(0, row)
        endRow = min(row + count - 1, len(self.pixmaps) - 1)

        self.beginRemoveRows(parent, beginRow, endRow)

        del self.pixmaps[beginRow:endRow + 1]
        del self.locations[beginRow:endRow + 1]

        self.endRemoveRows()
        return True

    def mimeTypes(self):
        return ['image/x-puzzle-piece']

    def mimeData(self, indexes):
        mimeData = QtCore.QMimeData()
        encodedData = QtCore.QByteArray()

        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                pixmap = QtGui.QPixmap(self.data(index, QtCore.Qt.UserRole))
                location = self.data(index, QtCore.Qt.UserRole + 1)
                stream << pixmap << location

        mimeData.setData('image/x-puzzle-piece', encodedData)
        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat('image/x-puzzle-piece'):
            return False

        if action == QtCore.Qt.IgnoreAction:
            return True

        if column > 0:
            return False

        if not parent.isValid():
            if row < 0:
                endRow = len(self.pixmaps)
            else:
                endRow = min(row, len(self.pixmaps))
        else:
            endRow = parent.row()

        encodedData = data.data('image/x-puzzle-piece')
        stream = QtCore.QDataStream(encodedData, QtCore.QIODevice.ReadOnly)

        while not stream.atEnd():
            pixmap = QtGui.QPixmap()
            location = QtGui.QPoint()
            stream >> pixmap >> location

            self.beginInsertRows(QtCore.QModelIndex(), endRow, endRow)
            self.pixmaps.insert(endRow, pixmap)
            self.locations.insert(endRow, location)
            self.endInsertRows()

            endRow += 1

        return True

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.pixmaps)

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def addPieces(self, pixmap):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 24)
        self.pixmaps = []
        self.locations = []
        self.endRemoveRows()

        for y in range(5):
            for x in range(5):
                pieceImage = pixmap.copy(x*80, y*80, 80, 80)
                self.addPiece(pieceImage, QtCore.QPoint(x, y))


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.puzzleImage = QtGui.QPixmap()

        self.setupMenus()
        self.setupWidgets()

        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                QtGui.QSizePolicy.Fixed))
        self.setWindowTitle("Puzzle")

    def openImage(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self, "Open Image", '',
                    "Image Files (*.png *.jpg *.bmp)")

        if path:
            newImage = QtGui.QPixmap()
            if not newImage.load(path):
                QtGui.QMessageBox.warning(self, "Open Image",
                        "The image file could not be loaded.",
                        QtGui.QMessageBox.Cancel)
                return

            self.puzzleImage = newImage
            self.setupPuzzle()

    def setCompleted(self):
        QtGui.QMessageBox.information(self, "Puzzle Completed",
                "Congratulations! You have completed the puzzle!\nClick OK "
                "to start again.",
                QtGui.QMessageBox.Ok)

        self.setupPuzzle()

    def setupPuzzle(self):
        size = min(self.puzzleImage.width(), self.puzzleImage.height())
        self.puzzleImage = self.puzzleImage.copy((self.puzzleImage.width()-size)/2,
                (self.puzzleImage.height() - size)/2, size, size).scaled(400,
                        400, QtCore.Qt.IgnoreAspectRatio,
                        QtCore.Qt.SmoothTransformation)

        random.seed(QtGui.QCursor.pos().x() ^ QtGui.QCursor.pos().y())

        self.model.addPieces(self.puzzleImage)
        self.puzzleWidget.clear()

    def setupMenus(self):
        fileMenu = self.menuBar().addMenu("&File")

        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        exitAction = fileMenu.addAction("E&xit")
        exitAction.setShortcut("Ctrl+Q")

        gameMenu = self.menuBar().addMenu("&Game")

        restartAction = gameMenu.addAction("&Restart")

        openAction.triggered.connect(self.openImage)
        exitAction.triggered.connect(QtGui.qApp.quit)
        restartAction.triggered.connect(self.setupPuzzle)

    def setupWidgets(self):
        frame = QtGui.QFrame()
        frameLayout = QtGui.QHBoxLayout(frame)

        self.piecesList = QtGui.QListView()
        self.piecesList.setDragEnabled(True)
        self.piecesList.setViewMode(QtGui.QListView.IconMode)
        self.piecesList.setIconSize(QtCore.QSize(60,60))
        self.piecesList.setGridSize(QtCore.QSize(80,80))
        self.piecesList.setSpacing(10)
        self.piecesList.setMovement(QtGui.QListView.Snap)
        self.piecesList.setAcceptDrops(True)
        self.piecesList.setDropIndicatorShown(True)

        self.model = PiecesModel(self)
        self.piecesList.setModel(self.model)

        self.puzzleWidget = PuzzleWidget()

        self.puzzleWidget.puzzleCompleted.connect(self.setCompleted,
                QtCore.Qt.QueuedConnection)

        frameLayout.addWidget(self.piecesList)
        frameLayout.addWidget(self.puzzleWidget)
        self.setCentralWidget(frame)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.openImage(':/images/example.jpg')
    window.show()
    sys.exit(app.exec_())
