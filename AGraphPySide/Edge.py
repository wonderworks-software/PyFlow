from PySide import QtCore
from PySide import QtGui
from Settings import Colors
from Nodes import Reroute
from AbstractGraph import *
import weakref


class Edge(QtGui.QGraphicsPathItem, Colors):

    def __init__(self, source, destination, graph):
        QtGui.QGraphicsPathItem.__init__(self)
        self.graph = weakref.ref(graph)
        self.source = weakref.ref(source)
        self.destination = weakref.ref(destination)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self.path = QtGui.QPainterPath()

        self.setZValue(-1)
        self.connection = {'From': self.source().port_name(),
                           'To': self.destination().port_name()}

        if isinstance(source.parentItem(), Reroute):
            if source.parentItem().inp0.hasConnections():
                self.color = source.parentItem().color
            else:
                self.color = destination.color
        else:
            self.color = self.source().color

        self.thikness = 1.0
        if source.data_type in [AGPortDataTypes.tExec, AGPortDataTypes.tReroute] and destination.data_type in [AGPortDataTypes.tExec, AGPortDataTypes.tReroute]:
            self.thikness = 2.0

        self.pen = QtGui.QPen(self.color, self.thikness, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        self.setPen(self.pen)

        self.source().update()
        self.destination().update()

    def __str__(self):
        return '{0}.{1} >>> {2}.{3}'.format(self.source().parent().name,
                                            self.source().name,
                                            self.destination().parent().name,
                                            self.destination().name)

    def hoverEnterEvent(self, event):
        super(Edge, self).hoverEnterEvent(event)
        self.pen.setWidthF(self.thikness + (self.thikness / 1.5))
        self.update()
        if self.graph().is_debug():
            print(self.__str__())

    def getEndPoints(self):
        offset = self.source().boundingRect().width() / 3.25
        p1 = self.source().sceneTransform().map(QtCore.QPointF(offset * 2, offset))
        p2 = self.destination().sceneTransform().map(QtCore.QPointF(0, offset))
        return p1, p2

    def mousePressEvent(self, event):
        super(Edge, self).mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        super(Edge, self).mouseReleaseEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        super(Edge, self).mouseMoveEvent(event)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(Edge, self).hoverLeaveEvent(event)
        self.pen.setWidthF(self.thikness)
        self.update()

    def source_port_name(self):
        return self.source().port_name()

    def updateCurve(self, p1, p2):
        xDistance = p2.x() - p1.x()
        multiply = 3
        self.path = QtGui.QPainterPath()

        direction = QtGui.QVector2D(p1) - QtGui.QVector2D(p2)
        direction.normalize()

        self.path.moveTo(p1)
        if xDistance < 0:
            self.path.cubicTo(QtCore.QPoint(p1.x() + xDistance / -multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y()), p2)
        else:
            self.path.cubicTo(QtCore.QPoint(p1.x() + xDistance / multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / 2, p2.y()), p2)

        self.setPath(self.path)

    def destination_port_name(self):
        return self.destination().port_name()

    def setEdgeControlPoint(self, point):
        pass

    def paint(self, painter, option, widget):
        self.setPen(self.pen)
        p1, p2 = self.getEndPoints()

        xDistance = p2.x() - p1.x()
        xInpFlipEdge = 0.0
        xOutFlipEdge = 0.0
        if self.source().data_type == AGPortDataTypes.tReroute:
            xInpArr = [p.scenePos().x() for p in self.source().parentItem().inp0.affected_by]
            xInpFlipEdge = sum(xInpArr) / (float(len(xInpArr)) + 0.0001)
            painter.drawLine(xInpFlipEdge, self.source().scenePos().y(), xInpFlipEdge, self.source().scenePos().y() + 200.0)
            painter.drawText(int(xInpFlipEdge), int(self.source().scenePos().y()), str(xInpFlipEdge))
        if self.destination().data_type == AGPortDataTypes.tReroute:
            xOutArr = [p.scenePos().x() for p in self.destination().parentItem().out0.affects]
            xOutFlipEdge = sum(xOutArr) / (float(len(xOutArr)) + 0.0001)
            painter.drawLine(xOutFlipEdge, self.source().scenePos().y(), xOutFlipEdge, self.source().scenePos().y() + 200.0)
            painter.drawText(int(xOutFlipEdge), int(self.source().scenePos().y()), str(xOutFlipEdge))

        multiply = 3
        self.path = QtGui.QPainterPath()

        direction = QtGui.QVector2D(p1) - QtGui.QVector2D(p2)
        direction.normalize()

        self.path.moveTo(p1)

        if xDistance < 0:
            inpType = self.source().data_type
            cp1 = QtCore.QPoint(p1.x() + xDistance / -1.5, p1.y())
            cp2 = QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y())

            painter.drawText(cp1, "c1")
            painter.drawText(cp2, "c2")
        else:
            cp1 = QtCore.QPoint(p1.x() + xDistance / multiply, p1.y())
            cp2 = QtCore.QPoint(p2.x() - xDistance / 2, p2.y())
            painter.drawText(cp1, "c1")
            painter.drawText(cp2, "c2")

        self.path.cubicTo(cp1, cp2, p2)

        self.setPath(self.path)

        super(Edge, self).paint(painter, option, widget)
