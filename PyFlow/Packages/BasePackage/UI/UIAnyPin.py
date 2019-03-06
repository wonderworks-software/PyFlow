from PyFlow.Packages.BasePackage import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow.Core.AGraphCommon import *
from PyFlow.UI.Settings import Colors
from PyFlow import getAllPinClasses

from PyFlow.UI.UIPinBase import UIPinBase
from Qt import QtGui


class UIAnyPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIAnyPin, self).__init__(owningNode, raw_pin)
        self._defaultColor = self._color

    def checkFree(self, checked=[], selfChek=True):
        return self._rawPin.checkFree(checked, selfChek)

    def pinConnected(self, other):
        self._rawPin.updateOnConnection(other._rawPin)
        UIPinBase.pinConnected(self, other)
        self.OnPinConnected.emit(other)

    def pinDisconnected(self, other):
        UIPinBase.pinDisconnected(self, other._rawPin)
        self.OnPinConnected.emit(other)
        self._rawPin.updateOnDisconnection()

    def setDefault(self, defcolor):
        self._color = QtGui.QColor(*defcolor)
        for e in self.edge_list:
            e.setColor(QtGui.QColor(*defcolor))
        self.OnPinChanged.emit(self)
        self.update()

    def setType(self, otherColor):
        self._color = QtGui.QColor(*otherColor)
        for e in self.edge_list:
            e.setColor(self._color)
        self.OnPinChanged.emit(self)
        self.update()

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}\r\nAllowed Types: {2}".format(str(
            self._rawPin.currentData()), self._rawPin.dirty, self._rawPin.supportedDataTypesList)
        self.setToolTip(hoverMessage)
        event.accept()
