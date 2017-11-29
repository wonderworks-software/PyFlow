from PySide import QtCore, QtGui

from demoitem import DemoItem


class DemoTextItem(DemoItem):
    STATIC_TEXT, DYNAMIC_TEXT = range(2)

    def __init__(self, text, font, textColor, textWidth, scene=None,
            parent=None, type=STATIC_TEXT, bgColor=QtGui.QColor()):
        super(DemoTextItem, self).__init__(scene, parent)

        self.type = type
        self.text = text
        self.font = font
        self.textColor = textColor
        self.bgColor = bgColor
        self.textWidth = textWidth
        self.noSubPixeling = True

    def setText(self, text):
        self.text = text
        self.update()

    def createImage(self, matrix):
        if self.type == DemoTextItem.DYNAMIC_TEXT:
            return None

        sx = min(matrix.m11(), matrix.m22())
        sy = max(matrix.m22(), sx)

        textItem = QtGui.QGraphicsTextItem()
        textItem.setHtml(self.text)
        textItem.setTextWidth(self.textWidth)
        textItem.setFont(self.font)
        textItem.setDefaultTextColor(self.textColor)
        textItem.document().setDocumentMargin(2)

        w = textItem.boundingRect().width()
        h = textItem.boundingRect().height()
        image = QtGui.QImage(int(w * sx), int(h * sy),
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.QColor(0, 0, 0, 0).rgba())
        painter = QtGui.QPainter(image)
        painter.scale(sx, sy)
        style = QtGui.QStyleOptionGraphicsItem()
        textItem.paint(painter, style, None)

        return image

    def animationStarted(self, id=0):
        self.noSubPixeling = False

    def animationStopped(self, id=0):
        self.noSubPixeling = True

    def boundingRect(self):
        if self.type == DemoTextItem.STATIC_TEXT:
            return super(DemoTextItem, self).boundingRect()

        # Sorry for using magic number.
        return QtCore.QRectF(0, 0, 50, 20)

    def paint(self, painter, option, widget):
        if self.type == DemoTextItem.STATIC_TEXT:
            super(DemoTextItem, self).paint(painter, option, widget)
            return

        painter.setPen(self.textColor)
        painter.drawText(0, 0, self.text)
