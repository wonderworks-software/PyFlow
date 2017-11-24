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
        self.label.hide()

        self.color = BaseNode.getPortColorByType(AGPortDataTypes.tReroute)

        self.inp0 = BaseNode.Port('in', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.inp0.type = AGPortTypes.kInput
        self.inp0.setParentItem(self)
        self.inp0.setY(5.0)
        self.inp0.port_connected = self.OnInputConneceted
        self.inp0.port_disconnected = self.OnInputDisconneceted
        self.inputs.append(self.inp0)

        self.out0 = BaseNode.Port('out', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.out0.type = AGPortTypes.kOutput
        self.out0.setParentItem(self)
        self.out0.setY(5.0)
        self.out0.port_connected = self.OnOutputConnected
        self.out0.port_disconnected = self.OnOutputDisconneceted
        self.outputs.append(self.out0)

        self.srcControlPoint = QtCore.QPoint(0, 0)
        self.dstControlPoint = QtCore.QPoint(0, 0)

        portAffects(self.inp0, self.out0)

        self.inp0.hide()
        self.out0.hide()

        self._pen = QtGui.QPen(Colors.kDirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def Tick(self):
        offset = self.inp0.boundingRect().width() / 3.25
        p1 = None
        p2 = None
        if self.inp0.hasConnections():
            p1 = self.inp0.sceneTransform().map(QtCore.QPointF(offset, offset))
        if self.out0.hasConnections():
            p2 = self.out0.sceneTransform().map(QtCore.QPointF(offset, offset))
        self.srcControlPoint = p1
        self.dstControlPoint = p2

    def OnInputConneceted(self, other):
        self.inp0._connected = True
        self.inp0.color = self.inp0.affected_by[0].color
        self.out0.color = self.inp0.color
        self.inp0.data_type = other.data_type
        if self.out0.hasConnections():
            self.color = self.out0.color
            for e in self.out0.edge_list:
                e.pen.setColor(self.color)
        else:
            self.color = BaseNode.getPortColorByType(other.data_type)
        self.update()

    def OnOutputConnected(self, other):
        self.out0._connected = True
        self.out0.data_type = other.data_type
        if self.inp0.hasConnections():
            self.color = self.inp0.color
        else:
            self.color = BaseNode.getPortColorByType(other.data_type)
        self.update()

    def OnInputDisconneceted(self, other):
        if self.inp0.hasConnections():
            self.inp0._connected = False
        if not self.out0.hasConnections():
            self.resetTypeInfo()

    def OnOutputDisconneceted(self, other):
        if self.out0.hasConnections():
            self.out0._connected = False
        if not self.inp0.hasConnections():
            self.resetTypeInfo()

    def resetTypeInfo(self):
        self.inp0.data_type = AGPortDataTypes.tReroute
        self.out0.data_type = AGPortDataTypes.tReroute
        self.color = BaseNode.getPortColorByType(AGPortDataTypes.tReroute)
        self.update()

    @staticmethod
    def get_category():
        return 'Common'

    def boundingRect(self):
        return QtCore.QRectF(-10.0, -0.5, 30.0, 20.0)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(0, 5, 10, 10)
        arrHeight = 5.0
        wh = 10.0
        arrow = QtGui.QPolygonF([QtCore.QPointF(wh, wh * 0.7 + arrHeight),
                                 QtCore.QPointF(wh * 1.2, wh / 2.0 + arrHeight),
                                 QtCore.QPointF(wh, wh * 0.3 + arrHeight),
                                 QtCore.QPointF(wh, wh * 0.7 + arrHeight)])
        painter.drawPolygon(arrow)
        painter.setBrush(QtCore.Qt.NoBrush)
        if self.isSelected():
            painter.setPen(self._pen)
            painter.drawRoundedRect(self.boundingRect(), 2.0, 2.0)

    @staticmethod
    def description():
        return DESC

    def compute(self):
        data = self.inp0.get_data()
        try:
            self.out0.set_data(data, False)
        except Exception as e:
            print(e)
