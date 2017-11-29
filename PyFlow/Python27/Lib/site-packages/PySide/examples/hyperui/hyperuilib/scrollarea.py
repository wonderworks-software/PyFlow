"""
/*
 * This file is part of PySide: Python for Qt
 *
 * Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * version 2.1 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 *
 */
"""

from PySide import QtGui, QtCore
from kineticscroll import KineticScroll

#Ok I know, this class is not necessary in python
#but this will change the logic and this will bring more work

class ScrollAreaPrivate:
    def __init__(self, parent):
        self._offset = 0
        self._maximumOffset = 0
        self._widget = None
        self._kinetic = None
        self._isDragging = False
        self._mouseDownPos = -1
        self._moveConstant = 15
        self._clickConstant = 25
        self._scrollArea = parent
        self._ignoreList = []


    def smoothPos(self, y):
        if abs(self._mouseDownPos - y) <= self._moveConstant:
            return y
        elif self._mouseDownPos - y < 0:
            return y - self._moveConstant
        else:
            return y + self._moveConstant


    def isClickPossible(self, y):
        if self._isDragging or self._mouseDownPos < 0:
            return False
        else:
            return abs(y - self._mouseDownPos) <= self._clickConstant

    def updateMaximumOffset(self):
        value = 0
        if self._widget:
            value = max(0, self._widget.size().height() - self._scrollArea.size().height())

        if value != self._maximumOffset:
            self._maximumOffset = value
            self._scrollArea.emit(QtCore.SIGNAL("maximumOffsetChanged()"))

    def reconfigure(self):
        if self._widget:
            self._widget.resize(self._scrollArea.size().width(), self._widget.size().height())
            self.updateMaximumOffset()
            self._scrollArea.setOffset(self._offset)

    def sendClick(self, x, y):
        if self._scrollArea.scene() == None:
            return

        event = QtGui.QGraphicsSceneMouseEvent(QtCore.QEvent.GraphicsSceneMousePress)
        event.setButton(QtCore.Qt.LeftButton)
        pos = QtCore.QPointF(x, y)
        event.setScenePos(pos)
        self._ignoreList.append(pos)
        QtCore.QCoreApplication.postEvent(self._scrollArea.scene(), event)

        event = QtGui.QGraphicsSceneMouseEvent(QtCore.QEvent.GraphicsSceneMouseRelease)
        event.setButton(QtCore.Qt.LeftButton)

        pos = QtCore.QPointF(x, y)
        event.setScenePos(pos)
        self._ignoreList.append(pos)
        QtCore.QCoreApplication.postEvent(self._scrollArea.scene(), event)


class ScrollArea(QtGui.QGraphicsWidget):
    def __init__(self, parent = None):
        QtGui.QGraphicsWidget.__init__(self, parent)

        self.setFlags(QtGui.QGraphicsItem.ItemHasNoContents)
        self.setFlags(QtGui.QGraphicsItem.ItemClipsChildrenToShape)

        self._d = ScrollAreaPrivate(self)
        self._d._kinetic = KineticScroll(self)
        self.connect(self._d._kinetic, QtCore.SIGNAL("signalMoveOffset(int)"), QtCore.SLOT("kineticMove(int)"))


    def widget(self):
        return self._d._widget

    def setWidget(self, widget):
        if self._d._widget:
            self._d._widget.setParentItem(0)
            self._d._widget.removeEventFilter(self)
            self._d._widget = None

        if widget:
            self._d._widget = widget
            self._d._widget.setParentItem(self)
            self._d._widget.installEventFilter(self)
            self._d._widget.setPos(0, 0)
            self._d._widget.setFlag(QtGui.QGraphicsItem.ItemStacksBehindParent)
            self._d.reconfigure()


    def offset(self):
        return self._d._offset

    def setOffset(self, offset):
        if self._d._widget:
            value = max(min(offset, self._d._maximumOffset), 0)

            if value != self._d._offset:
                self._d._offset = value
                self._d._widget.setY(-value)
                self.emit(QtCore.SIGNAL("offsetChanged()"))

    def maximumOffset(self):
        return self._d._maximumOffset

    def resizeEvent(self, event):
        QtGui.QGraphicsWidget.resizeEvent(self, event)
        self._d.reconfigure()

    def eventFilter(self, object, event):
        if object == self._d._widget and event.type() == QtCore.QEvent.GraphicsSceneResize:
            self._d.reconfigure()

        return False

    def mousePressEvent(self, event):
        pos = event.scenePos()
        if pos in self._d._ignoreList:
            self._d._ignoreList.remove(pos)
            event.ignore()
            return

        y = event.pos().y()
        self._d._mouseDownPos = y
        self._d._isDragging = not self._d._kinetic.mouseDown(y)

    def stopKinetic(self):
        self._d._kinetic.kineticStop()

    def mouseReleaseEvent(self, event):
        pos = event.scenePos()
        if pos in self._d._ignoreList:
            self._d._ignoreList.remove(pos)
            event.ignore()
            return

        if self._d._mouseDownPos >= 0:
            y = event.pos().y()
            if self._d.isClickPossible(y):
                self._d.sendClick(event.scenePos().x(), event.scenePos().y())
                self._d._kinetic.mouseCancel()
            else:
                self._d._kinetic.mouseUp(self._d.smoothPos(y))

        self._d._mouseDownPos = -1

    def mouseMoveEvent(self, event):
        if self._d._mouseDownPos >= 0:
            y = event.pos().y()

            if not self._d.isClickPossible(y):
                self._d._isDragging = True

            if abs(self._d._mouseDownPos - y) > self._d._moveConstant:
                self._d._kinetic.mouseMove(self._d.smoothPos(y))

    def kineticMove(self, value):
        finalOffset = self.offset() - value
        self.setOffset(finalOffset)

        if value == 0 or finalOffset != self.offset():
            self._d._kinetic.kineticStop()
            return False

        return True




