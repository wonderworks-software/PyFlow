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

    def __init__(self, name, parent, data_type, width, height, color=Colors.kConnectors):
        QtGui.QGraphicsWidget.__init__(self)
        AGPort.__init__(self, name, parent, data_type)
        self.menu = QtGui.QMenu()
        self.disconnected = self.menu.addAction('Disconnect all')
        self.disconnected.triggered.connect(self.disconnect_all)
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.__width = width+1
        self.__height = height+1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self.options = self.parent.graph.get_settings()
        if self.options:
            self.color = QtGui.QColor(self.options.value('NODES/Port color'))
            opt_dirty_pen = QtGui.QColor(self.options.value('NODES/Port dirty color'))
            opt_dirty_type_name = QtGui.QColor(self.options.value('NODES/Port dirty type'))
            if opt_dirty_type_name == 'dot':
                opt_port_dirty_pen_type = QtCore.Qt.DotLine
            elif opt_dirty_type_name == 'solid':
                opt_port_dirty_pen_type = QtCore.Qt.SolidLine
            elif opt_dirty_type_name == 'dash':
                opt_port_dirty_pen_type = QtCore.Qt.DashLine
            elif opt_dirty_type_name == 'dashdotdot':
                opt_port_dirty_pen_type = QtCore.Qt.DashDotDotLine
            else:
                opt_port_dirty_pen_type = QtCore.Qt.DashDotLine
            self._dirty_pen = QtGui.QPen(opt_dirty_pen, 1, opt_port_dirty_pen_type, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self.color = color
            self._dirty_pen = QtGui.QPen(Colors.kDirtyPen, 1, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def boundingRect(self):

        return QtCore.QRectF(0, -0.5, self.__width, self.__height)

    def sizeHint(self, which, constraint):

        return QtCore.QSizeF(self.__width, self.__height)

    def disconnect_all(self):
        if self.parent.graph.is_debug():
            print self.edge_list
        for e in self.edge_list:
            if self.parent.graph.is_debug():
                print e, 'killed'
                self.parent.graph.write_to_console('{0} killed'.format(e.__str__()))
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

    def write_to_console(self, data):
        p = self.parent.graph.parent
        if p:
            p.console.appendPlainText(str(self._data))

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True
        if self.parent.graph.is_debug():
            print 'data -', self._data
            self.write_to_console(self._data)

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

    def set_data(self, data, dirty_propagate=True):

        AGPort.set_data(self, data, dirty_propagate)
        update_ports(self)
