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

        self.out0 = ReroutePin('out0', self, DataTypes.Reroute, PinDirection.Output)
        self.outputs[self.out0.uid] = self.out0
        self.out0.setX(5)
        self.out0.OnPinConnected.connect(self.outputConnected)

        pinAffects(self.inp0, self.out0)
        self.r = 10
        self._connected = False
        self.label().hide()
        self._pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.inp0.hide()
        self.out0.hide()

    def inputConnected(self, other):
        self._connected = True

    def outputConnected(self, other):
        self._connected = True

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
        data = self.inp0.getData()
        self.out0.setData(data)
