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

import sys
from PySide import QtCore, QtGui

import pixelator_rc


ItemSize = 256


class PixelDelegate(QtGui.QAbstractItemDelegate):
    def __init__(self, parent=None):
        super(PixelDelegate, self).__init__(parent)

        self.pixelSize = 12

    def paint(self, painter, option, index):
        if option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())

        size = min(option.rect.width(), option.rect.height())
        brightness = index.model().data(index, QtCore.Qt.DisplayRole)
        radius = (size/2.0) - (brightness/255.0 * size/2.0)
        if radius == 0.0:
            return

        painter.save()
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)

        if option.state & QtGui.QStyle.State_Selected:
            painter.setBrush(option.palette.highlightedText())
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.black))

        painter.drawEllipse(QtCore.QRectF(
                            option.rect.x() + option.rect.width()/2 - radius,
                            option.rect.y() + option.rect.height()/2 - radius,
                            2*radius, 2*radius))

        painter.restore()

    def sizeHint(self, option, index):
        return QtCore.QSize(self.pixelSize, self.pixelSize)

    def setPixelSize(self, size):
        self.pixelSize = size


class ImageModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(ImageModel, self).__init__(parent)

        self.modelImage = QtGui.QImage()

    def setImage(self, image):
        self.modelImage = QtGui.QImage(image)
        self.reset()

    def rowCount(self, parent):
        return self.modelImage.height()

    def columnCount(self, parent):
        return self.modelImage.width()

    def data(self, index, role):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return None

        return QtGui.qGray(self.modelImage.pixel(index.column(), index.row()))

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.SizeHintRole:
            return QtCore.QSize(1, 1)

        return None


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.currentPath = QtCore.QDir.homePath()
        self.model = ImageModel(self)

        centralWidget = QtGui.QWidget()

        self.view = QtGui.QTableView()
        self.view.setShowGrid(False)
        self.view.horizontalHeader().hide()
        self.view.verticalHeader().hide()
        self.view.horizontalHeader().setMinimumSectionSize(1)
        self.view.verticalHeader().setMinimumSectionSize(1)
        self.view.setModel(self.model)

        delegate = PixelDelegate(self)
        self.view.setItemDelegate(delegate)

        pixelSizeLabel = QtGui.QLabel("Pixel size:")
        pixelSizeSpinBox = QtGui.QSpinBox()
        pixelSizeSpinBox.setMinimum(4)
        pixelSizeSpinBox.setMaximum(32)
        pixelSizeSpinBox.setValue(12)

        fileMenu = QtGui.QMenu("&File", self)
        openAction = fileMenu.addAction("&Open...")
        openAction.setShortcut("Ctrl+O")

        self.printAction = fileMenu.addAction("&Print...")
        self.printAction.setEnabled(False)
        self.printAction.setShortcut("Ctrl+P")

        quitAction = fileMenu.addAction("E&xit")
        quitAction.setShortcut("Ctrl+Q")

        helpMenu = QtGui.QMenu("&Help", self)
        aboutAction = helpMenu.addAction("&About")

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(helpMenu)

        openAction.triggered.connect(self.chooseImage)
        self.printAction.triggered.connect(self.printImage)
        quitAction.triggered.connect(QtGui.qApp.quit)
        aboutAction.triggered.connect(self.showAboutBox)
        pixelSizeSpinBox.valueChanged[int].connect(delegate.setPixelSize)
        pixelSizeSpinBox.valueChanged[int].connect(self.updateView)

        controlsLayout = QtGui.QHBoxLayout()
        controlsLayout.addWidget(pixelSizeLabel)
        controlsLayout.addWidget(pixelSizeSpinBox)
        controlsLayout.addStretch(1)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.view)
        mainLayout.addLayout(controlsLayout)
        centralWidget.setLayout(mainLayout)

        self.setCentralWidget(centralWidget)

        self.setWindowTitle("Pixelator")
        self.resize(640, 480)

    def chooseImage(self):
        fileName,_ = QtGui.QFileDialog.getOpenFileName(self, "Choose an Image",
                self.currentPath, '*')

        if fileName:
            self.openImage(fileName)

    def openImage(self, fileName):
        image = QtGui.QImage()

        if image.load(fileName):
            self.model.setImage(image)

            if not fileName.startswith(':/'):
                self.currentPath = fileName
                self.setWindowTitle("%s - Pixelator" % self.currentPath)

            self.printAction.setEnabled(True)
            self.updateView()

    def printImage(self):
        if self.model.rowCount(QtCore.QModelIndex()) * self.model.columnCount(QtCore.QModelIndex()) > 90000:
            answer = QtGui.QMessageBox.question(self, "Large Image Size",
                    "The printed image may be very large. Are you sure that "
                    "you want to print it?",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if answer == QtGui.QMessageBox.No:
                return

        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)

        dlg = QtGui.QPrintDialog(printer, self)
        dlg.setWindowTitle("Print Image")

        if dlg.exec_() != QtGui.QDialog.Accepted:
            return

        painter = QtGui.QPainter()
        painter.begin(printer)

        rows = self.model.rowCount(QtCore.QModelIndex())
        columns = self.model.columnCount(QtCore.QModelIndex())
        sourceWidth = (columns+1) * ItemSize
        sourceHeight = (rows+1) * ItemSize

        painter.save()

        xscale = printer.pageRect().width() / float(sourceWidth)
        yscale = printer.pageRect().height() / float(sourceHeight)
        scale = min(xscale, yscale)

        painter.translate(printer.pageRect().x()+printer.pageRect().width()/2,
                          printer.pageRect().y()+printer.pageRect().height()/2)
        painter.scale(scale, scale)
        painter.translate(-sourceWidt/2, -sourceHeight/2)

        option = QtGui.QStyleOptionViewItem()
        parent = QtCore.QModelIndex()

        progress = QtGui.QProgressDialog("Printing...", "Cancel", 0, rows,
                self)
        y = ItemSize / 2.0

        for row in range(rows):
            progress.setValue(row)
            QtGui.qApp.processEvents()
            if progress.wasCanceled():
                break

            x = ItemSize / 2.0

            for col in range(columns):
                option.rect = QtCore.QRect(x, y, ItemSize, ItemSize)
                self.view.itemDelegate.paint(painter, option,
                        self.model.index(row, column, parent))
                x = x + ItemSize

            y = y + ItemSize

        progress.setValue(rows)

        painter.restore()
        painter.end()

        if progress.wasCanceled():
            QtGui.QMessageBox.information(self, "Printing canceled",
                    "The printing process was canceled.",
                    QtGui.QMessageBox.Cancel)

    def showAboutBox(self):
        QtGui.QMessageBox.about(self, "About the Pixelator example",
                "This example demonstrates how a standard view and a custom\n"
                "delegate can be used to produce a specialized "
                "representation\nof data in a simple custom model.")

    def updateView(self):
        self.view.resizeColumnsToContents()
        self.view.resizeRowsToContents()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.openImage(':/images/qt.png')
    sys.exit(app.exec_())
