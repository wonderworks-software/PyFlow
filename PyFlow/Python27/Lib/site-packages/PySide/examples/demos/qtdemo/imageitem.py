from PySide import QtCore, QtGui

from colors import Colors
from demoitem import DemoItem


class ImageItem(DemoItem):
    def __init__(self, image, maxWidth, maxHeight, scene=None, parent=None,
            adjustSize=False, scale=1.0):
        super(ImageItem, self).__init__(scene, parent)

        self.image = image
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.adjustSize = adjustSize
        self.scale = scale

    def createImage(self, matrix):
        original = QtGui.QImage(self.image)
        if original.isNull():
            return original

        size = matrix.map(QtCore.QPoint(self.maxWidth, self.maxHeight))
        w = size.x()
        h = size.y()

        # Optimization: if image is smaller than maximum allowed size, just
        # return the loaded image.
        if original.size().height() <= h and original.size().width() <= w and not self.adjustSize and self.scale == 1:
            return original

        # Calculate what the size of the final image will be.
        w = min(w, float(original.size().width()) * self.scale)
        h = min(h, float(original.size().height()) * self.scale)

        adjustx = 1.0
        adjusty = 1.0
        if self.adjustSize:
            adjustx = min(matrix.m11(), matrix.m22())
            adjusty = max(matrix.m22(), adjustx)
            w *= adjustx
            h *= adjusty

        # Create a new image with correct size, and draw original on it.
        image = QtGui.QImage(int(w + 2), int(h + 2),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        if self.adjustSize:
            painter.scale(adjustx, adjusty)
        if self.scale != 1:
            painter.scale(self.scale, self.scale)
        painter.drawImage(0, 0, original)

        if not self.adjustSize:
            # Blur out edges.
            blur = 30

            if h < original.height():
                brush1 = QtGui.QLinearGradient(0, h - blur, 0, h)
                brush1.setSpread(QtGui.QGradient.PadSpread)
                brush1.setColorAt(0.0, QtGui.QColor(0, 0, 0, 0))
                brush1.setColorAt(1.0, Colors.sceneBg1)
                painter.fillRect(0, int(h) - blur, original.width(), int(h),
                        brush1)

            if w < original.width():
                brush2 = QtGui.QLinearGradient(w - blur, 0, w, 0)
                brush2.setSpread(QtGui.QGradient.PadSpread)
                brush2.setColorAt(0.0, QtGui.QColor(0, 0, 0, 0))
                brush2.setColorAt(1.0, Colors.sceneBg1)
                painter.fillRect(int(w) - blur, 0, int(w), original.height(),
                        brush2)

        return image
