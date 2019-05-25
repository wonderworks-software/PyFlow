from PyFlow.UI.Canvas.Painters import PinPainter
from PyFlow.UI.Canvas.UIPinBase import UIPinBase


class UIListPin(UIPinBase):
    def __init__(self, owningNode, raw_pin):
        super(UIListPin, self).__init__(owningNode, raw_pin)

    def paint(self, painter, option, widget):
        PinPainter.asListPin(self, painter, option, widget)
