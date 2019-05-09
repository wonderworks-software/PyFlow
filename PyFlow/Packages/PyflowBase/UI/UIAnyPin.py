from PyFlow.Packages.PyflowBase import PACKAGE_NAME
from PyFlow.Core import PinBase
from PyFlow import findPinClassByType
from PyFlow.Core.Common import *
from PyFlow.UI.Utils.Settings import Colors
from PyFlow.UI.Canvas.Painters import PinPainter
from PyFlow import getAllPinClasses
from PyFlow.Packages.PyflowBase.Pins.AnyPin import AnyPin

from PyFlow.UI.Canvas.UIPinBase import UIPinBase
from Qt import QtGui


class UIAnyPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIAnyPin, self).__init__(owningNode, raw_pin)
        self._defaultColor = self._pinColor
        self._rawPin.typeChanged.connect(self.setType)
        self._rawPin.dataTypeBeenSet.connect(self.dataTypeBeenSet)

    def dataTypeBeenSet(self, *args, **kwargs):
        self.setDefault(self._rawPin.defColor())

    def checkFree(self, checked=[], selfChek=True):
        return self._rawPin.checkFree(checked, selfChek)

    @property
    def activeDataType(self):
        return self._rawPin.activeDataType

    def setDefault(self, defcolor):
        self._pinColor = QtGui.QColor(*defcolor)
        for e in self.connections:
            e.setColor(QtGui.QColor(*defcolor))
        self.OnPinChanged.emit(self)
        self.update()

    def setType(self, dataType):
        colorTuple = findPinClassByType(dataType).color()
        self._pinColor = QtGui.QColor(*colorTuple)
        for e in self.connections:
            e.setColor(self._pinColor)
        self.OnPinChanged.emit(self)
        self.update()

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        supportedTypes = self._rawPin.supportedDataTypes()
        hoverMessage = "Data: {0}\r\nDirty: {1}\r\nAllowed Types: {2}".format(str(self._rawPin.currentData()), self._rawPin.dirty, supportedTypes)
        self.setToolTip(hoverMessage)
        event.accept()

    def paint(self, painter, option, widget):
        if self.isExec():
            PinPainter.asExecPin(self, painter, option, widget)
        elif self.isList():
            PinPainter.asArrayPin(self, painter, option, widget)
        else:
            PinPainter.asValuePin(self, painter, option, widget)
