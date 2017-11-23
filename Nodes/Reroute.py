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

        self.inp0 = BaseNode.Port('in', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.inp0.type = AGPortTypes.kInput
        self.inp0.setParentItem(self)
        self.inp0.setY(5.0)
        self.inputs.append(self.inp0)

        self.out0 = BaseNode.Port('out', self, AGPortDataTypes.tReroute, 10, 10, self.color)
        self.out0.type = AGPortTypes.kOutput
        self.out0.setParentItem(self)
        self.out0.setY(5.0)
        self.outputs.append(self.out0)

        portAffects(self.inp0, self.out0)

        self.inp0.hide()
        self.out0.hide()

        self._pen = QtGui.QPen(Colors.kDirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    @staticmethod
    def get_category():
        return 'Common'

    def boundingRect(self):
        return QtCore.QRectF(-10.0, -0.5, 30.0, 20.0)

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
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
