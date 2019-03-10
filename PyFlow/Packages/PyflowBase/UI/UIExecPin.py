from Qt import (
    QtGui,
    QtCore
)

from PyFlow.Core import PinBase
from PyFlow.Core.Common import *
from PyFlow.UI.UIPinBase import UIPinBase
from PyFlow.UI.PinPainter import PinPainter


class UIExecPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIExecPin, self).__init__(owningNode, raw_pin)

    def paint(self, painter, option, widget):
        PinPainter.asExecPin(self, painter, option, widget)

    def hoverEnterEvent(self, event):
        super(UIPinBase, self).hoverEnterEvent(event)
        self.update()
        self.hovered = True
        hoverMessage = "Data: {0}\r\nDirty: {1}".format(str(self._rawPin.currentData()), self._rawPin.dirty)
        self.setToolTip(hoverMessage)
        event.accept()
