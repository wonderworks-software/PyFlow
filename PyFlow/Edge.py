from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsPathItem
from Settings import Colors
from AbstractGraph import *
import weakref
from uuid import UUID, uuid4
import numpy
from Nodes import Reroute


def CatmullRomSpline(P0, P1, P2, P3, nPoints=10):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    alpha = 0.5

    def tj(ti, Pi, Pj):
        xi, yi = Pi
        xj, yj = Pj
        return (((xj - xi)**2 + (yj - yi)**2) ** 0.5) ** alpha + ti

    t0 = 0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)

    # Only calculate points between P1 and P2
    t = numpy.linspace(t1, t2, nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t), 1)
    A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
    A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
    A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3

    B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
    B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3

    C = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2
    return C


def CatmullRomChain(P):
    """
    Calculate Catmull Rom for a chain of points and return the combined curve.
    """
    sz = len(P)

    # The curve C will contain an array of (x,y) points.
    C = []
    for i in range(sz - 3):
        c = CatmullRomSpline(P[i], P[i + 1], P[i + 2], P[i + 3])
        C.extend(c)

    return C


class Edge(QGraphicsPathItem):
    def __init__(self, source, destination, graph):
        QGraphicsPathItem.__init__(self)
        self._uid = uuid4()
        self.graph = weakref.ref(graph)
        self.source = weakref.ref(source)
        self.destination = weakref.ref(destination)
        self.object_type = ObjectTypes.Connection
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)

        self.mPath = QtGui.QPainterPath()

        self.cp1 = QtCore.QPointF(0.0, 0.0)
        self.cp2 = QtCore.QPointF(0.0, 0.0)

        self.setZValue(-1)
        # self.connection = {'From': self.source().getName(),
        #                    'To': self.destination().getName()}

        self.color = self.source().color()

        self.thikness = 1
        if source.dataType == DataTypes.Exec and destination.dataType == DataTypes.Exec:
            self.thikness = 2

        self.pen = QtGui.QPen(self.color, self.thikness, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        self.setPen(self.pen)

        self.source().update()
        self.destination().update()
        self.fade = 0.0

    def setColor(self, color):
        self.pen.setColor(color)
        self.color = color

    def Tick(self):
        if self.fade > 0:
            self.pen.setWidthF(self.thikness + self.fade * 2)
            r = abs(lerp(self.color.red(), Colors.Yellow.red(), clamp(self.fade, 0, 1)))
            g = abs(lerp(self.color.green(), Colors.Yellow.green(), clamp(self.fade, 0, 1)))
            b = abs(lerp(self.color.blue(), Colors.Yellow.blue(), clamp(self.fade, 0, 1)))
            self.pen.setColor(QtGui.QColor.fromRgb(r, g, b))
            self.fade -= 0.1
            self.update()

    def highlight(self):
        self.fade = 1.0

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, value):
        if self._uid in self.graph().edges:
            self.graph().edges[value] = self.graph().edges.pop(self._uid)
            self._uid = value

    @staticmethod
    def deserialize(data, graph):
        srcUUID = UUID(data['sourceUUID'])
        dstUUID = UUID(data['destinationUUID'])
        # if srcUUID in graph.pins and dstUUID in graph.pins:
        srcPin = graph.pins[srcUUID]
        dstPin = graph.pins[dstUUID]
        edge = graph._addEdge(srcPin, dstPin)
        edge.uid = uuid.UUID(data['uuid'])

    def serialize(self):
        script = {'sourceUUID': str(self.source().uid),
                  'destinationUUID': str(self.destination().uid),
                  'sourceName': self.source().getName(),
                  'destinationName': self.destination().getName(),
                  'uuid': str(self.uid)
                  }
        return script

    def __str__(self):
        return '{0}.{1} >>> {2}.{3}'.format(self.source().parent().name,
                                            self.source().name,
                                            self.destination().parent().name,
                                            self.destination().name)

    def hoverEnterEvent(self, event):
        super(Edge, self).hoverEnterEvent(event)
        self.pen.setWidthF(self.thikness + (self.thikness / 1.5))
        self.update()

    def getEndPoints(self):
        p1 = self.source().boundingRect().center() + self.source().scenePos()
        p2 = self.destination().boundingRect().center() + self.destination().scenePos()
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
        return self.source().getName()

    def shape(self):
        qp = QtGui.QPainterPathStroker()
        qp.setWidth(10.0)
        qp.setCapStyle(QtCore.Qt.SquareCap)
        return qp.createStroke(self.path())

    def updateCurve(self, p1, p2):
        xDistance = p2.x() - p1.x()
        multiply = 3
        self.mPath = QtGui.QPainterPath()

        direction = QtGui.QVector2D(p1) - QtGui.QVector2D(p2)
        direction.normalize()

        self.mPath.moveTo(p1)
        if xDistance < 0:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / -multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y()), p2)
        else:
            self.mPath.cubicTo(QtCore.QPoint(p1.x() + xDistance / multiply, p1.y()), QtCore.QPoint(p2.x() - xDistance / 2, p2.y()), p2)

        self.setPath(self.mPath)

    def destination_port_name(self):
        return self.destination().getName()

    def paint(self, painter, option, widget):
        self.setPen(self.pen)
        p1, p2 = self.getEndPoints()

        xDistance = p2.x() - p1.x()
        vDistance = p2.y() - p1.y()

        defaultVerticalOffset = 100.0
        minimumV = min(defaultVerticalOffset, abs(vDistance))
        maximumV = max(defaultVerticalOffset, abs(vDistance))
        verticalOffset = 0.0

        multiply = 2
        self.mPath = QtGui.QPainterPath()
        self.mPath.moveTo(p1)

        if xDistance <= 0:
            if vDistance <= 0:
                # verticalOffset = -minimumV
                verticalOffset = 0
                pass
            else:
                # verticalOffset = minimumV
                verticalOffset = 0

        if xDistance < 0:
            if isinstance(self.source().parentItem(), Reroute):
                self.cp1 = self.source().parentItem().getOutControlPoint()
            else:
                self.cp1 = QtCore.QPoint(p1.x() + xDistance / -multiply, p1.y() + verticalOffset)

            if isinstance(self.destination().parentItem(), Reroute):
                self.cp2 = self.destination().parentItem().getInControlPoint()
            else:
                self.cp2 = QtCore.QPoint(p2.x() - xDistance / -multiply, p2.y() - verticalOffset)
        else:
            if isinstance(self.destination().parentItem(), Reroute):
                self.cp2 = self.destination().parentItem().getInControlPoint()
            else:
                self.cp2 = QtCore.QPoint(p2.x() - xDistance / multiply, p2.y() - verticalOffset)

            if isinstance(self.source().parentItem(), Reroute):
                self.cp1 = self.source().parentItem().getOutControlPoint()
            else:
                self.cp1 = QtCore.QPoint(p1.x() + xDistance / multiply, p1.y() + verticalOffset)

        self.mPath.cubicTo(self.cp1, self.cp2, p2)
        self.setPath(self.mPath)
        super(Edge, self).paint(painter, option, widget)
