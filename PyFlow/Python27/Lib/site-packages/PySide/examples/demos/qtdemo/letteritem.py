from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem


class LetterItem(DemoItem):
    def __init__(self, letter, scene=None, parent=None):
        super(LetterItem, self).__init__(scene, parent)

        self.letter = letter

        self.useSharedImage(__file__ + letter)

    def createImage(self, matrix):
        scaledRect = matrix.mapRect(QtCore.QRect(0, 0, 25, 25))
        image = QtGui.QImage(scaledRect.width(), scaledRect.height(),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(0)
        painter = QtGui.QPainter(image)
        painter.scale(matrix.m11(), matrix.m22())
        painter.setRenderHints(QtGui.QPainter.TextAntialiasing | QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        painter.setPen(QtCore.Qt.NoPen)

        if Colors.useEightBitPalette:
            painter.setBrush(QtGui.QColor(102, 175, 54))
            painter.drawEllipse(0, 0, 25, 25)
            painter.setFont(Colors.tickerFont())
            painter.setPen(QtGui.QColor(255, 255, 255))
            painter.drawText(10, 15, self.letter)
        else:
            brush = QtGui.QLinearGradient(0, 0, 0, 25)
            brush.setSpread(QtGui.QLinearGradient.PadSpread)
            brush.setColorAt(0.0, QtGui.QColor(102, 175, 54, 200))
            brush.setColorAt(1.0, QtGui.QColor(102, 175, 54, 60))
            painter.setBrush(brush)
            painter.drawEllipse(0, 0, 25, 25)
            painter.setFont(Colors.tickerFont())
            painter.setPen(QtGui.QColor(255, 255, 255, 255))
            painter.drawText(10, 15, self.letter)

        return image
