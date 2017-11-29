#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2006-2006 Trolltech ASA. All rights reserved.
##
## This file is part of the example classes of the Qt Toolkit.
##
## This file may be used under the terms of the GNU General Public
## License version 2.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http://www.trolltech.com/products/qt/opensource.html
##
## If you are unsure which license is appropriate for your use, please
## review the following information:
## http://www.trolltech.com/products/qt/licensing.html or contact the
## sales department at sales@trolltech.com.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
##
############################################################################

import sys
import math
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtOpenGL import *

try:
    from OpenGL import GL
except ImportError:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "OpenGL 2dpainting",
                            "PyOpenGL must be installed to run this example.",
                            QMessageBox.Ok | QMessageBox.Default,
                            QMessageBox.NoButton)
    sys.exit(1)


class Helper:
    def __init__(self):
        gradient = QLinearGradient(QPointF(50, -20), QPointF(80, 20))
        gradient.setColorAt(0.0, Qt.white)
        gradient.setColorAt(1.0, QColor(0xa6, 0xce, 0x39))

        self.background = QBrush(QColor(64, 32, 64))
        self.circleBrush = QBrush(gradient)
        self.circlePen = QPen(Qt.black)
        self.circlePen.setWidth(1)
        self.textPen = QPen(Qt.white)
        self.textFont = QFont()
        self.textFont.setPixelSize(50)

    def paint(self, painter, event, elapsed):
        painter.fillRect(event.rect(), self.background)
        painter.translate(100, 100)

        painter.save()
        painter.setBrush(self.circleBrush)
        painter.setPen(self.circlePen)
        painter.rotate(elapsed * 0.030)

        r = elapsed/1000.0
        n = 30
        for i in range(n):
            painter.rotate(30)
            radius = 0 + 120.0*((i+r)/n)
            circleRadius = 1 + ((i+r)/n)*20
            painter.drawEllipse(QRectF(radius, -circleRadius,
                                       circleRadius*2, circleRadius*2))

        painter.restore()

        painter.setPen(self.textPen)
        painter.setFont(self.textFont)
        painter.drawText(QRect(-50, -50, 100, 100), Qt.AlignCenter, "Qt")


class Widget(QWidget):
    def __init__(self, helper, parent = None):
        QWidget.__init__(self, parent)

        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()


class GLWidget(QGLWidget):
    def __init__(self, helper, parent = None):
        QGLWidget.__init__(self, QGLFormat(QGL.SampleBuffers), parent)

        self.helper = helper
        self.elapsed = 0
        self.setFixedSize(200, 200)

    def animate(self):
        self.elapsed = (self.elapsed + self.sender().interval()) % 1000
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.helper.paint(painter, event, self.elapsed)
        painter.end()


class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        helper = Helper()
        native = Widget(helper, self)
        openGL = GLWidget(helper, self)
        nativeLabel = QLabel(self.tr("Native"))
        nativeLabel.setAlignment(Qt.AlignHCenter)
        openGLLabel = QLabel(self.tr("OpenGL"))
        openGLLabel.setAlignment(Qt.AlignHCenter)

        layout = QGridLayout()
        layout.addWidget(native, 0, 0)
        layout.addWidget(openGL, 0, 1)
        layout.addWidget(nativeLabel, 1, 0)
        layout.addWidget(openGLLabel, 1, 1)
        self.setLayout(layout)

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), native.animate)
        self.connect(timer, SIGNAL("timeout()"), openGL.animate)
        timer.start(50)

        self.setWindowTitle(self.tr("2D Painting on Native and OpenGL Widgets"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
