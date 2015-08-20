from PySide import QtCore
from PySide import QtGui
from Settings import Colors
from Settings import get_line_type
from AbstractGraph import *


class Edge(QtGui.QGraphicsLineItem, Colors):

    def __init__(self, source, destination, graph):
        QtGui.QGraphicsLineItem.__init__(self)
        self.source = source
        self.graph = graph
        self.destination = destination
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setFlag(self.ItemIsSelectable)

        self.setZValue(1)
        self.connection = {'From': self.source.port_name(),
                           'To': self.destination.port_name()}

        self.setToolTip(self.connection['From']+'>>>'+self.connection['To'])
        self.settings = self.graph.get_settings()
        if self.settings:
            self.color = QtGui.QColor(self.settings.value('SCENE/Edge color'))
            self.lineType = get_line_type(self.settings.value('SCENE/Edge pen type'))
            self.thikness = float(self.settings.value('SCENE/Edge line thickness'))

    def __str__(self):
        return '{0}.{1} >>> {2}.{3}'.format(self.source.parent.name,
                                            self.source.name,
                                            self.destination.parent.name,
                                            self.destination.name)

    def source_port_name(self):

        return self.source.port_name()

    def destination_port_name(self):

        return self.destination.port_name()

    def paint(self, painter, option, widget):
        if self.settings:
            pen = QtGui.QPen(self.color, self.thikness, self.lineType, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            pen = QtGui.QPen(self.kConnectionLines, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        offset = self.source.boundingRect().width()/2

        p1 = self.source.sceneTransform().map(QtCore.QPointF(offset*2, offset))
        p2 = self.destination.sceneTransform().map(QtCore.QPointF(0, offset))

        distance = p2.x() - p1.x()
        multiply = 3
        path = QtGui.QPainterPath()
        path.moveTo(p1)
        if distance < 0:
            path.cubicTo(QtCore.QPoint(p1.x()+distance/-multiply, p1.y()), QtCore.QPoint(p2.x()-distance/-multiply, p2.y()), p2)
        else:
            path.cubicTo(QtCore.QPoint(p1.x()+distance/multiply, p1.y()), QtCore.QPoint(p2.x()-distance/2, p2.y()), p2)
        painter.setPen(pen)
        painter.drawPath(path)

    def boundingRect(self):

        return QtCore.QRectF(self.source.scenePos(), self.destination.scenePos())


class RealTimeLine(QtGui.QGraphicsLineItem, Colors):
    def __init__(self, graph):
        super(RealTimeLine, self).__init__()
        self.p1 = QtCore.QPointF(0, 0)
        self.p2 = QtCore.QPointF(50, 50)
        self.graph = graph
        self.offset = 0
        self.setZValue(1)

    def paint(self, painter, option, widget):

        painter.setPen(QtGui.QPen(self.kBlack, 1, QtCore.Qt.SolidLine))
        if self.graph.pressed_item and hasattr(self.graph.pressed_item, 'object_type'):
            if self.graph.pressed_item.object_type == AGObjectTypes.tPort:
                self.offset = self.graph.pressed_item.boundingRect().width()/2
                painter.drawLine(self.mapToParent(QtCore.QPointF(self.p1.x()+self.offset,
                                                                 self.p1.y()+self.offset)),
                                 self.p2)

    def boundingRect(self):
        return QtCore.QRectF(self.p1, self.p2)
