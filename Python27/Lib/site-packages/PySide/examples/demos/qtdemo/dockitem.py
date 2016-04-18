from PySide import QtGui

from colors import Colors
from demoitem import DemoItem


class DockItem(DemoItem):
    UP, DOWN, LEFT, RIGHT = range(4)

    def __init__(self, orien, x, y, width, length, scene=None, parent=None):
        super(DockItem, self).__init__(scene, parent)

        self.orientation = orien
        self.width = width
        self.length = length
        self.setPos(x, y)
        self.setZValue(40)
        self.setupPixmap()

    def setupPixmap(self):
        self.pixmap = QtGui.QPixmap(int(self.boundingRect().width()),
                int(self.boundingRect().height()))
        self.pixmap.fill(QtGui.QColor(0, 0, 0, 0))

        painter = QtGui.QPainter(self.pixmap)

        # Create brush.
        background = Colors.sceneBg1
        brush = QtGui.QLinearGradient(0, 0, 0, self.boundingRect().height())
        brush.setSpread(QtGui.QGradient.PadSpread)

        if self.orientation == DockItem.DOWN:
            brush.setColorAt(0.0, background)
            brush.setColorAt(0.2, background)
            background.setAlpha(0)
            brush.setColorAt(1.0, background)
        elif self.orientation == DockItem.UP:
            brush.setColorAt(1.0, background)
            brush.setColorAt(0.8, background)
            background.setAlpha(0)
            brush.setColorAt(0.0, background)

        painter.fillRect(0, 0, int(self.boundingRect().width()),
                int(self.boundingRect().height()), brush)

    def boundingRect(self):
        if self.orientation in (DockItem.UP, DockItem.DOWN):
            return QtCore.QRectF(0, 0, self.length, self.width)
        else:
            return QtCore.QRectF(0, 0, self.width, self.length)

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self.pixmap)
