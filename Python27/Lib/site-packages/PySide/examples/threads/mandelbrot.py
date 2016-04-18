#!/usr/bin/env python

############################################################################
#
#  Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
#
#  This file is part of the example classes of the Qt Toolkit.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file LICENSE.GPL included in the packaging of
#  self file.  Please review the following information to ensure GNU
#  General Public Licensing requirements will be met:
#  http://www.trolltech.com/products/qt/opensource.html
#
#  If you are unsure which license is appropriate for your use, please
#  review the following information:
#  http://www.trolltech.com/products/qt/licensing.html or contact the
#  sales department at sales@trolltech.com.
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
############################################################################

import sys
from PySide import QtCore, QtGui


DefaultCenterX = -0.647011
DefaultCenterY = -0.0395159
DefaultScale = 0.00403897

ZoomInFactor = 0.8
ZoomOutFactor = 1 / ZoomInFactor
ScrollStep = 20


class RenderThread(QtCore.QThread):
    ColormapSize = 512

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.mutex = QtCore.QMutex()
        self.condition = QtCore.QWaitCondition()
        self.centerX = 0.0
        self.centerY = 0.0
        self.scaleFactor = 0.0
        self.resultSize = QtCore.QSize()
        self.colormap = []

        self.restart = False
        self.abort = False

        for i in range(RenderThread.ColormapSize):
            self.colormap.append(self.rgbFromWaveLength(380.0 + (i * 400.0 / RenderThread.ColormapSize)))

    def stop(self):
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()

        self.wait()

    def render(self, centerX, centerY, scaleFactor, resultSize):
        locker = QtCore.QMutexLocker(self.mutex)

        self.centerX = centerX
        self.centerY = centerY
        self.scaleFactor = scaleFactor
        self.resultSize = resultSize

        if not self.isRunning():
            self.start(QtCore.QThread.LowPriority)
        else:
            self.restart = True
            self.condition.wakeOne()

    def run(self):
        while True:
            self.mutex.lock()
            resultSize = self.resultSize
            scaleFactor = self.scaleFactor
            centerX = self.centerX
            centerY = self.centerY
            self.mutex.unlock()

            halfWidth = int(resultSize.width() / 2)
            halfHeight = int(resultSize.height() / 2)
            image = QtGui.QImage(resultSize, QtGui.QImage.Format_RGB32)

            NumPasses = 8
            curpass = 0

            while curpass < NumPasses:
                MaxIterations = (1 << (2 * curpass + 6)) + 32
                Limit = 4
                allBlack = True

                for y in range(-halfHeight, halfHeight):
                    if self.restart:
                        break
                    if self.abort:
                        return

                    ay = 1j * (centerY + (y * scaleFactor))

                    for x in range(-halfWidth, halfWidth):
                        c0 = centerX + (x * scaleFactor) + ay
                        c = c0
                        numIterations = 0

                        while numIterations < MaxIterations:
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break
                            numIterations += 1
                            c = c*c + c0
                            if abs(c) >= Limit:
                                break

                        if numIterations < MaxIterations:
                            image.setPixel(x + halfWidth, y + halfHeight,
                                           self.colormap[numIterations % RenderThread.ColormapSize])
                            allBlack = False
                        else:
                            image.setPixel(x + halfWidth, y + halfHeight, QtGui.qRgb(0, 0, 0))

                if allBlack and curpass == 0:
                    curpass = 4
                else:
                    if not self.restart:
                        self.emit(QtCore.SIGNAL("renderedImage(const QImage &, double)"), image, scaleFactor)
                    curpass += 1

            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()

    def rgbFromWaveLength(self, wave):
        r = 0.0
        g = 0.0
        b = 0.0

        if wave >= 380.0 and wave <= 440.0:
            r = -1.0 * (wave - 440.0) / (440.0 - 380.0)
            b = 1.0
        elif wave >= 440.0 and wave <= 490.0:
            g = (wave - 440.0) / (490.0 - 440.0)
            b = 1.0
        elif wave >= 490.0 and wave <= 510.0:
            g = 1.0
            b = -1.0 * (wave - 510.0) / (510.0 - 490.0)
        elif wave >= 510.0 and wave <= 580.0:
            r = (wave - 510.0) / (580.0 - 510.0)
            g = 1.0
        elif wave >= 580.0 and wave <= 645.0:
            r = 1.0
            g = -1.0 * (wave - 645.0) / (645.0 - 580.0)
        elif wave >= 645.0 and wave <= 780.0:
            r = 1.0

        s = 1.0
        if wave > 700.0:
            s = 0.3 + 0.7 * (780.0 - wave) / (780.0 - 700.0)
        elif wave < 420.0:
            s = 0.3 + 0.7 * (wave - 380.0) / (420.0 - 380.0)

        r = pow(r * s, 0.8)
        g = pow(g * s, 0.8)
        b = pow(b * s, 0.8)

        return QtGui.qRgb(int(r*255), int(g*255), int(b*255))


class MandelbrotWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.thread = RenderThread()
        self.pixmap = QtGui.QPixmap()
        self.pixmapOffset = QtCore.QPoint()
        self.lastDragPos = QtCore.QPoint()

        self.centerX = DefaultCenterX
        self.centerY = DefaultCenterY
        self.pixmapScale = DefaultScale
        self.curScale = DefaultScale

        self.connect(self.thread,
                     QtCore.SIGNAL("renderedImage(const QImage &, double)"),
                     self.updatePixmap)

        self.setWindowTitle(self.tr("Mandelbrot"))
        self.setCursor(QtCore.Qt.CrossCursor)
        self.resize(550, 400)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)

        if self.pixmap.isNull():
            painter.setPen(QtCore.Qt.white)
            painter.drawText(self.rect(), QtCore.Qt.AlignCenter,
                             self.tr("Rendering initial image, please wait..."))
            return

        if self.curScale == self.pixmapScale:
            painter.drawPixmap(self.pixmapOffset, self.pixmap)
        else:
            scaleFactor = self.pixmapScale / self.curScale
            newWidth = int(self.pixmap.width() * scaleFactor)
            newHeight = int(self.pixmap.height() * scaleFactor)
            newX = self.pixmapOffset.x() + (self.pixmap.width() - newWidth) / 2
            newY = self.pixmapOffset.y() + (self.pixmap.height() - newHeight) / 2

            painter.save()
            painter.translate(newX, newY)
            painter.scale(scaleFactor, scaleFactor)
            painter.drawPixmap(0, 0, self.pixmap)
            painter.restore()

        text = self.tr("Use mouse wheel to zoom. "
                       "Press and hold left mouse button to scroll.")
        metrics = painter.fontMetrics()
        textWidth = metrics.width(text)

        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QColor(0, 0, 0, 127))
        painter.drawRect((self.width() - textWidth) / 2 - 5, 0, textWidth + 10,
                         metrics.lineSpacing() + 5)
        painter.setPen(QtCore.Qt.white)
        painter.drawText((self.width() - textWidth) / 2,
                         metrics.leading() + metrics.ascent(), text)

    def resizeEvent(self, event):
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Plus:
            self.zoom(ZoomInFactor)
        elif event.key() == QtCore.Qt.Key_Minus:
            self.zoom(ZoomOutFactor)
        elif event.key() == QtCore.Qt.Key_Left:
            self.scroll(-ScrollStep, 0)
        elif event.key() == QtCore.Qt.Key_Right:
            self.scroll(+ScrollStep, 0)
        elif event.key() == QtCore.Qt.Key_Down:
            self.scroll(0, -ScrollStep)
        elif event.key() == QtCore.Qt.Key_Up:
            self.scroll(0, +ScrollStep)
        else:
            QtGui.QWidget.keyPressEvent(self, event)

    def wheelEvent(self, event):
        numDegrees = event.delta() / 8
        numSteps = numDegrees / 15.0
        self.zoom(pow(ZoomInFactor, numSteps))

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.lastDragPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QtCore.QPoint(event.pos())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.pixmapOffset += event.pos() - self.lastDragPos
            self.lastDragPos = QtCore.QPoint()

            deltaX = (self.width() - self.pixmap.width()) / 2 - self.pixmapOffset.x()
            deltaY = (self.height() - self.pixmap.height()) / 2 - self.pixmapOffset.y()
            self.scroll(deltaX, deltaY)

    def updatePixmap(self, image, scaleFactor):
        if not self.lastDragPos.isNull():
            return

        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.pixmapOffset = QtCore.QPoint()
        self.lastDragPosition = QtCore.QPoint()
        self.pixmapScale = scaleFactor
        self.update()

    def zoom(self, zoomFactor):
        self.curScale *= zoomFactor
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())

    def scroll(self, deltaX, deltaY):
        self.centerX += deltaX * self.curScale
        self.centerY += deltaY * self.curScale
        self.update()
        self.thread.render(self.centerX, self.centerY, self.curScale, self.size())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MandelbrotWidget()
    widget.show()
    r = app.exec_()
    widget.thread.stop()
    sys.exit(r)
