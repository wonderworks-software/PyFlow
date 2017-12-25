from AbstractGraph import *
from Settings import *
from Node import Node, getPortColorByType
from Pin import Pin
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QGraphicsRectItem
from Qt.QtWidgets import QApplication


DESC = '''This node's purpose is change flow of edges'''


class RerouteMover(QGraphicsRectItem):
    def __init__(self, parent):
        super(RerouteMover, self).__init__(parent)
        self.setRect(0, 0, 20, 5)
        self.setBrush(QtGui.QColor(0, 0, 0, 0))
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        self.setAcceptHoverEvents(True)
        self.setCursor(QtCore.Qt.OpenHandCursor)

    def hoverEnterEvent(self, event):
        super(RerouteMover, self).hoverEnterEvent(event)


class Reroute(Node, NodeBase):
    def __init__(self, name, graph):
        super(Reroute, self).__init__(name, graph)
        self.h = 25
        self.sizes[4] = self.h
        self.label().hide()
        self.setCursor(QtCore.Qt.CrossCursor)

        self.reroute_mover = RerouteMover(self)

        self.reroute_mover.setX(-5)
        self.reroute_mover.setY(-5)

        self.r = 10.0

        self.setFlag(QGraphicsItem.ItemIsMovable, False)

        self.color = getPortColorByType(DataTypes.Reroute)
        self.color.setAlpha(255)

        self.inp0 = Pin('in', self, DataTypes.Reroute, 10, 10, self.color)
        self.inp0.type = PinTypes.Input
        self.inp0.pinConnected = self.OnInputConneceted
        self.inp0.pinDisconnected = self.OnInputDisconneceted
        self.inputs.append(self.inp0)
        # self.inp0.setX(-15.0)
        self._connected = False

        self.out0 = Pin('out', self, DataTypes.Reroute, 10, 10, self.color)
        self.out0.type = PinTypes.Output
        self.out0.pinConnected = self.OnOutputConnected
        self.out0.pinDisconnected = self.OnOutputDisconneceted
        # self.out0.setX(10.0)
        self.outputs.append(self.out0)

        portAffects(self.inp0, self.out0)

        self.cp1 = QtCore.QPointF(0.0, 0.0)
        self.cp2 = QtCore.QPointF(0.0, 0.0)

        self.inp0.hide()
        self.out0.hide()

        self._pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def isReroute(self):
        return True

    def serialize(self):
        return "createNode ~type {0} ~x {1} ~y {2} ~n {3} ~dataType {4}\n".format(self.__class__.__name__, self.scenePos().x(), self.scenePos().y(), self.name, self.inp0.dataType)

    def disconnectAll(self):
        if self.inp0.hasConnections():
            self.inp0.disconnectAll()
        if self.out0.hasConnections():
            self.out0.disconnectAll()

    def getOutControlPoint(self):
        cp1 = self.out0.scenePos()
        xDistance = abs(self.out0.scenePos().x() - self.out0.getAvgXConnected())
        if xDistance < 70.0:
            xDistance = 70.0
        if self.out0.bEdgeTangentDirection:
            cp1.setX(self.out0.scenePos().x() - (xDistance / 2.0))
        else:
            cp1.setX(self.out0.scenePos().x() + (xDistance / 2.0))
        return cp1

    def getInControlPoint(self):
        cp2 = self.inp0.scenePos()
        xDistance = abs(self.inp0.scenePos().x() - self.inp0.getAvgXConnected())
        if xDistance < 70.0:
            xDistance = 70.0
        if self.inp0.bEdgeTangentDirection:
            cp2.setX(self.inp0.scenePos().x() + (xDistance / 2.0))
        else:
            cp2.setX(self.inp0.scenePos().x() - (xDistance / 2.0))
        return cp2

    def Tick(self, delta):
        InxDistance = self.inp0.getAvgXConnected() - self.inp0.scenePos().x()
        OutxDistance = self.out0.getAvgXConnected() - self.out0.scenePos().x()
        if OutxDistance < 0 or InxDistance > 0:
            if self.out0.hasConnections() and self.inp0.hasConnections():
                self.inp0.setEdgesControlPointsFlipped(True)
                self.out0.setEdgesControlPointsFlipped(True)
        else:
            self.inp0.setEdgesControlPointsFlipped(False)
            self.out0.setEdgesControlPointsFlipped(False)

    def updateColor(self, dataType):
        color = getPortColorByType(dataType)
        self.inp0.color = color
        self.out0.color = color
        for i in self.inp0.edge_list + self.out0.edge_list:
            i.pen.setColor(color)

    def OnInputConneceted(self, other):
        self.inp0._connected = True
        self._connected = True
        # self.inp0.color = self.inp0.affected_by[0].color
        # self.out0.color = self.inp0.color
        self.inp0.dataType = other.dataType
        self.out0.dataType = other.dataType
        self.updateColor(other.dataType)
        if self.out0.hasConnections():
            self.color = self.out0.color
            self.color.setAlpha(255)
            for e in self.out0.edge_list:
                e.pen.setColor(self.color)
        else:
            self.color = getPortColorByType(other.dataType)
            self.color.setAlpha(255)
        self.update()

    def OnOutputConnected(self, other):
        self.out0._connected = True
        self._connected = True
        self.out0.dataType = other.dataType
        self.inp0.dataType = other.dataType
        if self.inp0.hasConnections():
            self.color = self.inp0.color
            self.color.setAlpha(255)
        else:
            self.color = getPortColorByType(other.dataType)
            self.color.setAlpha(255)
        self.update()

    def OnInputDisconneceted(self, other):
        if not self.inp0.hasConnections():
            self.inp0._connected = False
        self._connected = self.inp0.hasConnections() or self.out0.hasConnections()
        if not self._connected:
            self.inp0.bEdgeTangentDirection = False
            self.resetTypeInfo()
        self.update()

    def OnOutputDisconneceted(self, other):
        if not self.out0.hasConnections():
            self.out0._connected = False
        self._connected = self.inp0.hasConnections() or self.out0.hasConnections()
        if not self._connected:
            self.out0.bEdgeTangentDirection = False
            self.resetTypeInfo()
        self.update()

    def resetTypeInfo(self):
        self.inp0.dataType = DataTypes.Reroute
        self.out0.dataType = DataTypes.Reroute
        self.color = getPortColorByType(DataTypes.Reroute)
        self.color.setAlpha(255)

    def mousePressEvent(self, event):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.AltModifier and event.button() == QtCore.Qt.LeftButton:
            self.disconnectAll()
        super(Reroute, self).mousePressEvent(event)

    @staticmethod
    def category():
        return 'Core'

    def boundingRect(self):
        return QtCore.QRectF(-10.0, -5.0, 30.0, 20.0)

    def paint(self, painter, option, widget):
        center = QtCore.QPointF(self.r / 2, self.r / 2)

        linearGrad = QtGui.QRadialGradient(center, self.r / 2)
        if not self._connected:
            linearGrad.setColorAt(0, self.color.darker(280))
            linearGrad.setColorAt(0.5, self.color.darker(280))
            linearGrad.setColorAt(0.65, self.color.lighter(130))
            linearGrad.setColorAt(1, self.color.lighter(70))
            painter.setBrush(QtGui.QBrush(linearGrad))
        else:
            painter.setBrush(self.color)

        painter.drawEllipse(center, self.r / 2, self.r / 2)
        painter.drawEllipse(self.inp0.scenePos(), self.r / 2, self.r / 2)
        arrow = QtGui.QPolygonF([QtCore.QPointF(self.r, self.r * 0.7),
                                 QtCore.QPointF(self.r * 1.2, self.r / 2.0),
                                 QtCore.QPointF(self.r, self.r * 0.3),
                                 QtCore.QPointF(self.r, self.r * 0.7)])
        # painter.drawPolygon(arrow)
        painter.setBrush(QtCore.Qt.NoBrush)
        if self.isSelected():
            painter.setPen(self._pen)
            painter.drawRoundedRect(self.boundingRect(), 2.0, 2.0)

    @staticmethod
    def description():
        return DESC

    def compute(self):
        data = self.inp0.getData()
        try:
            self.out0.setData(data)
        except Exception as e:
            print(e)
