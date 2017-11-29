from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem


class HeadingItem(DemoItem):
    def __init__(self, text, scene=None, parent=None):
        super(HeadingItem, self).__init__(scene, parent)

        self.text = text
        self.noSubPixeling = True

    def createImage(self, matrix):
        sx = min(matrix.m11(), matrix.m22())
        sy = max(matrix.m22(), sx)
        fm = QtGui.QFontMetrics(Colors.headingFont())

        w = fm.width(self.text) + 1
        h = fm.height()
        xShadow = 3.0
        yShadow = 3.0

        image = QtGui.QImage(int((w + xShadow) * sx), int((h + yShadow) * sy),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.setFont(Colors.headingFont())
        painter.scale(sx, sy)

        # Draw shadow.
        brush_shadow = QtGui.QLinearGradient(xShadow, yShadow, w, yShadow)
        brush_shadow.setSpread(QtGui.QLinearGradient.PadSpread)
        if Colors.useEightBitPalette:
            brush_shadow.setColorAt(0.0, QtGui.QColor(0, 0, 0))
        else:
            brush_shadow.setColorAt(0.0, QtGui.QColor(0, 0, 0, 100))
        pen_shadow = QtGui.QPen()
        pen_shadow.setBrush(brush_shadow)
        painter.setPen(pen_shadow)
        painter.drawText(int(xShadow), int(yShadow), int(w), int(h),
                QtCore.Qt.AlignLeft, self.text)

        # Draw text.
        brush_text = QtGui.QLinearGradient(0, 0, w, w)
        brush_text.setSpread(QtGui.QLinearGradient.PadSpread)
        brush_text.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        brush_text.setColorAt(0.2, QtGui.QColor(255, 255, 255))
        brush_text.setColorAt(0.5, QtGui.QColor(190, 190, 190))
        pen_text = QtGui.QPen()
        pen_text.setBrush(brush_text)
        painter.setPen(pen_text)
        painter.drawText(0, 0, int(w), int(h), QtCore.Qt.AlignLeft, self.text)

        return image

    def animationStarted(self, id=0):
        self.noSubPixeling = False

    def animationStopped(self, id=0):
        self.noSubPixeling = True
