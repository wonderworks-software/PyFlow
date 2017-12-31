from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from AbstractGraph import *
from Settings import *
import nodes_res_rc


def updatePins(start_from):
    if not start_from.affects == []:
        start_from.update()
        for i in start_from.affects:
            i.update()
            updatePins(i)


class Pin(QGraphicsWidget, PinBase):

    OnDataChanged = QtCore.Signal(object)
    OnPinConnected = QtCore.Signal()
    OnPinDisconnected = QtCore.Signal()

    def __init__(self, name, parent, dataType, width=8.0, height=8.0, color=Colors.Connectors):
        PinBase.__init__(self, name, parent, dataType)
        QGraphicsWidget.__init__(self)
        name = name.replace(" ", "_")  # spaces are not allowed
        self.setParentItem(parent)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.menu = QMenu()
        self.disconnected = self.menu.addAction('Disconnect all')
        self.disconnected.triggered.connect(self.disconnectAll)
        self.newPos = QtCore.QPointF()
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.width = width + 1
        self.height = height + 1
        if self.dataType == DataTypes.Exec:
            self.width = self.height = 10.0
            self.dirty = False
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self.bEdgeTangentDirection = False
        self.options = self.parent().graph().getSettings()
        self._container = None
        self.color = getPortColorByType(dataType)
        if dataType == DataTypes.Reference:
            self.color = getPortColorByType(dataType.dataType)
        self._execPen = QtGui.QPen(self.color, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        if self.options:
            opt_dirty_pen = QtGui.QColor(self.options.value('NODES/Pin dirty color'))
            opt_dirty_type_name = self.options.value('NODES/Pin dirty type')
            opt_port_dirty_pen_type = get_line_type(opt_dirty_type_name)
            self._dirty_pen = QtGui.QPen(opt_dirty_pen, 0.5, opt_port_dirty_pen_type, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
        else:
            self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.portImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False

    def setData(self, data):
        PinBase.setData(self, data)
        self.OnDataChanged.emit(data)

    def kill(self):
        PinBase.kill(self)
        con = self._container
        self.disconnectAll()
        if hasattr(self.parent(), self.name):
            delattr(self.parent(), self.name)
        self.parent().graph().scene().removeItem(self._container)
        if self.type == PinTypes.Input:
            self.parent().inputsLayout.removeItem(con)
        else:
            self.parent().outputsLayout.removeItem(con)

    def serialize(self):
        data = {'name': self.name,
                'dataType': self.dataType,
                'type': self.type,
                'value': self.currentData(),
                'uuid': str(self.uid),
                'bLabelHidden': self.bLabelHidden,
                'bDirty': self.dirty
                }
        return data

    def ungrabMouseEvent(self, event):
        super(Pin, self).ungrabMouseEvent(event)

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
        if not self.dataType == DataTypes.Exec:
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.width, self.height)

    def disconnectAll(self):
        trash = []
        for e in self.parent().graph().edges.values():
            if self.uid == e.destination().uid:
                trash.append(e)
            if self.pinName() == e.source().uid:
                trash.append(e)
        for e in trash:
            self.parent().graph().removeEdge(e)
        self.bEdgeTangentDirection = False

    def shape(self):

        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        background_rect = QtCore.QRectF(0, 0, self.width, self.width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), self.width / 2.5)
        if not self._connected:
            linearGrad.setColorAt(0, self.color.darker(280))
            linearGrad.setColorAt(0.5, self.color.darker(280))
            linearGrad.setColorAt(0.65, self.color.lighter(130))
            linearGrad.setColorAt(1, self.color.lighter(70))
        else:
            linearGrad.setColorAt(0, self.color)
            linearGrad.setColorAt(1, self.color)

        if self.dirty:
            painter.setPen(self._dirty_pen)  # move to callback and use in debug mode

        if self.hovered:
            linearGrad.setColorAt(1, self.color.lighter(200))
        if self.dataType == DataTypes.Array:
            if self.portImage:
                painter.drawImage(background_rect, self.portImage)
            else:
                painter.setBrush(Colors.Array)
                rect = background_rect
                painter.drawRect(rect)
        elif self.dataType == DataTypes.Exec:
            if self._connected:
                painter.setBrush(QtGui.QBrush(self.color))
            else:
                painter.setBrush(QtCore.Qt.NoBrush)
                painter.setPen(self._execPen)
            arrow = QtGui.QPolygonF([QtCore.QPointF(0.0, 0.0),
                                    QtCore.QPointF(self.width / 2.0, 0.0),
                                    QtCore.QPointF(self.width, self.height / 2.0),
                                    QtCore.QPointF(self.width / 2.0, self.height),
                                    QtCore.QPointF(0, self.height)])
            painter.drawPolygon(arrow)
        else:
            painter.setBrush(QtGui.QBrush(linearGrad))
            painter.drawEllipse(background_rect)
            arrow = QtGui.QPolygonF([QtCore.QPointF(self.width, self.height * 0.7),
                                    QtCore.QPointF(self.width * 1.15, self.height / 2.0),
                                    QtCore.QPointF(self.width, self.height * 0.3),
                                    QtCore.QPointF(self.width, self.height * 0.7)])
            painter.drawPolygon(arrow)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def writeToConsole(self, data):
        if self.parent().graph():
            self.parent().graph().writeToConsole(str(data))

    def getLayout(self):
        if self.type == PinTypes.Input:
            return self.parent().inputsLayout
        else:
            return self.parent().outputsLayout

    def hoverEnterEvent(self, event):
        super(Pin, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        self.setToolTip(str(self.currentData()))
        event.accept()

    def hoverLeaveEvent(self, event):
        super(Pin, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        PinBase.pinConnected(self, other)
        self.OnPinConnected.emit()

    def pinDisconnected(self, other):
        PinBase.pinDisconnected(self, other)
        self.OnPinDisconnected.emit()

    def setData(self, data):
        PinBase.setData(self, data)
        updatePins(self)
