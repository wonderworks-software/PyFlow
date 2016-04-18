#!/usr/bin/env python

"""PyQt4 port of the examples/graphicsview/padnavigator example from Qt v4.x"""

import math

from PySide import QtCore, QtGui, QtOpenGL

from padnavigator_rc import *
from ui_backside import Ui_BackSide


class Panel(QtGui.QGraphicsView):
    def __init__(self, width, height):
        super(Panel, self).__init__()

        self.selectedX = 0
        self.selectedY = 0
        self.width = width
        self.height = height
        self.flipped = False
        self.flipLeft = True

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.setRenderHints(QtGui.QPainter.Antialiasing |
                QtGui.QPainter.SmoothPixmapTransform |
                QtGui.QPainter.TextAntialiasing)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap('./images/blue_angle_swirl.jpg')))

        if QtOpenGL.QGLFormat.hasOpenGL():
            self.setViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)))

        self.setMinimumSize(50, 50)

        self.selectionTimeLine = QtCore.QTimeLine(150, self)
        self.flipTimeLine = QtCore.QTimeLine(500, self)
        bounds = QtCore.QRectF((-width / 2.0) * 150, (-height / 2.0) * 150, width * 150, height * 150)

        self.scene = QtGui.QGraphicsScene(bounds, self)
        self.setScene(self.scene)

        self.baseItem = RoundRectItem(bounds, QtGui.QColor(226, 255, 92, 64))
        self.scene.addItem(self.baseItem)

        embed = QtGui.QWidget()

        self.ui = Ui_BackSide()
        self.ui.setupUi(embed) 
        self.ui.hostName.setFocus()

        self.backItem = RoundRectItem(bounds, embed.palette().window(), embed)
        self.backItem.setTransform(QtGui.QTransform().rotate(180, QtCore.Qt.YAxis))
        self.backItem.setParentItem(self.baseItem)

        self.selectionItem = RoundRectItem(QtCore.QRectF(-60, -60, 120, 120), QtCore.Qt.gray)
        self.selectionItem.setParentItem(self.baseItem)
        self.selectionItem.setZValue(-1)
        self.selectionItem.setPos(self.posForLocation(0, 0))
        self.startPos = self.selectionItem.pos()
        self.endPos = QtCore.QPointF()

        self.grid = []

        for y in range(height):
            self.grid.append([])
            for x in range(width):
                item = RoundRectItem(QtCore.QRectF(-54, -54, 108, 108), QtGui.QColor(214, 240, 110, 128))
                item.setPos(self.posForLocation(x, y))

                item.setParentItem(self.baseItem)
                item.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
                self.grid[y].append(item)

                rand = QtCore.qrand() % 9
                if rand == 0 :
                    item.setPixmap(QtGui.QPixmap(':/images/kontact_contacts.png'))
                elif rand == 1:
                    item.setPixmap(QtGui.QPixmap(':/images/kontact_journal.png'))
                elif rand == 2:
                    item.setPixmap(QtGui.QPixmap(':/images/kontact_notes.png'))
                elif rand == 3:
                    item.setPixmap(QtGui.QPixmap(':/images/kopeteavailable.png'))
                elif rand == 4:
                    item.setPixmap(QtGui.QPixmap(':/images/metacontact_online.png'))
                elif rand == 5:
                    item.setPixmap(QtGui.QPixmap(':/images/minitools.png'))
                elif rand == 6:
                    item.setPixmap(QtGui.QPixmap(':/images/kontact_journal.png'))
                elif rand == 7:
                    item.setPixmap(QtGui.QPixmap(':/images/kontact_contacts.png'))
                elif rand == 8:
                    item.setPixmap(QtGui.QPixmap(':/images/kopeteavailable.png'))
                else:
                    pass

                item.qobject.activated.connect(self.flip)

        self.grid[0][0].setFocus()

        self.backItem.qobject.activated.connect(self.flip)
        self.selectionTimeLine.valueChanged.connect(self.updateSelectionStep)
        self.flipTimeLine.valueChanged.connect(self.updateFlipStep)

        self.splash = SplashItem()
        self.splash.setZValue(5)
        self.splash.setPos(-self.splash.rect().width()/2,
                self.scene.sceneRect().top())
        self.scene.addItem(self.splash)

        self.splash.grabKeyboard()

        self.updateSelectionStep(0)

        self.setWindowTitle("Pad Navigator Example")

    def keyPressEvent(self, event):
        if self.splash.isVisible() or event.key() == QtCore.Qt.Key_Return or self.flipped :
            super(Panel, self).keyPressEvent(event)
            return

        self.selectedX = (self.selectedX + self.width + (event.key() == QtCore.Qt.Key_Right) - (event.key() == QtCore.Qt.Key_Left)) % self.width
        self.selectedY = (self.selectedY + self.height + (event.key() == QtCore.Qt.Key_Down) - (event.key() == QtCore.Qt.Key_Up)) % self.height
        self.grid[self.selectedY][self.selectedX].setFocus()

        self.selectionTimeLine.stop()
        self.startPos = self.selectionItem.pos()
        self.endPos = self.posForLocation(self.selectedX, self.selectedY)
        self.selectionTimeLine.start()

    def resizeEvent(self, event):
        super(Panel, self).resizeEvent(event)
        self.fitInView(self.scene.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def updateSelectionStep(self, val):
        self.newPos = QtCore.QPointF(self.startPos.x() + (self.endPos - self.startPos).x() * val,
                    self.startPos.y() + (self.endPos - self.startPos).y() * val)
        self.selectionItem.setPos(self.newPos)

        transform= QtGui.QTransform()
        self.yrot = self.newPos.x() / 6.0
        self.xrot = self.newPos.y() / 6.0
        transform.rotate(self.newPos.x() / 6.0, QtCore.Qt.YAxis)
        transform.rotate(self.newPos.y() / 6.0, QtCore.Qt.XAxis)
        self.baseItem.setTransform(transform)

    def updateFlipStep(self, val):
        finalxrot = self.xrot - self.xrot * val
        if self.flipLeft:
            finalyrot = self.yrot - self.yrot * val - 180 * val
        else:
            finalyrot = self.yrot - self.yrot * val + 180 * val
        transform = QtGui.QTransform()
        transform.rotate(finalyrot, QtCore.Qt.YAxis)
        transform.rotate(finalxrot, QtCore.Qt.XAxis)
        scale = 1 - math.sin(3.14 * val) * 0.3
        transform.scale(scale, scale)
        self.baseItem.setTransform(transform)
        if val == 0:
            self.grid[self.selectedY][self.selectedX].setFocus()

    def flip(self):
        if self.flipTimeLine.state() == QtCore.QTimeLine.Running:
            return

        if self.flipTimeLine.currentValue() == 0:
            self.flipTimeLine.setDirection(QtCore.QTimeLine.Forward)
            self.flipTimeLine.start()
            self.flipped = True
            self.flipLeft = self.selectionItem.pos().x() < 0
        else:
            self.flipTimeLine.setDirection(QtCore.QTimeLine.Backward)
            self.flipTimeLine.start()
            self.flipped = False

    def posForLocation(self, x, y):
        return QtCore.QPointF(x*150, y*150) - QtCore.QPointF((self.width - 1) * 75, (self.height - 1) * 75)


class Activated(QtCore.QObject):

    activated = QtCore.Signal()


class RoundRectItem(QtGui.QGraphicsRectItem):
    def __init__(self, rect, brush, embeddedWidget=None):
        super(RoundRectItem, self).__init__(rect)

        self.brush = QtGui.QBrush(brush)
        self.timeLine = QtCore.QTimeLine(75)
        self.lastVal = 0
        self.opa = 1
        self.proxyWidget = None
        self.pix = QtGui.QPixmap()

        # In the C++ version of this example, this class is also derived from
        # QObject in order to emit the activated() signal.  PyQt does not
        # support deriving from more than one wrapped class so we just create
        # an explicit QObject sub-class.
        self.qobject = Activated()

        self.timeLine.valueChanged.connect(self.updateValue)

        if embeddedWidget:
            self.proxyWidget = QtGui.QGraphicsProxyWidget(self)
            self.proxyWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.proxyWidget.setWidget(embeddedWidget)
            self.proxyWidget.setGeometry(self.boundingRect().adjusted(25, 25, -25, -25))

    def paint(self, painter, qstyleoptiongraphicsitem, qwidget):
        x = painter.worldTransform()

        unit = x.map(QtCore.QLineF(0, 0, 1, 1))
        if unit.p1().x() > unit.p2().x() or unit.p1().y() > unit.p2().y():
            if self.proxyWidget and self.proxyWidget.isVisible():
                self.proxyWidget.hide()
                self.proxyWidget.setGeometry(self.rect())
            return

        if self.proxyWidget and not self.proxyWidget.isVisible():
            self.proxyWidget.show()
            self.proxyWidget.setFocus()

        if (self.proxyWidget and self.proxyWidget.pos() != QtCore.QPoint()):
            self.proxyWidget.setGeometry(self.boundingRect().adjusted(25, 25, -25, -25))

        painter.setOpacity(self.opacity())
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 64))
        painter.drawRoundRect(self.rect().translated(2, 2))

        if not self.proxyWidget:
            gradient= QtGui.QLinearGradient (self.rect().topLeft(), self.rect().bottomRight())
            col = self.brush.color()
            gradient.setColorAt(0, col)
            gradient.setColorAt(1, col.darker(int(200 + self.lastVal * 50)))
            painter.setBrush(gradient)
        else:
            painter.setBrush(self.brush)

        painter.setPen(QtGui.QPen(QtCore.Qt.black, 1))
        painter.drawRoundRect(self.rect())
        if not self.pix.isNull():
            painter.scale(1.95, 1.95)
            painter.drawPixmap(-self.pix.width() / 2, -self.pix.height() / 2, self.pix)

    def boundingRect(self):
        penW = 0.5
        shadowW = 2.0
        return self.rect().adjusted(-penW, -penW, penW + shadowW, penW + shadowW)

    def setPixmap(self, pixmap):
        self.pix = pixmap
        if self.scene() and self.isVisible():
            self.update()

    def opacity(self):
        parent = self.parentItem()

        if parent:
            op = parent.opacity()
        else:
            op = 0
        return self.opa + op

    def setOpacity(self, opacity):
        self.opa = opacity
        self.update()

    def keyPressEvent(self, event):
        if event.isAutoRepeat() or event.key() != QtCore.Qt.Key_Return \
                or (self.timeLine.state() == QtCore.QTimeLine.Running and self.timeLine.direction() == QtCore.QTimeLine.Forward):
            super(RoundRectItem, self).keyPressEvent(event)
            return

        self.timeLine.stop()
        self.timeLine.setDirection(QtCore.QTimeLine.Forward)
        self.timeLine.start()
        self.qobject.activated.emit()

    def keyReleaseEvent(self, event):
        if event.key() != QtCore.Qt.Key_Return:
            super(RoundRectItem, self).keyReleaseEvent(event)
            return

        self.timeLine.stop()
        self.timeLine.setDirection(QtCore.QTimeLine.Backward)
        self.timeLine.start()

    def updateValue(self, value):
        self.lastVal = value
        if not self.proxyWidget:
            self.setTransform(QtGui.QTransform().scale(1 - value / 10.0, 1 - value / 10.0))


