#!/usr/bin/env python

# This file was taken from Riverbank's examples,
# which was an adaptation of the original C++ Qt's examples.


from PySide import QtCore, QtGui

import animatedtiles_rc


# PyQt doesn't support deriving from more than one wrapped class so we use
# composition and delegate the property.
class Pixmap(QtCore.QObject):
    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.pixmap_item = QtGui.QGraphicsPixmapItem(pix)
        self.pixmap_item.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)

    def set_pos(self, pos):
        self.pixmap_item.setPos(pos)

    def get_pos(self):
        return self.pixmap_item.pos()

    pos = QtCore.Property(QtCore.QPointF, get_pos, set_pos)


class Button(QtGui.QGraphicsWidget):
    pressed = QtCore.Signal()

    def __init__(self, pixmap, parent=None):
        super(Button, self).__init__(parent)

        self._pix = pixmap

        self.setAcceptHoverEvents(True)
        self.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)

    def boundingRect(self):
        return QtCore.QRectF(-65, -65, 130, 130)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())

        return path

    def paint(self, painter, option, widget):
        down = option.state & QtGui.QStyle.State_Sunken
        r = self.boundingRect()

        grad = QtGui.QLinearGradient(r.topLeft(), r.bottomRight())
        if option.state & QtGui.QStyle.State_MouseOver:
            color_0 = QtCore.Qt.white
        else:
            color_0 = QtCore.Qt.lightGray

        color_1 = QtCore.Qt.darkGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(QtCore.Qt.darkGray)
        painter.setBrush(grad)
        painter.drawEllipse(r)

        color_0 = QtCore.Qt.darkGray
        color_1 = QtCore.Qt.lightGray

        if down:
            color_0, color_1 = color_1, color_0

        grad.setColorAt(0, color_0)
        grad.setColorAt(1, color_1)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(grad)

        if down:
            painter.translate(2, 2)

        painter.drawEllipse(r.adjusted(5, 5, -5, -5))
        painter.drawPixmap(-self._pix.width() / 2, -self._pix.height() / 2,
                self._pix)

    def mousePressEvent(self, ev):
        self.pressed.emit()
        self.update()

    def mouseReleaseEvent(self, ev):
        self.update()


class View(QtGui.QGraphicsView):
    def resizeEvent(self, event):
        super(View, self).resizeEvent(event)
        self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)


if __name__ == '__main__':

    import sys
    import math

    app = QtGui.QApplication(sys.argv)

    kineticPix = QtGui.QPixmap(':/images/kinetic.png')
    bgPix = QtGui.QPixmap(':/images/Time-For-Lunch-2.jpg')

    scene = QtGui.QGraphicsScene(-350, -350, 700, 700)

    items = []
    for i in range(64):
        item = Pixmap(kineticPix)
        item.pixmap_item.setOffset(-kineticPix.width() / 2,
                -kineticPix.height() / 2)
        item.pixmap_item.setZValue(i)
        items.append(item)
        scene.addItem(item.pixmap_item)

    # Buttons.
    buttonParent = QtGui.QGraphicsRectItem()
    ellipseButton = Button(QtGui.QPixmap(':/images/ellipse.png'), buttonParent)
    figure8Button = Button(QtGui.QPixmap(':/images/figure8.png'), buttonParent)
    randomButton = Button(QtGui.QPixmap(':/images/random.png'), buttonParent)
    tiledButton = Button(QtGui.QPixmap(':/images/tile.png'), buttonParent)
    centeredButton = Button(QtGui.QPixmap(':/images/centered.png'), buttonParent)

    ellipseButton.setPos(-100, -100)
    figure8Button.setPos(100, -100)
    randomButton.setPos(0, 0)
    tiledButton.setPos(-100, 100)
    centeredButton.setPos(100, 100)

    scene.addItem(buttonParent)
    buttonParent.scale(0.75, 0.75)
    buttonParent.setPos(200, 200)
    buttonParent.setZValue(65)

    # States.
    rootState = QtCore.QState()
    ellipseState = QtCore.QState(rootState)
    figure8State = QtCore.QState(rootState)
    randomState = QtCore.QState(rootState)
    tiledState = QtCore.QState(rootState)
    centeredState = QtCore.QState(rootState)

    # Values.
    for i, item in enumerate(items):
        # Ellipse.
        ellipseState.assignProperty(item, 'pos',
                QtCore.QPointF(math.cos((i / 63.0) * 6.28) * 250,
                        math.sin((i / 63.0) * 6.28) * 250))

        # Figure 8.
        figure8State.assignProperty(item, 'pos',
                QtCore.QPointF(math.sin((i / 63.0) * 6.28) * 250,
                        math.sin(((i * 2)/63.0) * 6.28) * 250))

        # Random.
        randomState.assignProperty(item, 'pos',
                QtCore.QPointF(-250 + QtCore.qrand() % 500,
                        -250 + QtCore.qrand() % 500))

        # Tiled.
        tiledState.assignProperty(item, 'pos',
                QtCore.QPointF(((i % 8) - 4) * kineticPix.width() + kineticPix.width() / 2,
                        ((i // 8) - 4) * kineticPix.height() + kineticPix.height() / 2))

        # Centered.
        centeredState.assignProperty(item, 'pos', QtCore.QPointF())

    # Ui.
    view = View(scene)
    view.setWindowTitle("Animated Tiles")
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.setBackgroundBrush(QtGui.QBrush(bgPix))
    view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    view.setRenderHints(
            QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
    view.show()

    states = QtCore.QStateMachine()
    states.addState(rootState)
    states.setInitialState(rootState)
    rootState.setInitialState(centeredState)

    group = QtCore.QParallelAnimationGroup()
    for i, item in enumerate(items):
        anim = QtCore.QPropertyAnimation(item, 'pos')
        anim.setDuration(750 + i * 25)
        anim.setEasingCurve(QtCore.QEasingCurve.InOutBack)
        group.addAnimation(anim)

    trans = rootState.addTransition(ellipseButton.pressed, ellipseState)
    trans.addAnimation(group)

    trans = rootState.addTransition(figure8Button.pressed, figure8State)
    trans.addAnimation(group)

    trans = rootState.addTransition(randomButton.pressed, randomState)
    trans.addAnimation(group)

    trans = rootState.addTransition(tiledButton.pressed, tiledState)
    trans.addAnimation(group)

    trans = rootState.addTransition(centeredButton.pressed, centeredState)
    trans.addAnimation(group)

    timer = QtCore.QTimer()
    timer.start(125)
    timer.setSingleShot(True)
    trans = rootState.addTransition(timer.timeout, ellipseState)
    trans.addAnimation(group)

    states.start()

    sys.exit(app.exec_())
