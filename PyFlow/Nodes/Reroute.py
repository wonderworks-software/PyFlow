from AbstractGraph import *
from Settings import *
from Node import Node
from Pins import ReroutePin


class Reroute(Node, NodeBase):
    def __init__(self, name, graph):
        super(Reroute, self).__init__(name, graph)
        self.inp0 = ReroutePin('in0', self, DataTypes.Reroute, PinDirection.Input)
        self.inputs[self.inp0.uid] = self.inp0
        self.inp0.setX(-5)
        self.inp0.OnPinConnected.connect(self.inputConnected)
        self.inp0.OnPinDisconnected.connect(self.inputDisconnected)

        self.out0 = ReroutePin('out0', self, DataTypes.Reroute, PinDirection.Output)
        self.outputs[self.out0.uid] = self.out0
        self.out0.setX(5)
        self.out0.OnPinConnected.connect(self.outputConnected)
        self.out0.OnPinDisconnected.connect(self.outputDisconnected)

        pinAffects(self.inp0, self.out0)
        self.r = 10
        self._connected = False
        self.label().hide()
        self._pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.inp0.hide()
        self.out0.hide()
        self.dataType = DataTypes.Any
        self.inp0.call = self.compute

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
        if OutxDistance <= 0 or InxDistance >= 0:
            if self.out0.hasConnections() and self.inp0.hasConnections():
                self.inp0.setEdgesControlPointsFlipped(True)
                self.out0.setEdgesControlPointsFlipped(True)
        else:
            self.inp0.setEdgesControlPointsFlipped(False)
            self.out0.setEdgesControlPointsFlipped(False)

    def inputConnected(self, other):
        self._connected = True
        self.dataType = other.dataType
        self.inp0.dataType = self.dataType

    def inputDisconnected(self, other):
        if not self.inp0.hasConnections():
            self.inp0.dataType = DataTypes.Reroute

    def outputConnected(self, other):
        self._connected = True
        self.dataType = other.dataType
        self.out0.dataType = self.dataType

    def outputDisconnected(self, other):
        if not self.out0.hasConnections():
            self.out0.dataType = DataTypes.Reroute

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
    def pinTypeHints():
        return {'inputs': [DataTypes.Any, DataTypes.Exec], 'outputs': [DataTypes.Any, DataTypes.Exec]}

    @staticmethod
    def category():
        return 'Utils'

    @staticmethod
    def keywords():
        return ['knot']

    @staticmethod
    def description():
        return 'Changes edge flow'

    def compute(self):
        if self.dataType is DataTypes.Exec:
            self.out0.call()
        else:
            data = self.inp0.getData()
            self.out0.setData(data)
