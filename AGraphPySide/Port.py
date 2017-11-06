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
        AGPort.__init__(self, name, parent, data_type)
        QtGui.QGraphicsWidget.__init__(self)
        name = name.replace(" ", "_")  # spaces are not allowed
        self.setParentItem(parent)
        self.menu = QtGui.QMenu()
        self.disconnected = self.menu.addAction('Disconnect all')
        self.disconnected.triggered.connect(self.disconnect_all)
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.__width = width + 1
        self.__height = height + 1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self.options = self.parent().graph().get_settings()
        self.reroutes = []
        if self.options:
            self.color = color
            opt_dirty_pen = QtGui.QColor(self.options.value('NODES/Port dirty color'))
            opt_dirty_type_name = self.options.value('NODES/Port dirty type')
            opt_port_dirty_pen_type = get_line_type(opt_dirty_type_name)
            self._dirty_pen = QtGui.QPen(opt_dirty_pen, 0.5, opt_port_dirty_pen_type, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self.color = color
            self._dirty_pen = QtGui.QPen(Colors.kDirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def boundingRect(self):
        return QtCore.QRectF(0, -0.5, self.__width * 1.5, self.__height)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.__width, self.__height)

    def disconnect_all(self):
        if self.parent().graph().is_debug():
            print(self.edge_list)
        for e in self.edge_list:
            self.parent().graph().write_to_console('{0} killed'.format(e.__str__()))
            e.kill()
        if not len(self.edge_list) == 0:
            self.disconnect_all()

        self.kill_reroutes()
        if self.type == AGPortTypes.kInput:
            for p in self.affected_by:
                p.kill_reroutes()

        self.parent().graph().write_to_console("disconnectAttr {1}an {0}".format(self.port_name(), FLAG_SYMBOL))

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def kill_reroutes(self):
        for r in self.reroutes:
            r.kill()

    def paint(self, painter, option, widget):

        background_rect = self.boundingRect()
        background_rect.setWidth(self.__width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2 - 0.5

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), self.__width / 2.5)
        linearGrad.setColorAt(0, self.color.darker(400))
        linearGrad.setColorAt(0.5, self.color.darker(400))
        linearGrad.setColorAt(0.65, self.color.lighter(130))
        linearGrad.setColorAt(1, self.color.lighter(70))

        # if self.dirty:
        #     painter.setPen(self._dirty_pen)  # move to callback and use in debug mode

        if self.hovered:
            linearGrad.setColorAt(1, self.color.lighter(200))
        else:
            painter.setBrush(QtGui.QBrush(self.color))
        if self.data_type == AGPortDataTypes.tArray:
            painter.drawRect(background_rect)
        else:
            painter.setBrush(linearGrad)
            painter.drawEllipse(background_rect)
            arrHeight = -0.4
            arrow = QtGui.QPolygonF([QtCore.QPointF(self.__width, self.__height * 0.7 + arrHeight),
                                    QtCore.QPointF(self.__width * 1.2, self.__height / 2.0 + arrHeight),
                                    QtCore.QPointF(self.__width, self.__height * 0.3 + arrHeight),
                                    QtCore.QPointF(self.__width, self.__height * 0.7 + arrHeight)])
            painter.drawPolygon(arrow)

    def contextMenuEvent(self, event):

        self.menu.exec_(event.screenPos())

    def write_to_console(self, data):
        if self.parent().graph():
            self.parent().graph().write_to_console("setAttr {2}an {0} {2}v {1}".format(self.port_name(), self._data, FLAG_SYMBOL))

    def getLayout(self):
        if self.type == AGPortTypes.kInput:
            return self.parent().inputsLayout
        else:
            return self.parent().outputsLayout

    def hoverEnterEvent(self, *args, **kwargs):

        self.update()
        self.hovered = True
        if self.parent().graph().is_debug():
            print('data -', self._data)
            self.write_to_console(self._data)

    def hoverLeaveEvent(self, *args, **kwargs):

        self.update()
        self.hovered = False

    def set_data(self, data, dirty_propagate=True):

        AGPort.set_data(self, data, dirty_propagate)
        self.write_to_console("setAttr {2}an {0} {2}v {1}".format(self.port_name(), data, FLAG_SYMBOL))
        update_ports(self)
