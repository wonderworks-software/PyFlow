"""@file Pin.py
"""
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from AbstractGraph import *
from Settings import *


class PinWidgetBase(QGraphicsWidget, PinBase):
    '''
    This is base class for all ui pins
    '''

    OnPinConnected = QtCore.Signal(object)
    OnPinDisconnected = QtCore.Signal(object)
    dataBeenSet = QtCore.Signal(object)
    nameChanged = QtCore.Signal(str)

    def __init__(self, name, parent, dataType, direction, **kwargs):
        QGraphicsWidget.__init__(self)
        PinBase.__init__(self, name, parent, dataType, direction, **kwargs)
        self.setParentItem(parent)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.menu = QMenu()
        self.actionDisconnect = self.menu.addAction('disconnect all')
        self.actionDisconnect.triggered.connect(self.disconnectAll)
        self.actionCopyUid = self.menu.addAction('copy uid')
        self.actionCopyUid.triggered.connect(self.saveUidToClipboard)
        self.actionCall = self.menu.addAction('execute')
        self.actionCall.triggered.connect(self.call)
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
        self._container = None
        self._execPen = QtGui.QPen(Colors.Exec, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.pinImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False
        self.bAnimate = False
        self.val = 0
        self.setData(self.defaultValue())

    def setName(self, newName):
        super(PinWidgetBase, self).setName(newName)
        self.nameChanged.emit(newName)

    def setData(self, value):
        PinBase.setData(self, value)
        self.dataBeenSet.emit(value)

    def highlight(self):
        self.bAnimate = True
        t = QtCore.QTimeLine(900, self)
        t.setFrameRange(0, 100)
        t.frameChanged[int].connect(self.animFrameChanged)
        t.finished.connect(self.animationFinished)
        t.start()

    def animFrameChanged(self, value):
        self.width = clamp(math.sin(self.val) * 9, 4.5, 25)
        self.update()
        self.val += 0.1

    def animationFinished(self):
        self.width = 9
        self.update()
        self.val = 0

    @staticmethod
    def color():
        return QtGui.QColor()

    def call(self):
        PinBase.call(self)

    def kill(self):
        PinBase.kill(self)
        self.disconnectAll()
        if hasattr(self.parent(), self.name):
            delattr(self.parent(), self.name)
        if self._container is not None:
            self.parent().graph().scene().removeItem(self._container)
            if self.direction == PinDirection.Input:
                self.parent().inputsLayout.removeItem(self._container)
            else:
                self.parent().outputsLayout.removeItem(self._container)

    @staticmethod
    def deserialize(owningNode, jsonData):
        name = jsonData['name']
        dataType = jsonData['dataType']
        direction = jsonData['direction']
        value = jsonData['value']
        uid = uuid.UUID(jsonData['uuid'])
        bLabelHidden = jsonData['bLabelHidden']
        bDirty = jsonData['bDirty']

        p = None
        if direction == PinDirection.Input:
            p = owningNode.addInputPin(name, dataType, hideLabel=bLabelHidden)
            p.uid = uid
        else:
            p = owningNode.addOutputPin(name, dataType, hideLabel=bLabelHidden)
            p.uid = uid

        p.setData(value)
        return p

    def serialize(self):
        data = PinBase.serialize(self)
        data['bLabelHidden'] = self.bLabelHidden
        return data

    def ungrabMouseEvent(self, event):
        super(PinWidgetBase, self).ungrabMouseEvent(event)

    def get_container(self):
        return self._container

    def boundingRect(self):
        if not self.dataType == DataTypes.Exec:
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        return QtCore.QSizeF(self.width, self.height)

    def saveUidToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(str(self.uid))

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
            painter.setPen(self._execPen)
            if self._connected:
                painter.setBrush(QtGui.QBrush(self.color()))
            else:
                painter.setBrush(QtCore.Qt.NoBrush)
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
        super(PinWidgetBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        self.setToolTip(str(self.currentData()))
        event.accept()

    def hoverLeaveEvent(self, event):
        super(PinWidgetBase, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        PinBase.pinConnected(self, other)
        self.OnPinConnected.emit(other)

    def pinDisconnected(self, other):
        PinBase.pinDisconnected(self, other)
        self.OnPinDisconnected.emit(other)
