from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem


class ScanItem(DemoItem):
    ITEM_WIDTH = 16
    ITEM_HEIGHT = 16

    def __init__(self, scene=None, parent=None):
        super(ScanItem, self).__init__(scene, parent)

        self.useSharedImage(__file__)

    def createImage(self, matrix):
        scaledRect = matrix.mapRect(QtCore.QRect(0, 0, ScanItem.ITEM_WIDTH, ScanItem.ITEM_HEIGHT))
        image = QtGui.QImage(scaledRect.width(), scaledRect.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if Colors.useEightBitPalette:
            painter.setPen(QtGui.QPen(QQtGui.Color(100, 100, 100), 2))
            painter.setBrush(QQtGui.Color(206, 246, 117))
            painter.drawEllipse(1, 1, scaledRect.width() - 2,
                    scaledRect.height() - 2)
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 15), 1))
            painter.setBrush(QtGui.QColor(0, 0, 0, 15))
            painter.drawEllipse(1, 1, scaledRect.width() - 2,
                    scaledRect.height() - 2)

        return image
