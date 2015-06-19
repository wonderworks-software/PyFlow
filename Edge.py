from PySide import QtCore
from PySide import QtGui
from Settings import Colors


class Edge(QtGui.QGraphicsLineItem, Colors):

    def __init__(self, source_node, destination_node, arrow_size=5.0, color=Colors.kConnectionLines):
        QtGui.QGraphicsLineItem.__init__(self)
        self.Type = 'EDGE'
        self.arrow_size = arrow_size
        self.color = color
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = source_node
        self.destination = destination_node

        self.setZValue(-1)
        self.connection = {'From': self.source.owned_node.label.name+'.'+self.source.name,
                           'To': self.destination.owned_node.label.name+'.'+self.destination.name}

        self.setToolTip(self.connection['From']+'>>>'+self.connection['To'])

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(self.kConnectionLines, 2, QtCore.Qt.DashDotLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        offset = self.source.boundingRect().width()/2

        p1 = self.source.sceneTransform().map(QtCore.QPointF(offset, offset))
        p2 = self.destination.sceneTransform().map(QtCore.QPointF(offset, offset))
        painter.drawLine(p1, p2)

    def boundingRect(self):
        return QtCore.QRectF(self.source.scenePos(), self.destination.scenePos())
