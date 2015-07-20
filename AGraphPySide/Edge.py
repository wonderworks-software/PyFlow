from PySide import QtCore
from PySide import QtGui
from Settings import Colors
from AbstractGraph import *


class Edge(QtGui.QGraphicsLineItem, Colors, AGEdge):

    def __init__(self, source, destination, arrow_size=5.0, color=Colors.kConnectionLines):
        QtGui.QGraphicsLineItem.__init__(self)
        AGEdge.__init__(self, source, destination)
        self.arrow_size = arrow_size
        self.color = color
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)

        self.setZValue(-1)
        self.connection = {'From': self.source.parent.label.name+'.'+self.source.name,
                           'To': self.destination.parent.label.name+'.'+self.destination.name}

        self.setToolTip(self.connection['From']+'>>>'+self.connection['To'])

    def paint(self, painter, option, widget):
        painter.setPen(QtGui.QPen(self.kConnectionLines, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        offset = self.source.boundingRect().width()/2

        p1 = self.source.sceneTransform().map(QtCore.QPointF(offset, offset))
        p2 = self.destination.sceneTransform().map(QtCore.QPointF(offset, offset))
        painter.drawLine(p1, p2)

    def boundingRect(self):
        return QtCore.QRectF(self.source.scenePos(), self.destination.scenePos())