class SplashItem(QtGui.QGraphicsWidget):
    def __init__(self, parent=None):
        super(SplashItem, self).__init__(parent)

        self.opacity = 1.0

        self.timeLine = QtCore.QTimeLine(350)
        self.timeLine.setCurveShape(QtCore.QTimeLine.EaseInCurve)
        self.timeLine.valueChanged.connect(self.setValue)

        self.text = "Welcome to the Pad Navigator Example. You can use the " \
                "keyboard arrows to navigate the icons, and press enter to " \
                "activate an item. Please " "press any key to continue."
        self.resize(400, 175)

    def paint(self, painter, qstyleoptiongraphicsitem, qwidget):
        painter.setOpacity(self.opacity)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.setBrush(QtGui.QColor(245, 245, 255, 220))
        painter.setClipRect(self.rect())
        painter.drawRoundRect(3, -100 + 3, 400 - 6, 250 - 6)

        textRect = self.rect().adjusted(10, 10, -10, -10)
        flags = int(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft) | QtCore.Qt.TextWordWrap

        font = QtGui.QFont()
        font.setPixelSize(18)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(font)
        painter.drawText(textRect, flags, self.text)

    def keyPressEvent(self, event):
        if self.timeLine.state() == QtCore.QTimeLine.NotRunning:
            self.timeLine.start()

    def setValue(self, value):
        self.opacity = 1 - value
        self.setPos(self.x(), self.scene().sceneRect().top() - self.rect().height() * value)
        if value == 1:
            self.hide()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    panel = Panel(3, 3)
    panel.setFocus()
    panel.show()

    sys.exit(app.exec_())
