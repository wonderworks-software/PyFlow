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

import random

from PySide import QtCore, QtGui

import tooltips_rc


class ShapeItem(object):
    def __init__(self):
        self.myPath = QtGui.QPainterPath()
        self.myPosition = QtCore.QPoint()
        self.myColor  = QtGui.QColor()
        self.myToolTip = ''

    def path(self):
        return self.myPath

    def position(self):
        return self.myPosition

    def color(self):
        return self.myColor

    def toolTip(self):
        return self.myToolTip

    def setPath(self, path):
        self.myPath = path

    def setToolTip(self, toolTip):
        self.myToolTip = toolTip

    def setPosition(self, position):
        self.myPosition = position

    def setColor(self, color):
        self.myColor = color


class SortingBox(QtGui.QWidget):
    circle_count = square_count = triangle_count = 1

    def __init__(self):
        super(SortingBox, self).__init__()

        self.circlePath = QtGui.QPainterPath()
        self.squarePath = QtGui.QPainterPath()
        self.trianglePath = QtGui.QPainterPath()
        self.shapeItems = []

        self.previousPosition = QtCore.QPoint()

        self.setMouseTracking(True)
        self.setBackgroundRole(QtGui.QPalette.Base)

        self.itemInMotion = None

        self.newCircleButton = self.createToolButton("New Circle",
                QtGui.QIcon(':/images/circle.png'), self.createNewCircle)
        self.newSquareButton = self.createToolButton("New Square",
                QtGui.QIcon(':/images/square.png'), self.createNewSquare)
        self.newTriangleButton = self.createToolButton("New Triangle",
                QtGui.QIcon(':/images/triangle.png'), self.createNewTriangle)

        self.circlePath.addEllipse(0, 0, 100, 100)
        self.squarePath.addRect(0, 0, 100, 100)

        x = self.trianglePath.currentPosition().x()
        y = self.trianglePath.currentPosition().y()
        self.trianglePath.moveTo(x + 120 / 2, y)
        self.trianglePath.lineTo(0, 100)
        self.trianglePath.lineTo(120, 100)
        self.trianglePath.lineTo(x + 120 / 2, y)

        self.setWindowTitle("Tooltips")
        self.resize(500, 300)

        self.createShapeItem(self.circlePath, "Circle",
                self.initialItemPosition(self.circlePath),
                self.initialItemColor())
        self.createShapeItem(self.squarePath, "Square",
                self.initialItemPosition(self.squarePath),
                self.initialItemColor())
        self.createShapeItem(self.trianglePath, "Triangle",
                self.initialItemPosition(self.trianglePath),
                self.initialItemColor())

    def event(self, event):
        if event.type() == QtCore.QEvent.ToolTip:
            helpEvent = event
            index = self.itemAt(helpEvent.pos())
            if index != -1:
                QtGui.QToolTip.showText(helpEvent.globalPos(),
                        self.shapeItems[index].toolTip())
            else:
                QtGui.QToolTip.hideText()
                event.ignore()

            return True

        return super(SortingBox, self).event(event)

    def resizeEvent(self, event):
        margin = self.style().pixelMetric(QtGui.QStyle.PM_DefaultTopLevelMargin)
        x = self.width() - margin
        y = self.height() - margin

        y = self.updateButtonGeometry(self.newCircleButton, x, y)
        y = self.updateButtonGeometry(self.newSquareButton, x, y)
        self.updateButtonGeometry(self.newTriangleButton, x, y)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for shapeItem in self.shapeItems:
            painter.translate(shapeItem.position())
            painter.setBrush(shapeItem.color())
            painter.drawPath(shapeItem.path())
            painter.translate(-shapeItem.position())

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            index = self.itemAt(event.pos())
            if index != -1:
                self.itemInMotion = self.shapeItems[index]
                self.previousPosition = event.pos()

                value = self.shapeItems[index]
                del self.shapeItems[index]
                self.shapeItems.insert(len(self.shapeItems) - 1, value)

                self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) and self.itemInMotion:
            self.moveItemTo(event.pos())

    def mouseReleaseEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton) and self.itemInMotion:
            self.moveItemTo(event.pos())
            self.itemInMotion = None

    def createNewCircle(self):
        SortingBox.circle_count += 1
        self.createShapeItem(self.circlePath,
                "Circle <%d>" % SortingBox.circle_count,
                self.randomItemPosition(), self.randomItemColor())

    def createNewSquare(self):
        SortingBox.square_count += 1
        self.createShapeItem(self.squarePath,
                "Square <%d>" % SortingBox.square_count,
                self.randomItemPosition(), self.randomItemColor())

    def createNewTriangle(self):
        SortingBox.triangle_count += 1
        self.createShapeItem(self.trianglePath,
                "Triangle <%d>" % SortingBox.triangle_count,
                self.randomItemPosition(), self.randomItemColor())

    def itemAt(self, pos):
        for i in range(len(self.shapeItems) - 1, -1, -1):
            item = self.shapeItems[i]
            if item.path().contains(QtCore.QPointF(pos - item.position())):
                return i

        return -1

    def moveItemTo(self, pos):
        offset = pos - self.previousPosition
        self.itemInMotion.setPosition(self.itemInMotion.position() + offset)
        self.previousPosition = QtCore.QPoint(pos)
        self.update()

    def updateButtonGeometry(self, button, x, y):
        size = button.sizeHint()
        button.setGeometry(x - size.width(), y - size.height(),
                size.width(), size.height())

        return y - size.height() - self.style().pixelMetric(QtGui.QStyle.PM_DefaultLayoutSpacing)

    def createShapeItem(self, path, toolTip, pos, color):
        shapeItem = ShapeItem()
        shapeItem.setPath(path)
        shapeItem.setToolTip(toolTip)
        shapeItem.setPosition(pos)
        shapeItem.setColor(color)
        self.shapeItems.append(shapeItem)
        self.update()

    def createToolButton(self, toolTip, icon, member):
        button = QtGui.QToolButton(self)
        button.setToolTip(toolTip)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(32, 32))
        button.clicked.connect(member)

        return button

    def initialItemPosition(self, path):
        y = (self.height() - path.controlPointRect().height()) / 2

        if len(self.shapeItems) == 0:
            x = ((3 * self.width()) / 2 - path.controlPointRect().width()) / 2
        else:
            x = (self.width() / len(self.shapeItems) - path.controlPointRect().width()) / 2

        return QtCore.QPoint(x, y)

    def randomItemPosition(self):
        x = random.randint(0, self.width() - 120)
        y = random.randint(0, self.height() - 120)

        return QtCore.QPoint(x, y)

    def initialItemColor(self):
        hue = ((len(self.shapeItems) + 1) * 85) % 256
        return QtGui.QColor.fromHsv(hue, 255, 190)

    def randomItemColor(self):
        return QtGui.QColor.fromHsv(random.randint(0, 256), 255, 190)


if __name__ == "__main__":

    import sys

    app = QtGui.QApplication(sys.argv)
    sortingBox = SortingBox()
    sortingBox.show()
    sys.exit(app.exec_())
