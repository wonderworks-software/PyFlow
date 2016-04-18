#!/usr/bin/env python

"""PyQt4 port of the demos/embeddeddialogs example from Qt v4.x"""

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)

from PySide import QtCore, QtGui

from embeddeddialog import Ui_embeddedDialog
from embeddeddialogs_rc import *


class CustomProxy(QtGui.QGraphicsProxyWidget):
    def __init__(self, parent=None, wFlags=0):
        super(CustomProxy, self).__init__(parent, wFlags)

        self.popupShown = False
        self.timeLine = QtCore.QTimeLine(250, self)
        self.timeLine.valueChanged.connect(self.updateStep)
        self.timeLine.stateChanged.connect(self.stateChanged)

    def boundingRect(self):
        return QtGui.QGraphicsProxyWidget.boundingRect(self).adjusted(0, 0, 10, 10)

    def paintWindowFrame(self, painter, option, widget):
        color = QtGui.QColor(0, 0, 0, 64)

        r = self.windowFrameRect()
        right = QtCore.QRectF(r.right(), r.top()+10, 10, r.height()-10)
        bottom = QtCore.QRectF(r.left()+10, r.bottom(), r.width(), 10)
        intersectsRight = right.intersects(option.exposedRect)
        intersectsBottom = bottom.intersects(option.exposedRect)
        if intersectsRight and intersectsBottom:
            path=QtGui.QPainterPath()
            path.addRect(right)
            path.addRect(bottom)
            painter.setPen(QtCore.Qt.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)
        elif intersectsBottom:
            painter.fillRect(bottom, color)
        elif intersectsRight:
            painter.fillRect(right, color)

        super(CustomProxy, self).paintWindowFrame(painter, option, widget)

    def hoverEnterEvent(self, event):
        super(CustomProxy, self).hoverEnterEvent(event)

        self.scene().setActiveWindow(self)
        if self.timeLine.currentValue != 1:
            self.zoomIn()

    def hoverLeaveEvent(self, event):
        super(CustomProxy, self).hoverLeaveEvent(event)

        if not self.popupShown and (self.timeLine.direction() != QtCore.QTimeLine.Backward or self.timeLine.currentValue() != 0):
            self.zoomOut()

    def sceneEventFilter(self, watched, event):
        if watched.isWindow() and (event.type() == QtCore.QEvent.UngrabMouse or event.type() == QtCore.QEvent.GrabMouse):
            self.popupShown = watched.isVisible()
            if not self.popupShown and not self.isUnderMouse():
                self.zoomOut()

        return super(CustomProxy, self).sceneEventFilter(watched, event)

    def itemChange(self, change, value):
        if change == self.ItemChildAddedChange or change == self.ItemChildRemovedChange :
            # how to translate this line to python?
            # QGraphicsItem *item = qVariantValue<QGraphicsItem *>(value);
            item = value
            try:
                if change == self.ItemChildAddedChange:
                    item.installSceneEventFilter(self)
                else:
                    item.removeSceneEventFilter(self)
            except:
                pass

        return super(CustomProxy, self).itemChange(change, value)

    def updateStep(self, step):
        r=self.boundingRect()
        self.setTransform( QtGui.QTransform() \
                            .translate(r.width() / 2, r.height() / 2)\
                            .rotate(step * 30, QtCore.Qt.XAxis)\
                            .rotate(step * 10, QtCore.Qt.YAxis)\
                            .rotate(step * 5, QtCore.Qt.ZAxis)\
                            .scale(1 + 1.5 * step, 1 + 1.5 * step)\
                            .translate(-r.width() / 2, -r.height() / 2))

    def stateChanged(self, state):
        if state == QtCore.QTimeLine.Running:
            if self.timeLine.direction() == QtCore.QTimeLine.Forward:
                self.setCacheMode(self.NoCache)
            elif state == QtCore.QTimeLine.NotRunning:
                if self.timeLine.direction() == QtCore.QTimeLine.Backward:
                    self.setCacheMode(self.DeviceCoordinateCache)

    def zoomIn(self):
        if self.timeLine.direction() != QtCore.QTimeLine.Forward:
            self.timeLine.setDirection(QtCore.QTimeLine.Forward)
        if self.timeLine.state() == QtCore.QTimeLine.NotRunning:
            self.timeLine.start()

    def zoomOut(self):
        if self.timeLine.direction() != QtCore.QTimeLine.Backward:
            self.timeLine.setDirection(QtCore.QTimeLine.Backward)
        if self.timeLine.state() == QtCore.QTimeLine.NotRunning:
            self.timeLine.start()


class EmbeddedDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(EmbeddedDialog, self).__init__(parent)

        self.ui = Ui_embeddedDialog()
        self.ui.setupUi(self)
        self.ui.layoutDirection.setCurrentIndex(self.layoutDirection() != QtCore.Qt.LeftToRight)

        for styleName in QtGui.QStyleFactory.keys():
            self.ui.style.addItem(styleName)
            if self.style().objectName().lower() == styleName.lower():
                self.ui.style.setCurrentIndex(self.ui.style.count() -1)

        self.ui.layoutDirection.activated.connect(self.layoutDirectionChanged)
        self.ui.spacing.valueChanged.connect(self.spacingChanged)
        self.ui.fontComboBox.currentFontChanged.connect(self.fontChanged)
        self.ui.style.activated[str].connect(self.styleChanged)

    def layoutDirectionChanged(self, index):
        if index == 0:
            self.setLayoutDirection(QtCore.Qt.LeftToRight)
        else:
            self.setLayoutDirection(QtCore.Qt.RightToLeft)

    def spacingChanged(self, spacing):
        self.layout().setSpacing(spacing)
        self.adjustSize()

    def fontChanged(self, font):
        self.setFont(font)

    def setStyleHelper(self, widget, style):
        widget.setStyle(style)
        widget.setPalette(style.standardPalette())
        for child in widget.children():
            if isinstance(child, QtGui.QWidget):
                self.setStyleHelper(child, style)
    
    def styleChanged(self, styleName):
        style=QtGui.QStyleFactory.create(styleName)
        if style:
            self.setStyleHelper(self, style)

        # Keep a reference to the style.
        self._style = style


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    scene = QtGui.QGraphicsScene()
    for y in range(10):
        for x in range(10):
            proxy = CustomProxy(None, QtCore.Qt.Window)
            proxy.setWidget(EmbeddedDialog())

            rect = proxy.boundingRect()

            proxy.setPos( x * rect.width()*1.05, y*rect.height()*1.05 )
            proxy.setCacheMode(QtGui.QGraphicsItem.DeviceCoordinateCache)
            scene.addItem(proxy)

    scene.setSceneRect(scene.itemsBoundingRect())

    view = QtGui.QGraphicsView(scene)
    view.scale(0.5, 0.5)
    view.setRenderHints(view.renderHints() | QtGui.QPainter.Antialiasing  | QtGui.QPainter.SmoothPixmapTransform)
    view.setBackgroundBrush(QtGui.QBrush(QtGui.QPixmap(':/No-Ones-Laughing-3.jpg')))
    view.setCacheMode(QtGui.QGraphicsView.CacheBackground)
    view.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
    view.show()
    view.setWindowTitle("Embedded Dialogs Demo")

    sys.exit(app.exec_())
