from PySide import QtCore
from AbstractGraph import *
from Settings import *


def update_ports(start_from):

    if not start_from.affects == []:
        start_from.update()
        for i in start_from.affects:
            i.update()
            update_ports(i)


class Port(QtGui.QGraphicsWidget, AGPort):

    def __init__(self, name, parent, width, height, color=Colors.kConnectors):
        QtGui.QGraphicsWidget.__init__(self)
        AGPort.__init__(self, name, parent)
        self.menu = QtGui.QMenu()
        self.disconnected = self.menu.addAction('Disconnect all')
        self.get_data_action = self.menu.addAction('GET')
        self.plot_action = self.menu.addAction('PLOT GRAPH')
        self.disconnected.triggered.connect(self.disconnect_all)
        self.get_data_action.triggered.connect(self.get_data)
        self.plot_action.triggered.connect(self.parent.graph.plot)
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.color = color
        self.setZValue(2)
        self.__width = width+1
        self.__height = height+1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self._dirty_pen = QtGui.QPen(Colors.kDirtyPen, 1, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def port_name(self):

        return self.parent.name+'.'+self.name

    def disconnect_all(self):
        if self.parent.graph.is_debug():
            print self.edge_list
        for e in self.edge_list:
            if self.parent.graph.is_debug():
                print e, 'killed'
            self.parent.graph.remove_edge(e)
        if len(self.edge_list):
            self.disconnect_all()

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):

        background_rect = self.boundingRect()
        if self.dirty:
            painter.setPen(self._dirty_pen)
        if self.hovered:
            painter.setBrush(QtGui.QBrush(self.color.lighter(160)))
        else:
            painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(background_rect)

    def contextMenuEvent(self, event):

        self.menu.exec_(event.screenPos())

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True
        if self.parent.graph.is_debug():
            print 'data -', self._data

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

    def set_data(self, data, dirty_propagate=True):
        AGPort.set_data(self, data, dirty_propagate)
        update_ports(self)
