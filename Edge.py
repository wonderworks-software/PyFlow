from PySide import QtCore
from PySide import QtGui
from Settings import Colors


class Edge(QtGui.QGraphicsItem, Colors):

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, source_node, dest_node):
        QtGui.QGraphicsItem.__init__(self)
        self.arrow_size = 10.0
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.source = source_node
        self.destination = dest_node
        self.setZValue(0)
        self.connection = {'From': self.source.owned_node.label.name+'.'+self.source.name,
                           'To': self.destination.owned_node.label.name+'.'+self.destination.name}
        self.setToolTip(self.connection['From']+'>>>'+self.connection['To'])

    def paint(self, painter, option, widget):

        painter.setPen(QtGui.QPen(self.kConnectionLines, 2, QtCore.Qt.DashDotLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        offset = self.source.boundingRect().width()/2
        x1 = self.source.scenePos().x()+offset
        x2 = self.destination.scenePos().x()+offset
        y1 = self.source.scenePos().y()+offset
        y2 = self.destination.scenePos().y()+offset

        # path = QtGui.QPainterPath()
        # path.moveTo(self.source.scenePos().x()+offset, self.source.scenePos().y()+offset)
        # mid = QtCore.QPointF(((x1+x2)/2), ((y1+y2)/2))
        # c_offset = 50
        # mult = y1/y2
        # if y1 > y2:
        #     ctrl1 = QtCore.QPointF(mid.x(), mid.y()+c_offset*mult)
        #     ctrl2 = QtCore.QPointF(mid.x(), mid.y()-c_offset*mult)
        # elif y1 < y2:
        #     ctrl1 = QtCore.QPointF(mid.x(), mid.y()-c_offset*mult)
        #     ctrl2 = QtCore.QPointF(mid.x(), mid.y()+c_offset*mult)
        # path.cubicTo(ctrl1, ctrl2, QtCore.QPointF(self.dest.scenePos().x()+offset, self.dest.scenePos().y()+offset))
        # painter.drawPath(path)
        painter.drawLine(x1, y1, x2, y2)

    def boundingRect(self):

        return QtCore.QRectF()
