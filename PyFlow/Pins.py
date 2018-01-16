from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from AbstractGraph import *
from Settings import *
import nodes_res_rc
import pyrr


def updatePins(start_from):
    if not start_from.affects == []:
        start_from.update()
        for i in start_from.affects:
            i.update()
            updatePins(i)


class _Pin(QGraphicsWidget, PinBase):
    '''
    This is base class for all ui pins
    '''

    OnPinConnected = QtCore.Signal()
    OnPinDisconnected = QtCore.Signal()

    def __init__(self, name, parent, dataType, direction):
        PinBase.__init__(self, name, parent, dataType, direction)
        QGraphicsWidget.__init__(self)
        name = name.replace(" ", "_")  # spaces are not allowed
        self.setParentItem(parent)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.menu = QMenu()
        self.actionDisconnect = self.menu.addAction('Disconnect all')
        self.actionDisconnect.triggered.connect(self.disconnectAll)
        self.newPos = QtCore.QPointF()
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(2)
        self.width = 8 + 1
        self.height = 8 + 1
        self.hovered = False
        self.startPos = None
        self.endPos = None
        self.bEdgeTangentDirection = False
        self._container = None
        self._execPen = QtGui.QPen(Colors.Exec, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.pinImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False

    def color(self):
        return QtGui.QColor()

    def call(self):
        PinBase.call(self)

    def defaultValue(self):
        return None

    def kill(self):
        PinBase.kill(self)
        con = self._container
        self.disconnectAll()
        if hasattr(self.parent(), self.name):
            delattr(self.parent(), self.name)
        self.parent().graph().scene().removeItem(self._container)
        if self.direction == PinDirection.Input:
            self.parent().inputsLayout.removeItem(con)
        else:
            self.parent().outputsLayout.removeItem(con)

    def deserialize(self):
        pass

    def serialize(self):
        data = {'name': self.name,
                'dataType': self.dataType,
                'type': self.direction,
                'value': self.currentData(),
                'uuid': str(self.uid),
                'bLabelHidden': self.bLabelHidden,
                'bDirty': self.dirty
                }
        return data

    def ungrabMouseEvent(self, event):
        super(_Pin, self).ungrabMouseEvent(event)

    def get_container(self):
        return self._container

    def boundingRect(self):
        if not self.dataType == DataTypes.Exec:
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.width, self.height)

    def disconnectAll(self):
        trash = []
        for e in self.edge_list:
            if self.uid == e.destination().uid:
                trash.append(e)
            if self.uid == e.source().uid:
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
            linearGrad.setColorAt(0, self.color().darker(280))
            linearGrad.setColorAt(0.5, self.color().darker(280))
            linearGrad.setColorAt(0.65, self.color().lighter(130))
            linearGrad.setColorAt(1, self.color().lighter(70))
        else:
            linearGrad.setColorAt(0, self.color())
            linearGrad.setColorAt(1, self.color())

        if self.dirty:
            painter.setPen(self._dirty_pen)  # move to callback and use in debug mode

        if self.hovered:
            linearGrad.setColorAt(1, self.color().lighter(200))
        if self.dataType == DataTypes.Array:
            if self.pinImage:
                painter.drawImage(background_rect, self.pinImage)
            else:
                painter.setBrush(Colors.Array)
                rect = background_rect
                painter.drawRect(rect)
        elif self.dataType == DataTypes.Exec:
            if self._connected:
                painter.setBrush(QtGui.QBrush(self.color()))
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

    def getLayout(self):
        if self.direction == PinDirection.Input:
            return self.parent().inputsLayout
        else:
            return self.parent().outputsLayout

    def hoverEnterEvent(self, event):
        super(_Pin, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        self.setToolTip(str(self.dirty))
        event.accept()

    def hoverLeaveEvent(self, event):
        super(_Pin, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        PinBase.pinConnected(self, other)
        self.OnPinConnected.emit()

    def pinDisconnected(self, other):
        PinBase.pinDisconnected(self, other)
        self.OnPinDisconnected.emit()


###############################
# # Custom pins implementations
###############################


class FloatPin(_Pin):
    """doc string for FloatPin"""
    def __init__(self, name, parent, dataType, direction):
        super(FloatPin, self).__init__(name, parent, dataType, direction)

    def color(self):
        return Colors.Float

    def supportedDataTypes(self):
        return (DataTypes.Float, DataTypes.Int)

    def defaultValue(self):
        return 0.0

    def setData(self, data):
        try:
            self._data = float(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class IntPin(_Pin):
    """doc string for IntPin"""
    def __init__(self, name, parent, dataType, direction):
        super(IntPin, self).__init__(name, parent, dataType, direction)

    def color(self):
        return Colors.Int

    def supportedDataTypes(self):
        return (DataTypes.Int, DataTypes.Float)

    def defaultValue(self):
        return 0

    def setData(self, data):
        try:
            self._data = int(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class ExecPin(_Pin):
    """doc string for ExecPin"""
    def __init__(self, name, parent, dataType, direction):
        super(ExecPin, self).__init__(name, parent, dataType, direction)
        self.width = self.height = 10.0
        self.dirty = False

    def supportedDataTypes(self):
        return (DataTypes.Exec,)

    def call(self):
        super(ExecPin, self).call()
        # pass execution flow forward
        for p in [pin for pin in self.affects if pin.dataType == DataTypes.Exec]:
            p.call()
        # highlight wire
        for e in self.edge_list:
            e.highlight()

    def color(self):
        return Colors.Exec

    def defaultValue(self):
        return None

    def setData(self, data):
        pass


class AnyPin(_Pin):
    """doc string for AnyPin"""
    def __init__(self, name, parent, dataType, direction):
        super(AnyPin, self).__init__(name, parent, dataType, direction)

    def defaultValue(self):
        return None

    def supportedDataTypes(self):
        # all except reference and exec
        return tuple([i[1] for i in inspect.getmembers(DataTypes) if isinstance(i[1], int) and i[1] not in (DataTypes.Reference, DataTypes.Exec)])

    def color(self):
        return Colors.Any

    def setData(self, data):
        self._data = data
        PinBase.setData(self, data)


class StringPin(_Pin):
    """doc string for StringPin"""
    def __init__(self, name, parent, dataType, direction):
        super(StringPin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.String,)

    def color(self):
        return Colors.String

    def defaultValue(self):
        return ""

    def setData(self, data):
        try:
            self._data = str(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class ListPin(_Pin):
    """doc string for ListPin"""
    def __init__(self, name, parent, dataType, direction):
        super(ListPin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.Array,)

    def color(self):
        return Colors.Array

    def defaultValue(self):
        return []

    def setData(self, data):
        if isinstance(data, list):
            self._data = data
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class BoolPin(_Pin):
    """doc string for BoolPin"""
    def __init__(self, name, parent, dataType, direction):
        super(BoolPin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.Bool,)

    def color(self):
        return Colors.Bool

    def defaultValue(self):
        return False

    def setData(self, data):
        try:
            self._data = bool(data)
        except:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class FloatVector3Pin(_Pin):
    """doc string for FloatVector3Pin"""
    def __init__(self, name, parent, dataType, direction):
        super(FloatVector3Pin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.FloatVector3,)

    def color(self):
        return Colors.FloatVector3

    def defaultValue(self):
        return pyrr.Vector3()

    def setData(self, data):
        if isinstance(data, pyrr.Vector3):
            self._data = data
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class FloatVector4Pin(_Pin):
    """doc string for FloatVector4Pin"""
    def __init__(self, name, parent, dataType, direction):
        super(FloatVector4Pin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.FloatVector4,)

    def color(self):
        return Colors.FloatVector4

    def defaultValue(self):
        return pyrr.Vector4()

    def setData(self, data):
        if isinstance(data, pyrr.Vector4):
            self._data = data
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


class QuatPin(_Pin):
    """doc string for QuatPin"""
    def __init__(self, name, parent, dataType, direction):
        super(QuatPin, self).__init__(name, parent, dataType, direction)

    def supportedDataTypes(self):
        return (DataTypes.Quaternion,)

    def color(self):
        return Colors.Quaternion

    def defaultValue(self):
        return pyrr.Quaternion()

    def setData(self, data):
        if isinstance(data, pyrr.Quaternion):
            self._data = data
        else:
            self._data = self.defaultValue()
        PinBase.setData(self, data)


def getPinByType(name, parent, dataType, direction):
    '''
    this function will be used by node
    '''
    if dataType == DataTypes.Float:
        return FloatPin(name, parent, dataType, direction)
    if dataType == DataTypes.Int:
        return IntPin(name, parent, dataType, direction)
    if dataType == DataTypes.Exec:
        return ExecPin(name, parent, dataType, direction)
    if dataType == DataTypes.Any:
        return AnyPin(name, parent, dataType, direction)
    if dataType == DataTypes.String:
        return StringPin(name, parent, dataType, direction)
    if dataType == DataTypes.Array:
        return ListPin(name, parent, dataType, direction)
    if dataType == DataTypes.Bool:
        return BoolPin(name, parent, dataType, direction)
    if dataType == DataTypes.FloatVector3:
        return FloatVector3Pin(name, parent, dataType, direction)
    if dataType == DataTypes.FloatVector4:
        return FloatVector4Pin(name, parent, dataType, direction)
    if dataType == DataTypes.Quaternion:
        return QuatPin(name, parent, dataType, direction)

    return None
