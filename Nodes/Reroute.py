from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode
from PySide import QtCore

DESC = '''This node's purpose is change flow of edges
'''


class Reroute(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Reroute, self).__init__(name, graph, spacings=Spacings)
        self.h = 25
        self.sizes[4] = self.h
        self.label().hide()

        self.r = 10.0

        self.color = BaseNode.getPortColorByType(AGPortDataTypes.tReroute)
        self.color.setAlpha(255)

        self.inp0 = BaseNode.Port('in', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.inp0.type = AGPortTypes.kInput
        self.inp0.setParentItem(self)
        self.inp0.port_connected = self.OnInputConneceted
        self.inp0.port_disconnected = self.OnInputDisconneceted
        self.inputs.append(self.inp0)
        self._connected = False

        self.out0 = BaseNode.Port('out', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.out0.type = AGPortTypes.kOutput
        self.out0.setParentItem(self)
        self.out0.port_connected = self.OnOutputConnected
        self.out0.port_disconnected = self.OnOutputDisconneceted
        self.outputs.append(self.out0)

        portAffects(self.inp0, self.out0)

        self.cp1 = QtCore.QPointF(0.0, 0.0)
        self.cp2 = QtCore.QPointF(0.0, 0.0)

        self.inp0.hide()
        self.out0.hide()

        self._pen = QtGui.QPen(Colors.kDirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def isReroute(self):
        return True

    def disconnect_all(self):
        if self.inp0.hasConnections():
            self.inp0.disconnect_all()
        if self.out0.hasConnections():
            self.out0.disconnect_all()

    def getOutControlPoint(self):
        cp1 = self.out0.scenePos()
        xDistance = abs(self.out0.scenePos().x() - self.out0.getAvgXConnected())
        if xDistance < 100.0:
            xDistance = 100.0
        if self.out0.bEdgeTangentDirection:
            cp1.setX(self.out0.scenePos().x() - (xDistance / 2.0))
        else:
            cp1.setX(self.out0.scenePos().x() + (xDistance / 2.0))
        return cp1

    def getInControlPoint(self):
        cp2 = self.inp0.scenePos()
        xDistance = abs(self.inp0.scenePos().x() - self.inp0.getAvgXConnected())
        if xDistance < 100.0:
            xDistance = 100.0
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

    def OnInputConneceted(self, other):
        self.inp0._connected = True
        self._connected = True
        self.inp0.color = self.inp0.affected_by[0].color
        self.out0.color = self.inp0.color
        self.inp0.data_type = other.data_type
        self.out0.data_type = other.data_type
        if self.out0.hasConnections():
            self.color = self.out0.color
            self.color.setAlpha(255)
            for e in self.out0.edge_list:
                e.pen.setColor(self.color)
        else:
            self.color = BaseNode.getPortColorByType(other.data_type)
            self.color.setAlpha(255)
        self.update()

    def OnOutputConnected(self, other):
        self.out0._connected = True
        self._connected = True
        self.out0.data_type = other.data_type
        self.inp0.data_type = other.data_type
        if self.inp0.hasConnections():
            self.color = self.inp0.color
            self.color.setAlpha(255)
        else:
            self.color = BaseNode.getPortColorByType(other.data_type)
            self.color.setAlpha(255)
        self.update()

    def OnInputDisconneceted(self, other):
        if self.inp0.hasConnections():
            self.inp0._connected = False
        if not self.out0.hasConnections():
            self.resetTypeInfo()
        self._connected = False
        self.inp0.bEdgeTangentDirection = False
        self.update()

    def OnOutputDisconneceted(self, other):
        if self.out0.hasConnections():
            self.out0._connected = False
        if not self.inp0.hasConnections():
            self.resetTypeInfo()
        self._connected = False
        self.out0.bEdgeTangentDirection = False
        self.update()

    def resetTypeInfo(self):
        self.inp0.data_type = AGPortDataTypes.tReroute
        self.out0.data_type = AGPortDataTypes.tReroute
        self.color = BaseNode.getPortColorByType(AGPortDataTypes.tReroute)
        self.color.setAlpha(255)

    def mousePressEvent(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.AltModifier and event.button() == QtCore.Qt.LeftButton:
            self.disconnect_all()
        super(Reroute, self).mousePressEvent(event)

    @staticmethod
    def get_category():
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
        arrow = QtGui.QPolygonF([QtCore.QPointF(self.r, self.r * 0.7),
                                 QtCore.QPointF(self.r * 1.2, self.r / 2.0),
                                 QtCore.QPointF(self.r, self.r * 0.3),
                                 QtCore.QPointF(self.r, self.r * 0.7)])
        # painter.drawPolygon(arrow)
        painter.setBrush(QtCore.Qt.NoBrush)
        if self.isSelected():
            painter.setPen(self._pen)
            painter.drawRoundedRect(self.boundingRect(), 2.0, 2.0)

    def itemChange(self, change, value):
        return QtGui.QGraphicsItem.itemChange(self, change, value)

    @staticmethod
    def description():
        return DESC

    def compute(self):
        data = self.inp0.get_data()
        try:
            self.out0.set_data(data, False)
        except Exception as e:
            print(e)
