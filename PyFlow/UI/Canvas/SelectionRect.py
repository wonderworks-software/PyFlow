## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from qtpy import QtGui, QtWidgets, QtCore


class SelectionRect(QtWidgets.QGraphicsWidget):
    __backgroundColor = QtGui.QColor(100, 100, 100, 50)
    __backgroundAddColor = QtGui.QColor(0, 100, 0, 50)
    __backgroundSubColor = QtGui.QColor(100, 0, 0, 50)
    __backgroundSwitchColor = QtGui.QColor(0, 0, 100, 50)
    __pen = QtGui.QPen(QtGui.QColor(255, 255, 255), 1.0, QtCore.Qt.DashLine)

    def __init__(self, graph, mouseDownPos, modifiers):
        super(SelectionRect, self).__init__()
        self.setZValue(2)

        self.__graph = graph
        self.__graph.scene().addItem(self)
        self.__mouseDownPos = mouseDownPos
        self.__modifiers = modifiers
        self.setPos(self.__mouseDownPos)
        self.resize(0, 0)
        self.selectFullyIntersectedItems = False

    def collidesWithItem(self, item):
        if self.selectFullyIntersectedItems:
            return self.sceneBoundingRect().contains(item.sceneBoundingRect())
        return super(SelectionRect, self).collidesWithItem(item)

    def setDragPoint(self, dragPoint, modifiers):
        self.__modifiers = modifiers
        topLeft = QtCore.QPointF(self.__mouseDownPos)
        bottomRight = QtCore.QPointF(dragPoint)
        if dragPoint.x() < self.__mouseDownPos.x():
            topLeft.setX(dragPoint.x())
            bottomRight.setX(self.__mouseDownPos.x())
        if dragPoint.y() < self.__mouseDownPos.y():
            topLeft.setY(dragPoint.y())
            bottomRight.setY(self.__mouseDownPos.y())
        self.setPos(topLeft)
        self.resize(bottomRight.x() - topLeft.x(), bottomRight.y() - topLeft.y())

    def paint(self, painter, option, widget):
        rect = self.windowFrameRect()
        if self.__modifiers == QtCore.Qt.NoModifier:
            painter.setBrush(self.__backgroundColor)
        if self.__modifiers == QtCore.Qt.ShiftModifier:
            painter.setBrush(self.__backgroundAddColor)
        elif self.__modifiers == QtCore.Qt.ControlModifier:
            painter.setBrush(self.__backgroundSwitchColor)
        elif self.__modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier:
            painter.setBrush(self.__backgroundSubColor)
        painter.setPen(self.__pen)
        painter.drawRect(rect)

    def destroy(self):
        self.__graph.scene().removeItem(self)
