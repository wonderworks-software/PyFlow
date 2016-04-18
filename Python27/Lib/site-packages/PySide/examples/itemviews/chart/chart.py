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

import math

from PySide import QtCore, QtGui

import chart_rc


class PieView(QtGui.QAbstractItemView):
    def __init__(self, parent=None):
        super(PieView, self).__init__(parent)

        self.horizontalScrollBar().setRange(0, 0)
        self.verticalScrollBar().setRange(0, 0)

        self.margin = 8
        self.totalSize = 300
        self.pieSize = self.totalSize - 2*self.margin
        self.validItems = 0
        self.totalValue = 0.0
        self.origin = QtCore.QPoint()
        self.rubberBand = None

    def dataChanged(self, topLeft, bottomRight):
        super(PieView, self).dataChanged(topLeft, bottomRight)

        self.validItems = 0
        self.totalValue = 0.0

        for row in range(self.model().rowCount(self.rootIndex())):

            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue += value
                self.validItems += 1

        self.viewport().update()

    def edit(self, index, trigger, event):
        if index.column() == 0:
            return super(PieView, self).edit(index, trigger, event)
        else:
            return False

    def indexAt(self, point):
        if self.validItems == 0:
            return QtCore.QModelIndex()

        # Transform the view coordinates into contents widget coordinates.
        wx = point.x() + self.horizontalScrollBar().value()
        wy = point.y() + self.verticalScrollBar().value()

        if wx < self.totalSize:
            cx = wx - self.totalSize/2
            cy = self.totalSize/2 - wy; # positive cy for items above the center

            # Determine the distance from the center point of the pie chart.
            d = (cx**2 + cy**2)**0.5

            if d == 0 or d > self.pieSize/2:
                return QtCore.QModelIndex()

            # Determine the angle of the point.
            angle = (180 / math.pi) * math.acos(cx/d)
            if cy < 0:
                angle = 360 - angle

            # Find the relevant slice of the pie.
            startAngle = 0.0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    sliceAngle = 360*value/self.totalValue

                    if angle >= startAngle and angle < (startAngle + sliceAngle):
                        return self.model().index(row, 1, self.rootIndex())

                    startAngle += sliceAngle

        else:
            itemHeight = QtGui.QFontMetrics(self.viewOptions().font).height()
            listItem = int((wy - self.margin) / itemHeight)
            validRow = 0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                if self.model().data(index) > 0.0:

                    if listItem == validRow:
                        return self.model().index(row, 0, self.rootIndex())

                    # Update the list index that corresponds to the next valid
                    # row.
                    validRow += 1

        return QtCore.QModelIndex()

    def isIndexHidden(self, index):
        return False

    def itemRect(self, index):
        if not index.isValid():
            return QtCore.QRect()

        # Check whether the index's row is in the list of rows represented
        # by slices.

        if index.column() != 1:
            valueIndex = self.model().index(index.row(), 1, self.rootIndex())
        else:
            valueIndex = index

        if self.model().data(valueIndex) > 0.0:

            listItem = 0
            for row in range(index.row()-1, -1, -1):
                if self.model().data(self.model().index(row, 1, self.rootIndex())) > 0.0:
                    listItem += 1

            if index.column() == 0:

                itemHeight = QtGui.QFontMetrics(self.viewOptions().font).height()
                return QtCore.QRect(self.totalSize,
                             int(self.margin + listItem*itemHeight),
                             self.totalSize - self.margin, int(itemHeight))
            elif index.column() == 1:
                return self.viewport().rect()

        return QtCore.QRect()

    def itemRegion(self, index):
        if not index.isValid():
            return QtGui.QRegion()

        if index.column() != 1:
            return QtGui.QRegion(self.itemRect(index))

        if self.model().data(index) <= 0.0:
            return QtGui.QRegion()

        startAngle = 0.0
        for row in range(self.model().rowCount(self.rootIndex())):

            sliceIndex = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(sliceIndex)

            if value > 0.0:
                angle = 360*value/self.totalValue

                if sliceIndex == index:
                    slicePath = QtGui.QPainterPath()
                    slicePath.moveTo(self.totalSize/2, self.totalSize/2)
                    slicePath.arcTo(self.margin, self.margin,
                            self.margin+self.pieSize, self.margin+self.pieSize,
                            startAngle, angle)
                    slicePath.closeSubpath()

                    return QtGui.QRegion(slicePath.toFillPolygon().toPolygon())

                startAngle += angle

        return QtGui.QRegion()

    def horizontalOffset(self):
        return self.horizontalScrollBar().value()

    def mousePressEvent(self, event):
        super(PieView, self).mousePressEvent(event)

        self.origin = event.pos()
        if not self.rubberBand:
            self.rubberBand = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle,
                    self)
        self.rubberBand.setGeometry(QtCore.QRect(self.origin, QtCore.QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if self.rubberBand:
            self.rubberBand.setGeometry(QtCore.QRect(self.origin, event.pos()).normalized())

        super(PieView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(PieView, self).mouseReleaseEvent(event)

        if self.rubberBand:
            self.rubberBand.hide()

        self.viewport().update()

    def moveCursor(self, cursorAction, modifiers):
        current = self.currentIndex()

        if cursorAction == QtGui.QAbstractItemView.MoveLeft or \
           cursorAction == QtGui.QAbstractItemView.MoveUp:

            if current.row() > 0:
                current = self.model().index(current.row() - 1,
                        current.column(), self.rootIndex())
            else:
                current = self.model().index(0, current.column(),
                        self.rootIndex())

        elif cursorAction == QtGui.QAbstractItemView.MoveRight or \
             cursorAction == QtGui.QAbstractItemView.MoveDown:

            if current.row() < rows(current) - 1:
                current = self.model().index(current.row() + 1,
                        current.column(), self.rootIndex())
            else:
                current = self.model().index(rows(current) - 1,
                        current.column(), self.rootIndex())

        self.viewport().update()
        return current

    def paintEvent(self, event):
        selections = self.selectionModel()
        option = self.viewOptions()
        state = option.state

        background = option.palette.base()
        foreground = QtGui.QPen(option.palette.color(QtGui.QPalette.WindowText))
        textPen = QtGui.QPen(option.palette.color(QtGui.QPalette.Text))
        highlightedPen = QtGui.QPen(option.palette.color(QtGui.QPalette.HighlightedText))

        painter = QtGui.QPainter(self.viewport())
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        painter.fillRect(event.rect(), background)
        painter.setPen(foreground)

        # Viewport rectangles
        pieRect = QtCore.QRect(self.margin, self.margin, self.pieSize,
                self.pieSize)
        keyPoint = QtCore.QPoint(self.totalSize - self.horizontalScrollBar().value(),
                self.margin - self.verticalScrollBar().value())

        if self.validItems > 0:
            painter.save()
            painter.translate(pieRect.x() - self.horizontalScrollBar().value(),
                    pieRect.y() - self.verticalScrollBar().value())
            painter.drawEllipse(0, 0, self.pieSize, self.pieSize)
            startAngle = 0.0

            for row in range(self.model().rowCount(self.rootIndex())):

                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    angle = 360*value/self.totalValue

                    colorIndex = self.model().index(row, 0, self.rootIndex())
                    color = self.model().data(colorIndex,
                            QtCore.Qt.DecorationRole)

                    if self.currentIndex() == index:
                        painter.setBrush(QtGui.QBrush(color,
                                QtCore.Qt.Dense4Pattern))
                    elif selections.isSelected(index):
                        painter.setBrush(QtGui.QBrush(color,
                                QtCore.Qt.Dense3Pattern))
                    else:
                        painter.setBrush(QtGui.QBrush(color))

                    painter.drawPie(0, 0, self.pieSize, self.pieSize,
                            int(startAngle*16), int(angle*16))

                    startAngle += angle

            painter.restore()

            keyNumber = 0

            for row in range(self.model().rowCount(self.rootIndex())):
                index = self.model().index(row, 1, self.rootIndex())
                value = self.model().data(index)

                if value > 0.0:
                    labelIndex = self.model().index(row, 0, self.rootIndex())

                    option = self.viewOptions()
                    option.rect = self.visualRect(labelIndex)
                    if selections.isSelected(labelIndex):
                        option.state |= QtGui.QStyle.State_Selected
                    if self.currentIndex() == labelIndex:
                        option.state |= QtGui.QStyle.State_HasFocus
                    self.itemDelegate().paint(painter, option, labelIndex)

                    keyNumber += 1

    def resizeEvent(self, event):
        self.updateGeometries()

    def rows(self, index):
        return self.model().rowCount(self.model().parent(index))

    def rowsInserted(self, parent, start, end):
        for row in range(start, end + 1):
            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue += value
                self.validItems += 1

        super(PieView, self).rowsInserted(parent, start, end)

    def rowsAboutToBeRemoved(self, parent, start, end):
        for row in range(start, end + 1):
            index = self.model().index(row, 1, self.rootIndex())
            value = self.model().data(index)

            if value is not None and value > 0.0:
                self.totalValue -= value
                self.validItems -= 1

        super(PieView, self).rowsAboutToBeRemoved(parent, start, end)

    def scrollContentsBy(self, dx, dy):
        self.viewport().scroll(dx, dy)

    def scrollTo(self, index, ScrollHint):
        area = self.viewport().rect()
        rect = self.visualRect(index)

        if rect.left() < area.left():
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + rect.left() - area.left())
        elif rect.right() > area.right():
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() + min(
                    rect.right() - area.right(), rect.left() - area.left()))

        if rect.top() < area.top():
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + rect.top() - area.top())
        elif rect.bottom() > area.bottom():
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + min(
                    rect.bottom() - area.bottom(), rect.top() - area.top()))

    def setSelection(self, rect, command):
        # Use content widget coordinates because we will use the itemRegion()
        # function to check for intersections.

        contentsRect = rect.translated(self.horizontalScrollBar().value(),
                self.verticalScrollBar().value()).normalized()

        rows = self.model().rowCount(self.rootIndex())
        columns = self.model().columnCount(self.rootIndex())
        indexes = []

        for row in range(rows):
            for column in range(columns):
                index = self.model().index(row, column, self.rootIndex())
                region = self.itemRegion(index)
                if not region.intersected(QtGui.QRegion(contentsRect)).isEmpty():
                    indexes.append(index)

        if len(indexes) > 0:
            firstRow = indexes[0].row()
            lastRow = indexes[0].row()
            firstColumn = indexes[0].column()
            lastColumn = indexes[0].column()

            for i in range(1, len(indexes)):
                firstRow = min(firstRow, indexes[i].row())
                lastRow = max(lastRow, indexes[i].row())
                firstColumn = min(firstColumn, indexes[i].column())
                lastColumn = max(lastColumn, indexes[i].column())

            selection = QtGui.QItemSelection(
                self.model().index(firstRow, firstColumn, self.rootIndex()),
                self.model().index(lastRow, lastColumn, self.rootIndex()))
            self.selectionModel().select(selection, command)
        else:
            noIndex = QtCore.QModelIndex()
            selection = QtGui.QItemSelection(noIndex, noIndex)
            self.selectionModel().select(selection, command)

        self.update()

    def updateGeometries(self):
        self.horizontalScrollBar().setPageStep(self.viewport().width())
        self.horizontalScrollBar().setRange(0, max(0, 2*self.totalSize - self.viewport().width()))
        self.verticalScrollBar().setPageStep(self.viewport().height())
        self.verticalScrollBar().setRange(0, max(0, self.totalSize - self.viewport().height()))

    def verticalOffset(self):
        return self.verticalScrollBar().value()

    def visualRect(self, index):
        rect = self.itemRect(index)
        if rect.isValid():
            return QtCore.QRect(rect.left() - self.horizontalScrollBar().value(),
                         rect.top() - self.verticalScrollBar().value(),
                         rect.width(), rect.height())
        else:
            return rect

    def visualRegionForSelection(self, selection):
        region = QtGui.QRegion()

        for span in selection:
            for row in range(span.top(), span.bottom() + 1):
                for col in range(span.left(), span.right() + 1):
                    index = self.model().index(row, col, self.rootIndex())
                    region += self.visualRect(index)

        return region


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        fileMenu = QtGui.QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")
        saveAction = fileMenu.addAction("&Save As...")
        saveAction.setShortcut("Ctrl+S")
        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        self.setupModel()
        self.setupViews()

        openAction.triggered.connect(self.openFile)
        saveAction.triggered.connect(self.saveFile)
        quitAction.triggered.connect(QtGui.qApp.quit)

        self.menuBar().addMenu(fileMenu)
        self.statusBar()

        self.openFile(':/Charts/qtdata.cht')

        self.setWindowTitle("Chart")
        self.resize(870, 550)

    def setupModel(self):
        self.model = QtGui.QStandardItemModel(8, 2, self)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Label")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Quantity")

    def setupViews(self):
        splitter = QtGui.QSplitter()
        table = QtGui.QTableView()
        self.pieChart = PieView()
        splitter.addWidget(table)
        splitter.addWidget(self.pieChart)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        table.setModel(self.model)
        self.pieChart.setModel(self.model)

        self.selectionModel = QtGui.QItemSelectionModel(self.model)
        table.setSelectionModel(self.selectionModel)
        self.pieChart.setSelectionModel(self.selectionModel)

        table.horizontalHeader().setStretchLastSection(True)

        self.setCentralWidget(splitter)

    def openFile(self, path=None):
        if not path:
            path = QtGui.QFileDialog.getOpenFileName(self,
                    "Choose a data file", '', '*.cht')[0]

        if path:
            f = QtCore.QFile(path)

            if f.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text):
                stream = QtCore.QTextStream(f)

                self.model.removeRows(0,
                        self.model.rowCount(QtCore.QModelIndex()),
                        QtCore.QModelIndex())

                row = 0
                line = stream.readLine()
                while line:
                    self.model.insertRows(row, 1, QtCore.QModelIndex())

                    pieces = line.split(',')
                    self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()),
                                pieces[0])
                    self.model.setData(self.model.index(row, 1, QtCore.QModelIndex()),
                                float(pieces[1]))
                    self.model.setData(self.model.index(row, 0, QtCore.QModelIndex()),
                                QtGui.QColor(pieces[2]),
                                QtCore.Qt.DecorationRole)

                    row += 1
                    line = stream.readLine()

                f.close()
                self.statusBar().showMessage("Loaded %s" % path, 2000)

    def saveFile(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save file as", '',
                '*.cht')

        if fileName:
            f = QtCore.QFile(fileName)

            if f.open(QtCore.QFile.WriteOnly | QtCore.QFile.Text):
                for row in range(self.model.rowCount(QtCore.QModelIndex())):
                    pieces = []

                    pieces.append(self.model.data(self.model.index(row, 0, QtCore.QModelIndex()),
                            QtCore.Qt.DisplayRole))
                    pieces.append(str(self.model.data(self.model.index(row, 1, QtCore.QModelIndex()),
                            QtCore.Qt.DisplayRole)))
                    pieces.append(self.model.data(self.model.index(row, 0, QtCore.QModelIndex()),
                            QtCore.Qt.DecorationRole).name())

                    f.write(QtCore.QByteArray(','.join(pieces)))
                    f.write('\n')

            f.close()
            self.statusBar().showMessage("Saved %s" % fileName, 2000)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
