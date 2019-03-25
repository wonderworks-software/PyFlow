from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import Colors
from PyFlow.UI.Graph.Painters import PinPainter
from PyFlow import getAllPinClasses
from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin

from PyFlow.UI.Graph.UIPinBase import UIPinBase
from Qt import QtGui


class UIAnyPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIAnyPin, self).__init__(owningNode, raw_pin)
        self._defaultColor = self._color

    def checkFree(self, checked=[], selfChek=True):
        return self._rawPin.checkFree(checked, selfChek)

    @property
    def activeDataType(self):
        return self._rawPin.activeDataType

    def pinConnected(self, other):
        self._rawPin.updateOnConnection(other._rawPin)
        UIPinBase.pinConnected(self, other)
        self.OnPinConnected.emit(other)

    def pinDisconnected(self, other):
        UIPinBase.pinDisconnected(self, other)
        self.OnPinConnected.emit(other)

    def setDefault(self, defcolor):
        self._color = QtGui.QColor(*defcolor)
        for e in self.connections:
            e.setColor(QtGui.QColor(*defcolor))
        self.OnPinChanged.emit(self)
        self.update()

    def setType(self, otherColor):
        self._color = QtGui.QColor(*otherColor)
        for e in self.connections:
            e.setColor(self._color)
        self.OnPinChanged.emit(self)
        self.update()

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}\r\nAllowed Types: {2}".format(str(
            self._rawPin.currentData()), self._rawPin.dirty, AnyPin.supportedDataTypes())
        self.setToolTip(hoverMessage)
        event.accept()

    def paint(self, painter, option, widget):
        if self.dataType == "ExecPin":
            PinPainter.asExecPin(self, painter, option, widget)
        elif self.isArray():
            PinPainter.asArrayPin(self, painter, option, widget)
        else:
            PinPainter.asValuePin(self, painter, option, widget)
