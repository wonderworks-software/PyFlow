#!/usr/bin/env python

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PySide import QtCore, QtGui


class CircleWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.floatBased = False
        self.antialiased = False
        self.frameNo = 0

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Expanding)

    def setFloatBased(self, floatBased):
        self.floatBased = floatBased
        self.update()

    def setAntialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(180, 180)

    def nextAnimationFrame(self):
        self.frameNo += 1
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, self.antialiased)
        painter.translate(self.width() / 2, self.height() / 2)

        for diameter in range(0, 256, 9):
            delta = abs((self.frameNo % 128) - diameter / 2)
            alpha = 255 - (delta * delta) / 4 - diameter
            if alpha > 0:
                painter.setPen(QtGui.QPen(QtGui.QColor(0, diameter / 2, 127, alpha), 3))

                if self.floatBased:
                    painter.drawEllipse(QtCore.QRectF(-diameter / 2.0, -diameter / 2.0,
                                                      diameter, diameter))
                else:
                    painter.drawEllipse(QtCore.QRect(-diameter / 2, -diameter / 2,
                                                     diameter, diameter))

        painter.end()


class Window(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.aliasedLabel = self.createLabel(self.tr("Aliased"))
        self.antialiasedLabel = self.createLabel(self.tr("Antialiased"))
        self.intLabel = self.createLabel(self.tr("Int"))
        self.floatLabel = self.createLabel(self.tr("Float"))

        layout = QtGui.QGridLayout()
        layout.addWidget(self.aliasedLabel, 0, 1)
        layout.addWidget(self.antialiasedLabel, 0, 2)
        layout.addWidget(self.intLabel, 1, 0)
        layout.addWidget(self.floatLabel, 2, 0)

        timer = QtCore.QTimer(self)

        self.circleWidgets = []
        for i in range(2):
            self.circleWidgets.append([None]*2)
            for j in range(2):
                self.circleWidgets[i][j] = CircleWidget()
                self.circleWidgets[i][j].setAntialiased(j != 0)
                self.circleWidgets[i][j].setFloatBased(i != 0)

                self.connect(timer, QtCore.SIGNAL("timeout()"),
                             self.circleWidgets[i][j].nextAnimationFrame)

                layout.addWidget(self.circleWidgets[i][j], i + 1, j + 1)

        timer.start(100)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Concentric Circles"))

    def createLabel(self, text):
        label = QtGui.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMargin(2)
        label.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Sunken)
        return label


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
