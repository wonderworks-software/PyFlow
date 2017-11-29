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

import sys
from PySide import QtCore, QtGui


NoTransformation, Translate, Rotate, Scale = range(4)

class RenderArea(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        newFont = self.font()
        newFont.setPixelSize(12)
        self.setFont(newFont)

        fontMetrics = QtGui.QFontMetrics(newFont)
        self.xBoundingRect = fontMetrics.boundingRect(self.tr("x"))
        self.yBoundingRect = fontMetrics.boundingRect(self.tr("y"))
        self.shape = QtGui.QPainterPath()
        self.operations = []

    def setOperations(self, operations):
        self.operations = operations
        self.update()

    def setShape(self, shape):
        self.shape = shape
        self.update()

    def minimumSizeHint(self):
        return QtCore.QSize(182, 182)

    def sizeHint(self):
        return QtCore.QSize(232, 182)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.white))

        painter.translate(66, 66)

        painter.save()
        self.transformPainter(painter)
        self.drawShape(painter)
        painter.restore()

        self.drawOutline(painter)

        painter.save()
        self.transformPainter(painter)
        self.drawCoordinates(painter)
        painter.restore()
        painter.end()

    def drawCoordinates(self, painter):
        painter.setPen(QtCore.Qt.red)

        painter.drawLine(0, 0, 50, 0)
        painter.drawLine(48, -2, 50, 0)
        painter.drawLine(48, 2, 50, 0)
        painter.drawText(60 - self.xBoundingRect.width() / 2,
                         0 + self.xBoundingRect.height() / 2, self.tr("x"))

        painter.drawLine(0, 0, 0, 50)
        painter.drawLine(-2, 48, 0, 50)
        painter.drawLine(2, 48, 0, 50)
        painter.drawText(0 - self.yBoundingRect.width() / 2,
                         60 + self.yBoundingRect.height() / 2, self.tr("y"))

    def drawOutline(self, painter):
        painter.setPen(QtCore.Qt.darkGreen)
        painter.setPen(QtCore.Qt.DashLine)
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(0, 0, 100, 100)

    def drawShape(self, painter):
        painter.fillPath(self.shape, QtCore.Qt.blue)

    def transformPainter(self, painter):
        for operation in self.operations:
            if operation == Translate:
                painter.translate(50, 50)

            elif operation == Scale:
                painter.scale(0.75, 0.75)

            elif operation == Rotate:
                painter.rotate(60)


class Window(QtGui.QWidget):

    operationTable = (NoTransformation, Rotate, Scale, Translate)
    NumTransformedAreas = 3

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.originalRenderArea = RenderArea()

        self.shapeComboBox = QtGui.QComboBox()
        self.shapeComboBox.addItem(self.tr("Clock"))
        self.shapeComboBox.addItem(self.tr("House"))
        self.shapeComboBox.addItem(self.tr("Text"))
        self.shapeComboBox.addItem(self.tr("Truck"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.originalRenderArea, 0, 0)
        layout.addWidget(self.shapeComboBox, 1, 0)

        self.transformedRenderAreas = range(Window.NumTransformedAreas)
        self.operationComboBoxes = range(Window.NumTransformedAreas)

        for i in range(Window.NumTransformedAreas):
            self.transformedRenderAreas[i] = RenderArea()

            self.operationComboBoxes[i] = QtGui.QComboBox()
            self.operationComboBoxes[i].addItem(self.tr("No transformation"))
            self.operationComboBoxes[i].addItem(self.tr("Rotate by 60\xB0"))
            self.operationComboBoxes[i].addItem(self.tr("Scale to 75%"))
            self.operationComboBoxes[i].addItem(self.tr("Translate by (50, 50)"))

            self.connect(self.operationComboBoxes[i], QtCore.SIGNAL("activated(int)"),
                         self.operationChanged)

            layout.addWidget(self.transformedRenderAreas[i], 0, i + 1)
            layout.addWidget(self.operationComboBoxes[i], 1, i + 1)

        self.setLayout(layout)
        self.setupShapes()
        self.shapeSelected(0)

        self.setWindowTitle(self.tr("Transformations"))

    def setupShapes(self):
        truck = QtGui.QPainterPath()
        truck.setFillRule(QtCore.Qt.WindingFill)
        truck.moveTo(0.0, 87.0)
        truck.lineTo(0.0, 60.0)
        truck.lineTo(10.0, 60.0)
        truck.lineTo(35.0, 35.0)
        truck.lineTo(100.0, 35.0)
        truck.lineTo(100.0, 87.0)
        truck.lineTo(0.0, 87.0)
        truck.moveTo(17.0, 60.0)
        truck.lineTo(55.0, 60.0)
        truck.lineTo(55.0, 40.0)
        truck.lineTo(37.0, 40.0)
        truck.lineTo(17.0, 60.0)
        truck.addEllipse(17.0, 75.0, 25.0, 25.0)
        truck.addEllipse(63.0, 75.0, 25.0, 25.0)

        clock = QtGui.QPainterPath()
        clock.addEllipse(-50.0, -50.0, 100.0, 100.0)
        clock.addEllipse(-48.0, -48.0, 96.0, 96.0)
        clock.moveTo(0.0, 0.0)
        clock.lineTo(-2.0, -2.0)
        clock.lineTo(0.0, -42.0)
        clock.lineTo(2.0, -2.0)
        clock.lineTo(0.0, 0.0)
        clock.moveTo(0.0, 0.0)
        clock.lineTo(2.732, -0.732)
        clock.lineTo(24.495, 14.142)
        clock.lineTo(0.732, 2.732)
        clock.lineTo(0.0, 0.0)

        house = QtGui.QPainterPath()
        house.moveTo(-45.0, -20.0)
        house.lineTo(0.0, -45.0)
        house.lineTo(45.0, -20.0)
        house.lineTo(45.0, 45.0)
        house.lineTo(-45.0, 45.0)
        house.lineTo(-45.0, -20.0)
        house.addRect(15.0, 5.0, 20.0, 35.0)
        house.addRect(-35.0, -15.0, 25.0, 25.0)

        text = QtGui.QPainterPath()
        font = QtGui.QFont()
        font.setPixelSize(50)
        fontBoundingRect = QtGui.QFontMetrics(font).boundingRect(self.tr("Qt"))
        text.addText(-QtCore.QPointF(fontBoundingRect.center()), font, self.tr("Qt"))

        self.shapes = (clock, house, text, truck)

        self.connect(self.shapeComboBox, QtCore.SIGNAL("activated(int)"),
                     self.shapeSelected)

    def operationChanged(self):
        operations = []
        for i in range(Window.NumTransformedAreas):
            index = self.operationComboBoxes[i].currentIndex()
            operations.append(Window.operationTable[index])
            self.transformedRenderAreas[i].setOperations(operations[:])

    def shapeSelected(self, index):
        shape = self.shapes[index]
        self.originalRenderArea.setShape(shape)
        for i in range(Window.NumTransformedAreas):
            self.transformedRenderAreas[i].setShape(shape)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
