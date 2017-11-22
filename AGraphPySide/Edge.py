from PySide import QtCore
from PySide import QtGui
from Settings import Colors
from Settings import get_line_type
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

        self.settings = self.graph().get_settings()
        self.color = self.source().color.darker(150)
        if self.settings:
            # self.color = QtGui.QColor(self.settings.value('SCENE/Edge color'))
            self.lineType = get_line_type(self.settings.value('SCENE/Edge pen type'))
            self.thikness = float(self.settings.value('SCENE/Edge line thickness'))

        if self.settings:
            self.pen = QtGui.QPen(self.color, self.thikness, self.lineType, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self.pen = QtGui.QPen(self.kConnectionLines, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])

        self.setPen(self.pen)

        self.source().port_connected()
        self.destination().port_connected()

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

    def kill(self):
        self.graph().remove_edge(self)
        self.source().port_disconnected()
        self.source().update()
        self.destination().port_disconnected()
        self.destination().update()

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
        distance = p2.x() - p1.x()
        multiply = 3
        self.path = QtGui.QPainterPath()

        self.path.moveTo(p1)
        if distance < 0:
            self.path.cubicTo(QtCore.QPoint(p1.x() + distance / -multiply, p1.y()), QtCore.QPoint(p2.x() - distance / -multiply, p2.y()), p2)
        else:
            self.path.cubicTo(QtCore.QPoint(p1.x() + distance / multiply, p1.y()), QtCore.QPoint(p2.x() - distance / 2, p2.y()), p2)

        self.setPath(self.path)

    def destination_port_name(self):
        return self.destination().port_name()

    def paint(self, painter, option, widget):
        self.setPen(self.pen)
        points = self.getEndPoints()
        self.updateCurve(points[0], points[1])
        super(Edge, self).paint(painter, option, widget)
