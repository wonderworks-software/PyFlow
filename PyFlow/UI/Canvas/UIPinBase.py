import weakref

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsWidget
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QSizePolicy

from PyFlow.Core.Common import *
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.Painters import PinPainter
from PyFlow.UI.Canvas.UICommon import *


UI_PINS_FACTORIES = {}

headerBtnStyle = """
QPushButton {
    background-color: rgb(55, 55, 55);
    border-style: outset;
    border-radius: 1px;
    border-width: 1px;
    padding: 0px;
    margin: 0px;
    font-size: 8px;
    font-family: "Consolas";
    color: white;
}
"""


class UIPinBase(QGraphicsWidget):
    """UI pin wrapper.
    """

    # Event called when pin is connected
    OnPinConnected = QtCore.Signal(object)
    # Event called when pin is disconnected
    OnPinDisconnected = QtCore.Signal(object)
    # Event called when data been set
    dataBeenSet = QtCore.Signal(object)
    # Event called when pin name changes
    displayNameChanged = QtCore.Signal(str)
    OnPinChanged = QtCore.Signal(object)
    OnPinDeleted = QtCore.Signal(object)

    def __init__(self, owningNode, raw_pin):
        """UI wrapper for :class:`PyFlow.Core.PinBase`

        :param owningNode: Owning node
        :type owningNode: :class:`PyFlow.UI.Canvas.NodeBase`
        :param raw_pin: PinBase reference
        :type raw_pin: :class:`PyFlow.Core.PinBase`
        """

        super(UIPinBase, self).__init__()
        self.setGraphicsItem(self)
        self.setFlag(QGraphicsWidget.ItemSendsGeometryChanges)
        self.setCacheMode(self.DeviceCoordinateCache)
        self.setAcceptHoverEvents(True)
        self.setZValue(1)
        self.setParentItem(owningNode)

        self.UiNode = weakref.ref(owningNode)
        self._rawPin = raw_pin
        if self._rawPin is not None:
            self._rawPin.serializationHook.connect(self.serializationHook)
            self._rawPin.containerTypeChanged.connect(
                self.onContainerTypeChanged)
            self._displayName = self._rawPin.name
            self._rawPin.setWrapper(self)
            self._rawPin.killed.connect(self.kill)
            self._rawPin.nameChanged.connect(self.setDisplayName)

            # Context menu for pin
            self.menu = QMenu()
            self.menu.addAction("Rename").triggered.connect(self.onRename)
            self.menu.addAction("Remove").triggered.connect(self._rawPin.kill)
            self.actionDisconnect = self.menu.addAction('Disconnect all')
            self.actionDisconnect.triggered.connect(self._rawPin.disconnectAll)
            self.actionResetValue = self.menu.addAction("Reset value")
            self.actionResetValue.triggered.connect(self.resetToDefault)
            if self._rawPin._structure == PinStructure.Multi:
                self.menu.addAction("changeStructure").triggered.connect(
                    self.selectStructure)

        # GUI
        self._font = QtGui.QFont("Consolas")
        self._font.setPointSize(6)
        self.pinSize = 6
        self.hovered = False
        self.bLabelHidden = False
        if self._rawPin is not None:
            self._pinColor = QtGui.QColor(*self._rawPin.color())
        self._labelColor = QtCore.Qt.white
        self._execPen = QtGui.QPen(Colors.White, 0.5, QtCore.Qt.SolidLine)
        self._dirty_pen = QtGui.QPen(
            Colors.DirtyPen, 0.5, QtCore.Qt.DashLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)

        self.uiConnectionList = []

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.pinCircleDrawOffset = QtCore.QPointF()

    @property
    def inputWidgetVariant(self):
        return self._rawPin.inputWidgetVariant

    @property
    def labelColor(self):
        return self._labelColor

    @labelColor.setter
    def labelColor(self, value):
        self._labelColor = value

    def pinCenter(self):
        """Point relative to pin widget, where circle is drawn."""

        frame = QtCore.QRectF(QtCore.QPointF(0, 0), self.geometry().size())
        halfPinSize = self.pinSize / 2
        pinX = self.pinSize
        pinY = (frame.height() / 2)
        if not self.bLabelHidden:
            if self.direction == PinDirection.Output:
                pinX = frame.width() - self.pinSize + halfPinSize
        result = QtCore.QPointF(pinX, pinY)
        if self.owningNode().collapsed:
            labelHeight = self.owningNode().labelHeight
            #labelHeight += self.owningNode().nodeLayout.spacing()
            if self.direction == PinDirection.Input:
                result = self.mapFromItem(
                    self.owningNode(), QtCore.QPointF(0, labelHeight))
            if self.direction == PinDirection.Output:
                result = self.mapFromItem(self.owningNode(), QtCore.QPointF(
                    self.owningNode().sizeHint(None, None).width(), labelHeight))
        return result

    def onContainerTypeChanged(self, *args, **kwargs):
        # underlined pin is changed to list or dict
        # update to redraw shape
        self.update()

    def setLabel(self, labelItem):
        if self._label is None:
            self._label = weakref.ref(labelItem)

    def displayName(self):
        return self._displayName

    def setDisplayName(self, displayName):
        if displayName != self._displayName:
            self._displayName = displayName
            self.displayNameChanged.emit(self._displayName)
            self.prepareGeometryChange()
            self.updateGeometry()
            self.update()

    def jsonEncoderClass(self):
        return self._rawPin.jsonEncoderClass()

    def jsonDecoderClass(self):
        return self._rawPin.jsonDecoderClass()

    @property
    def owningNode(self):
        return self.UiNode

    @property
    def constraint(self):
        return self._rawPin.constraint

    @property
    def isAny(self):
        return self._rawPin.isAny()

    def setMenuItemEnabled(self, actionName, bEnabled):
        for action in self.menu.actions():
            if action.text() == actionName:
                if bEnabled != action.isEnabled() and action.isVisible():
                    action.setEnabled(bEnabled)
                    action.setVisible(bEnabled)

    def syncRenamable(self):
        renamingEnabled = self._rawPin.optionEnabled(
            PinOptions.RenamingEnabled)
        # self._label()._isEditable = renamingEnabled
        self.setMenuItemEnabled("Rename", renamingEnabled)

    def onRename(self):
        name, confirmed = QInputDialog.getText(
            None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            uniqueName = self._rawPin.owningNode().getUniqPinName(name)
            self.setName(uniqueName)
            self.setDisplayName(uniqueName)
            self.owningNode().invalidateNodeLayouts()
            self.owningNode().updateNodeShape()

    def syncDynamic(self):
        self.setMenuItemEnabled(
            "Remove", self._rawPin.optionEnabled(PinOptions.Dynamic))

    @property
    def structureType(self):
        return self._rawPin.structureType

    @property
    def dirty(self):
        return self._rawPin.dirty

    @dirty.setter
    def dirty(self, value):
        self._rawPin.dirty = value

    def resetToDefault(self):
        self.setData(self.defaultValue())

    def defaultValue(self):
        return self._rawPin.defaultValue()

    def currentData(self):
        return self._rawPin.currentData()

    @property
    def name(self):
        return self._rawPin.name

    def getFullName(self):
        return self._rawPin.getFullName()

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
    def connections(self):
        return self.uiConnectionList

    @property
    def uid(self):
        return self._rawPin._uid

    @uid.setter
    def uid(self, value):
        self._rawPin._uid = value

    def color(self):
        return self._pinColor

    def setName(self, newName, force=False):
        return self._rawPin.setName(newName, force=force)

    def setData(self, value):
        self._rawPin.setData(value)
        self.dataBeenSet.emit(value)

    def getData(self):
        return self._rawPin.getData()

    def call(self):
        self._rawPin.call()

    def kill(self, *args, **kwargs):
        """this will be called after raw pin is deleted
        """
        scene = self.scene()
        if scene is None:
            del self
            return

        if self._rawPin.direction == PinDirection.Input:
            self.owningNode().inputsLayout.removeItem(self)
        else:
            self.owningNode().outputsLayout.removeItem(self)

        self.OnPinDeleted.emit(self)
        try:
            scene = self.scene()
            if scene is None:
                del self
                return
            scene.removeItem(self)
            self.owningNode().updateNodeShape()
        except:
            pass

    def assignRawPin(self, rawPin):
        if rawPin is not self._rawPin:
            self._rawPin = rawPin
            self.call = rawPin.call
            self._rawPin.setWrapper(self)
            self._pinColor = QtGui.QColor(*self._rawPin.color())

    def serializationHook(self, *args, **kwargs):
        data = {}
        data['bLabelHidden'] = self.bLabelHidden
        data['displayName'] = self.displayName()
        return data

    def serialize(self):
        return self._rawPin.serialize()

    def getContainer(self):
        return self._container

    def isExec(self):
        return self._rawPin.isExec()

    @property
    def dataType(self):
        return self._rawPin.dataType

    def sizeHint(self, which, constraint):
        height = QtGui.QFontMetrics(self._font).height()
        width = self.pinSize * 2
        if not self.bLabelHidden:
            width += QtGui.QFontMetrics(self._font).width(self.displayName())
        return QtCore.QSizeF(width, height)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def isArray(self):
        return self._rawPin.isArray()

    def isDict(self):
        return self._rawPin.isDict()

    def paint(self, painter, option, widget):
        if self.isArray():
            PinPainter.asArrayPin(self, painter, option, widget)
        elif self.isDict():
            PinPainter.asDictPin(self, painter, option, widget)
        else:
            PinPainter.asValuePin(self, painter, option, widget)

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
        supportedTypes = self._rawPin.allowedDataTypes(
            [], self._rawPin._supportedDataTypes)
        hoverMessage = "Data: {0}\r\nDirty: {1}\r\nAllowed Types: {2}\nStructure: {3}".format(str(
            self._rawPin.currentData()), self._rawPin.dirty, supportedTypes, str(self._rawPin.getCurrentStructure()))
        self.setToolTip(hoverMessage)
        event.accept()

    def hoverLeaveEvent(self, event):
        super(UIPinBase, self).hoverLeaveEvent(event)
        self.update()
        self.hovered = False

    def pinConnected(self, other):
        self.OnPinConnected.emit(other)
        self.update()

    def pinDisconnected(self, other):
        self.OnPinDisconnected.emit(other)
        self.update()

    def selectStructure(self):
        item, ok = QInputDialog.getItem(
            None, "", "", ([i.name for i in list(PinStructure)]), 0, False)
        if ok and item:
            self._rawPin.changeStructure(PinStructure[item], True)


class PinGroup(UIPinBase):
    """docstring for PinGroup."""

    def __init__(self, owningNode, direction, name="groupName"):
        self._name = name
        self._direction = direction
        super(PinGroup, self).__init__(owningNode, None)
        self.expanded = True
        self._pins = list()

    def numPins(self):
        return len(self._pins)

    def kill(self):
        scene = self.scene()
        if scene is None:
            del self
            return

        if self._direction == PinDirection.Input:
            self.owningNode().inputsLayout.removeItem(self)
            self.owningNode().groups["input"].pop(self.name)
        else:
            self.owningNode().outputsLayout.removeItem(self)
            self.owningNode().groups["output"].pop(self.name)

        # self.OnPinDeleted.emit(self)
        try:
            scene = self.scene()
            if scene is None:
                del self
                return
            scene.removeItem(self)
            self.owningNode().updateNodeShape()
        except:
            pass

    def setExpanded(self, expanded):
        self.expanded = expanded
        for pin in self._pins:
            pin.setVisible(self.expanded)
            if pin.direction == PinDirection.Input:
                for wire in pin.uiConnectionList:
                    if expanded:
                        wire.destinationPositionOverride = None
                    else:
                        wire.destinationPositionOverride = lambda: self.scenePos() + QtCore.QPointF(0,
                                                                                                    self.geometry().height())

            if pin.direction == PinDirection.Output:
                for wire in pin.uiConnectionList:
                    if expanded:
                        wire.sourcePositionOverride = None
                    else:
                        wire.sourcePositionOverride = lambda: self.scenePos(
                        ) + QtCore.QPointF(self.geometry().width(), self.geometry().height())

        self.update()
        self.owningNode().update()

    def onChildKilled(self, uiPin):
        self._pins.remove(uiPin)
        if len(self._pins) == 0:
            self.kill()

    def addPin(self, uiPin):
        self._pins.append(uiPin)
        uiPin.OnPinDeleted.connect(self.onChildKilled)

    def onClick(self):
        self.setExpanded(not self.expanded)

    def contextMenuEvent(self, event):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        if self._direction == PinDirection.Input:
            self.owningNode().groups["input"][newName] = self.owningNode(
            ).groups["input"].pop(self._name)
        else:
            self.owningNode().groups["output"][newName] = self.owningNode(
            ).groups["output"].pop(self._name)
        self._name = newName

    def hoverEnterEvent(self, event):
        super(QGraphicsWidget, self).hoverEnterEvent(event)
        self.hovered = True
        self.update()
        self.owningNode().update()
        event.accept()

    def hoverLeaveEvent(self, event):
        super(QGraphicsWidget, self).hoverLeaveEvent(event)
        self.hovered = False
        self.update()
        self.owningNode().update()
        event.accept()

    def sizeHint(self, which, constraint):
        height = QtGui.QFontMetrics(self._font).height()
        width = QtGui.QFontMetrics(self._font).width(self.name) + self.pinSize
        return QtCore.QSizeF(width, height)

    def paint(self, painter, option, widget):
        frame = QtCore.QRectF(QtCore.QPointF(0, 0), self.geometry().size())
        frame = frame.translated(self.pinSize * 1.1, 0)
        # TODO: move group bg color to themes?
        groupBGColor = self.owningNode().color.lighter(150)
        bgRect = QtCore.QRectF(frame)
        bgRect.setX(0)
        painter.setFont(self._font)
        painter.setPen(QtGui.QPen(self.labelColor, 1.0))
        painter.drawText(frame, self.name)

        painter.setPen(QtGui.QPen(self.labelColor, 0.1))
        square = QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(
            self.pinSize / 1.1, self.pinSize / 1.1))
        square2 = square.translated(0, (self.pinSize / 1.1) / 3)
        painter.drawRect(square2)

        font = QtGui.QFont(self._font)
        font.setPixelSize(7)
        painter.setFont(font)
        if not self.expanded:
            x = QtGui.QFontMetrics(font).width("+")
            square = square.translated(x / 3, 0.5)
            painter.drawText(square, "+")
        else:
            x = QtGui.QFontMetrics(font).width("-")
            square = square.translated(x / 3, 0.5)
            painter.drawText(square, "-")


def REGISTER_UI_PIN_FACTORY(packageName, factory):
    if packageName not in UI_PINS_FACTORIES:
        UI_PINS_FACTORIES[packageName] = factory
        print("registering", packageName, "ui pins")


def getUIPinInstance(owningNode, raw_instance):
    packageName = raw_instance.packageName
    instance = None
    if packageName in UI_PINS_FACTORIES:
        return UI_PINS_FACTORIES[packageName](owningNode, raw_instance)
    else:
        return UIPinBase(owningNode, raw_instance)
