"""@file Pin.py
"""
import weakref

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QInputDialog

from PyFlow.Core.AGraphCommon import *
from PyFlow.UI.Settings import *


UI_PINS_FACTORIES = {}


class UIPinBase(QGraphicsWidget):
    '''
    Pin ui wrapper
    '''

    ## Event called when pin is connected
    OnPinConnected = QtCore.Signal(object)
    ## Event called when pin is disconnected
    OnPinDisconnected = QtCore.Signal(object)
    ## Event called when data been set
    dataBeenSet = QtCore.Signal(object)
    ## Event called when pin name changes
    nameChanged = QtCore.Signal(str)
    ## Event called when pin name changes
    displayNameChanged = QtCore.Signal(str)
    ## Event called when setUserStruct called
    # used by enums
    userStructChanged = QtCore.Signal(object)
    OnPinChanged = QtCore.Signal(object)

    def __init__(self, owningNode, raw_pin):
        super(UIPinBase, self).__init__()
        self._rawPin = raw_pin
        self._rawPin.setWrapper(self)
        self.setParentItem(owningNode)
        self.UiNode = owningNode
        # self.setCursor(QtCore.Qt.CrossCursor)
        ## context menu for pin
        self.menu = QMenu()
        ## Disconnect all connections
        self.actionDisconnect = self.menu.addAction('Disconnect all')
        self.actionDisconnect.triggered.connect(self.disconnectAll)
        ## Copy UUID to buffer
        self.actionCopyUid = self.menu.addAction('Copy uid')
        self.actionCopyUid.triggered.connect(self.saveUidToClipboard)

        # label item weak ref
        self._label = None

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
        self._execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
        self.setGeometry(0, 0, self.width, self.height)
        self._dirty_pen = QtGui.QPen(Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.pinImage = QtGui.QImage(':/icons/resources/array.png')
        self.bLabelHidden = False
        self.bAnimate = False
        self._val = 0
        self._displayName = self.name
        self._color = QtGui.QColor(*self._rawPin.color())

    def setLabel(self, labelItem):
        if self._label is None:
            self._label = weakref.ref(labelItem)

    def getLabel(self):
        assert(self._label is not None)
        return self._label

    def displayName(self):
        return self._displayName

    def setDisplayName(self, displayName):
        self._displayName = displayName
        self.displayNameChanged.emit(self._displayName)

    @property
    def owningNode(self):
        return self._rawPin.owningNode

    @property
    def constraint(self):
        return self._rawPin.constraint
    @property
    def isAny(self):
        return self._rawPin.isAny
    
    def setRenamingEnabled(self, bEnabled):
        self._rawPin.setRenamingEnabled(bEnabled)
        actionsNames = [a.text() for a in self.menu.actions()]
        if bEnabled and "Rename" not in actionsNames:
            renameAction = self.menu.addAction("Rename")
            renameAction.triggered.connect(self.onRename)

    def canBeRenamed(self):
        return self._rawPin.canBeRenamed()

    def onRename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.setName(name)
            self.setDisplayName(name)

    def setDynamic(self, bDynamic):
        self._rawPin.setDynamic(bDynamic)
        actionsNames = [a.text() for a in self.menu.actions()]
        if bDynamic and "Remove" not in actionsNames:
            removeAction = self.menu.addAction("Remove")
            removeAction.triggered.connect(self.kill)

    def isDynamic(self):
        return self._rawPin.isDynamic()

    @property
    def dirty(self):
        return self._rawPin.dirty

    @dirty.setter
    def dirty(self, value):
        self._rawPin.dirty = value

    def defaultValue(self):
        return self._rawPin.defaultValue()

    def getUserStruct(self):
        return self._rawPin.getUserStruct()

    def currentData(self):
        return self._rawPin.currentData()

    @property
    def name(self):
        return self._rawPin.name

    def getName(self):
        return self._rawPin.getName()

    def hasConnections(self):
        return self._rawPin.hasConnections()

    def setClean(self):
        self._rawPin.setClean()

    def setDirty(self):
        self._rawPin.setDirty()

    @property
    def _data(self):
        return self._rawPin._data

    @_data.setter
    def _data(self, value):
        self._rawPin._data = value

    @property
    def affects(self):
        return self._rawPin.affects

    @property
    def direction(self):
        return self._rawPin.direction

    @property
    def affected_by(self):
        return self._rawPin.affected_by

    def supportedDataTypes(self):
        return self._rawPin.supportedDataTypes()

    @property
    def edge_list(self):
        return self._rawPin.edge_list

    @property
    def uid(self):
        return self._rawPin._uid

    @uid.setter
    def uid(self, value):
        self.owningNode().graph().pins[value] = self.owningNode().graph().pins.pop(self._rawPin._uid)
        self._rawPin._uid = value

    def color(self):
        return self._color

    def setUserStruct(self, inStruct):
        self._rawPin.setUserStruct(inStruct)
        self.userStructChanged.emit(inStruct)

    def setName(self, newName):
        self._rawPin.setName(newName)
        self.nameChanged.emit(newName)

    def setData(self, value):
        self._rawPin.setData(value)
        self.dataBeenSet.emit(value)

    def getData(self):
        return self._rawPin.getData()

    def highlight(self):
        # TODO: draw svg arrow instead
        self.bAnimate = True
        t = QtCore.QTimeLine(900, self)
        t.setFrameRange(0, 100)
        t.frameChanged[int].connect(self.animFrameChanged)
        t.finished.connect(self.animationFinished)
        t.start()

    def animFrameChanged(self, value):
        self.width = clamp(math.sin(self._val) * 9, 4.5, 25)
        self.update()
        self._val += 0.1

    def animationFinished(self):
        self.width = 9
        self.update()
        self._val = 0

    def call(self):
        self._rawPin.call()
        for e in self.edge_list:
            e.highlight()

    def kill(self):
        self.disconnectAll()
        if hasattr(self.owningNode(), self.name):
            delattr(self.owningNode(), self.name)
        if self._container is not None:
            self.owningNode().getWrapper()().graph().scene().removeItem(self._container)
            if self._rawPin.direction == PinDirection.Input:
                self.owningNode().getWrapper()().inputsLayout.removeItem(self._container)
            else:
                self.owningNode().getWrapper()().outputsLayout.removeItem(self._container)
        self._rawPin.kill()
        self.owningNode().getWrapper()().updateNodeShape()

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
        data = self._rawPin.serialize()
        data['bLabelHidden'] = self.bLabelHidden
        data['displayName'] = self.displayName()
        return data

    def ungrabMouseEvent(self, event):
        super(UIPinBase, self).ungrabMouseEvent(event)

    def get_container(self):
        return self._container

    @property
    def dataType(self):
        return self._rawPin._dataType

    @dataType.setter
    def dataType(self, value):
        self._rawPin._dataType = value

    def boundingRect(self):
        if not self.dataType == 'ExecPin':
            return QtCore.QRectF(0, -0.5, 8 * 1.5, 8 + 1.0)
        else:
            return QtCore.QRectF(0, -0.5, 10 * 1.5, 10 + 1.0)

    def sizeHint(self, which, constraint):
        try:
            return QtCore.QSizeF(self.width, self.height)
        except:
            return QGraphicsWidget.sizeHint(self, which, constraint)

    def saveUidToClipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(str(self.uid))

    def disconnectAll(self):
        trash = self._rawPin.disconnectAll()
        for e in trash:
            self.owningNode().graph().removeEdge(e)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        background_rect = QtCore.QRectF(0, 0, self.width, self.width)

        w = background_rect.width() / 2
        h = background_rect.height() / 2

        linearGrad = QtGui.QRadialGradient(QtCore.QPointF(w, h), self.width / 2.5)
        if not self._rawPin._connected:
            linearGrad.setColorAt(0, self.color().darker(280))
            linearGrad.setColorAt(0.5, self.color().darker(280))
            linearGrad.setColorAt(0.65, self.color().lighter(130))
            linearGrad.setColorAt(1, self.color().lighter(70))
        else:
            linearGrad.setColorAt(0, self.color())
            linearGrad.setColorAt(1, self.color())

        if self.hovered:
            linearGrad.setColorAt(1, self.color().lighter(200))
        if self.dataType == 'ListPin':
            if self.pinImage:
                painter.drawImage(background_rect, self.pinImage)
            else:
                painter.setBrush(Colors.Array)
                rect = background_rect
                painter.drawRect(rect)
        elif self.dataType == 'ExecPin':
            painter.setPen(self._execPen)
            if self._rawPin._connected:
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
            rect = background_rect.setX(background_rect.x())
            painter.drawEllipse(background_rect)

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    def getLayout(self):
        if self.direction == PinDirection.Input:
            return self.owningNode().inputsLayout
        else:
            return self.owningNode().outputsLayout

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}".format(str(self._rawPin.currentData()), self._rawPin.dirty)
        self.setToolTip(hoverMessage)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(UIPinBase, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        self._rawPin.pinConnected(other)
        self.OnPinConnected.emit(other)
        self.update()

    def pinDisconnected(self, other):
        self._rawPin.pinDisconnected(other)
        self.OnPinDisconnected.emit(other)
        self.update()


def REGISTER_UI_PIN_FACTORY(packageName, factory):
    if packageName not in UI_PINS_FACTORIES:
        UI_PINS_FACTORIES[packageName] = factory
        print("registering", packageName, "ui pins")


def getUIPinInstance(owningNode, raw_instance):
    packageName = raw_instance.packageName()
    instance = None
    if packageName in UI_PINS_FACTORIES:
        instance = UI_PINS_FACTORIES[packageName](owningNode, raw_instance)
    assert(instance is not None)
    return instance
