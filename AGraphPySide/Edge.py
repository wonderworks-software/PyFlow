from PySide import QtCore
from PySide import QtGui
from Settings import Colors
from Settings import get_line_type
from AbstractGraph import *
from RerouteNode import RerouteNode


class Edge(QtGui.QGraphicsPathItem, Colors):

    def __init__(self, source, destination, graph):
        QtGui.QGraphicsPathItem.__init__(self)
        self.source = source
        self.graph = graph
        self.source_pos_object = source
        self.destination_pos_object = destination
        self.destination = destination
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self.setZValue(1.0)
        self.connection = {'From': self.source.port_name(),
                           'To': self.destination.port_name()}

        self.settings = self.graph.get_settings()
        if self.settings:
            self.color = QtGui.QColor(self.settings.value('SCENE/Edge color'))
            self.lineType = get_line_type(self.settings.value('SCENE/Edge pen type'))
            self.thikness = float(self.settings.value('SCENE/Edge line thickness'))

        if self.settings:
            self.pen = QtGui.QPen(self.color, self.thikness, self.lineType, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self.pen = QtGui.QPen(self.kConnectionLines, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.setPen(self.pen)

        self.updateCurve(points[0], points[1])

    def __str__(self):
        return '{0}.{1} >>> {2}.{3}'.format(self.source.parent.name,
                                            self.source.name,
                                            self.destination.parent.name,
                                            self.destination.name)

    def hoverEnterEvent(self, event):
        super(Edge, self).hoverEnterEvent(event)
        self.pen.setWidthF(self.thikness+(self.thikness/1.5))
        self.update()
        if self.graph.is_debug():
            print self.__str__()

    def split(self, pos):

        size = 10.0

        # create reroute
        node = RerouteNode(0, 0, size, size, self, None, self.graph)
        self.source.reroutes.append(node)
        self.destination.reroutes.append(node)

        node.left_edge = self
        node.setPos(pos.x()-size/2, pos.y()-size/2)

        # create new edge
        edge = Edge(self.source, self.destination, self.graph)
        self.graph.scene_widget.addItem(edge)

        # set reroute as src pos object on newly created edge
        edge.source_pos_object = node

        # set dst pos object from clicked edge
        edge.destination_pos_object = self.destination_pos_object
        self.graph.edges.append(edge)
        node.right_edge = edge

        # set created node as dst pos object on clicked edge
        self.destination_pos_object = node
        # store
        self.graph.reroutes.append(node)

    def getEndPoints(self):
        offset = self.source_pos_object.boundingRect().width() / 2
        p1 = self.source_pos_object.sceneTransform().map(QtCore.QPointF(offset * 2, offset))
        p2 = self.destination_pos_object.sceneTransform().map(QtCore.QPointF(0, offset))
        return p1, p2

    def mousePressEvent(self, event):
        super(Edge, self).mousePressEvent(event)
        event.accept()

    def kill(self):
        self.graph.remove_edge(self)

    def mouseReleaseEvent(self, event):
        super(Edge, self).mouseReleaseEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        super(Edge, self).mouseMoveEvent(event)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(Edge, self).hoverLeaveEvent(event)
        # self.setZValue(0.0)
        self.pen.setWidthF(self.thikness)
        self.update()

    def source_port_name(self):

        return self.source.port_name()

    def updateCurve(self, p1, p2):
        distance = p2.x() - p1.x()
        multiply = 3
        path = QtGui.QPainterPath()

        path.moveTo(p1)
        if distance < 0:
            path.cubicTo(QtCore.QPoint(p1.x()+distance/-multiply, p1.y()), QtCore.QPoint(p2.x()-distance/-multiply, p2.y()), p2)
        else:
            path.cubicTo(QtCore.QPoint(p1.x()+distance/multiply, p1.y()), QtCore.QPoint(p2.x()-distance/2, p2.y()), p2)

        self.setPath(path)

    def destination_port_name(self):

        return self.destination.port_name()

    def paint(self, painter, option, widget):

        self.setPen(self.pen)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        super(Edge, self).paint(painter, option, widget)


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
                painter.drawLine(self.mapToParent(QtCore.QPointF(self.p1.x()+self.offset, self.p1.y()+self.offset)), self.p2)

    def boundingRect(self):
        return QtCore.QRectF(self.p1, self.p2)
