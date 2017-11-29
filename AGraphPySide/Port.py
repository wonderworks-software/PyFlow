from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from AbstractGraph import *
from Settings import *


def update_ports(start_from):
    if not start_from.affects == []:
        start_from.update()
        for i in start_from.affects:
            i.update()
            update_ports(i)


def getPortColorByType(t):
    if t == DataTypes.Any:
        return Colors.Any
    if t == DataTypes.Float:
        return Colors.Float
    if t == DataTypes.Int:
        return Colors.Int
    if t == DataTypes.Array:
        return Colors.Array
    if t == DataTypes.Bool:
        return Colors.Bool
    if t == DataTypes.Exec:
        return Colors.Exec
    if t == DataTypes.Reroute:
        return Colors.Reroute
    if t == DataTypes.String:
        return Colors.String


class Port(QGraphicsWidget, PortBase):
    def __init__(self, name, parent, data_type, width, height, color=Colors.Connectors):
        PortBase.__init__(self, name, parent, data_type)
        QGraphicsWidget.__init__(self)
        name = name.replace(" ", "_")  # spaces are not allowed
        self.setParentItem(parent)
        self.menu = QtGui.QMenu()
        self.disconnected = self.menu.addAction('Disconnect all')
        self.disconnected.triggered.connect(self.disconnect_all)
        self.newPos = QtCore.QPointF()
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.__width = width + 1
        self.__height = height + 1
        if self.data_type == DataTypes.Exec:
            self.__width = self.__height = 10.0
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self.bEdgeTangentDirection = False
        self.options = self.parent().graph().get_settings()
        self.reroutes = []
        self._container = None
        self.color = getPortColorByType(data_type)
        self._execPen = QtGui.QPen(self.color, 0.5, QtCore.Qt.SolidLine)
        if self.data_type == DataTypes.Reroute:
            self.color = color
        self.setGeometry(0, 0, self.__width, self.__height)
        if self.options:
            opt_dirty_pen = QtGui.QColor(self.options.value('NODES/Port dirty color'))
            opt_dirty_type_name = self.options.value('NODES/Port dirty type')
            opt_port_dirty_pen_type = get_line_type(opt_dirty_type_name)
            self._dirty_pen = QtGui.QPen(opt_dirty_pen, 0.5, opt_port_dirty_pen_type, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

    def mousePressEvent(self, event):
        modifiers = QtGui.QApplication.keyboardModifiers()
        if self.hasConnections() and modifiers == QtCore.Qt.AltModifier:
            self.disconnect_all()
        super(Port, self).mousePressEvent(event)

    def ungrabMouseEvent(self, event):
        super(Port, self).ungrabMouseEvent(event)

    def get_container(self):
        return self._container

    def setEdgesControlPointsFlipped(self, bFlipped=False):
        self.bEdgeTangentDirection = bFlipped

    def getAvgXConnected(self):
        xAvg = 0.0
        if not self.hasConnections():
            return xAvg
        if self.type == PinTypes.Input:
            positions = [p.scenePos().x() for p in self.affected_by]
        else:
            positions = [p.scenePos().x() for p in self.affects]
        if not len(positions) == 0:
            xAvg = sum(positions) / len(positions)
        return xAvg

    def boundingRect(self):
        return QtCore.QRectF(0, -0.5, self.__width * 1.5, self.__height + 1.0)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.__width, self.__height)

    def disconnect_all(self):
        trash = []
        for e in self.parent().graph().edges:
            if self.port_name() == e.connection["To"]:
                trash.append(e)
            if self.port_name() == e.connection["From"]:
                trash.append(e)
        for t in trash:
            self.parent().graph().remove_edge(t)
        self.bEdgeTangentDirection = False
        self.parent().graph().write_to_console("disconnectAttr {1}an {0}".format(self.port_name(), FLAG_SYMBOL))

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        background_rect = QtCore.QRectF(0, 0, self.__width, self.__width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), self.__width / 2.5)
        if not self._connected:
            linearGrad.setColorAt(0, self.color.darker(280))
            linearGrad.setColorAt(0.5, self.color.darker(280))
            linearGrad.setColorAt(0.65, self.color.lighter(130))
            linearGrad.setColorAt(1, self.color.lighter(70))
        else:
            linearGrad.setColorAt(0, self.color)
            linearGrad.setColorAt(1, self.color)

        # if self.dirty:
        #     painter.setPen(self._dirty_pen)  # move to callback and use in debug mode

        if self.hovered:
            linearGrad.setColorAt(1, self.color.lighter(200))
        if self.data_type == DataTypes.Array:
            painter.drawRect(background_rect)
        elif self.data_type == DataTypes.Exec:
            if self._connected:
                painter.setBrush(QtGui.QBrush(self.color))
            else:
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.setPen(self._execPen)
            arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                    QtCore.QPointF(self.__width / 2.0, 0.0),
                                    QtCore.QPointF(self.__width, self.__height / 2.0),
                                    QtCore.QPointF(self.__width / 2.0, self.__height),
                                    QtCore.QPointF(0, self.__height)])
            painter.drawPolygon(arrow)
        else:
            painter.setBrush(QtGui.QBrush(linearGrad))
            painter.drawEllipse(background_rect)
            arrow = QtGui.QPolygonF([QtCore.QPointF(self.__width, self.__height * 0.7),
                                    QtCore.QPointF(self.__width * 1.15, self.__height / 2.0),
                                    QtCore.QPointF(self.__width, self.__height * 0.3),
                                    QtCore.QPointF(self.__width, self.__height * 0.7)])
            painter.drawPolygon(arrow)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def write_to_console(self, data):
        if self.parent().graph():
            self.parent().graph().write_to_console("setAttr {2}an {0} {2}v {1}".format(self.port_name(), self._data, FLAG_SYMBOL))

    def getLayout(self):
        if self.type == PinTypes.Input:
            return self.parent().inputsLayout
        else:
            return self.parent().outputsLayout

    def hoverEnterEvent(self, event):
        self.update()
        self.hovered = True
        self.setToolTip(str(self.current_data()))
        if self.parent().graph().is_debug():
            print('data -', self._data)
            self.write_to_console(self._data)
        event.accept()
        super(Port, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.update()
        self.hovered = False
        super(Port, self).hoverLeaveEvent(event)

    def set_data(self, data, dirty_propagate=True):
        PortBase.set_data(self, data, dirty_propagate)
        self.write_to_console("setAttr {2}an {0} {2}v {1}".format(self.port_name(), data, FLAG_SYMBOL))
        update_ports(self)
