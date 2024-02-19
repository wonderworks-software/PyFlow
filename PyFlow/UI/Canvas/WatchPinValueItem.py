from qtpy import QtCore

from qtpy.QtWidgets import *

from PyFlow.UI.Utils.stylesheet import editableStyleSheet


class WatchItem(QGraphicsTextItem):
    """docstring for WatchItem."""

    def __init__(self, text=""):
        super(WatchItem, self).__init__(text)

    def paint(self, painter, option, widget):
        painter.drawRect(self.boundingRect())
        painter.fillRect(self.boundingRect(), editableStyleSheet().BgColor)
        super(WatchItem, self).paint(painter, option, widget)
