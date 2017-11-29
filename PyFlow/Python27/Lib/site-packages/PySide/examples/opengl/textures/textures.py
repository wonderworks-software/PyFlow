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
from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL.GL import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL textures",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)

import textures_rc


class GLWidget(QtOpenGL.QGLWidget):
    sharedObject = 0
    refCount = 0

    coords = (
        ( ( +1, -1, -1 ), ( -1, -1, -1 ), ( -1, +1, -1 ), ( +1, +1, -1 ) ),
        ( ( +1, +1, -1 ), ( -1, +1, -1 ), ( -1, +1, +1 ), ( +1, +1, +1 ) ),
        ( ( +1, -1, +1 ), ( +1, -1, -1 ), ( +1, +1, -1 ), ( +1, +1, +1 ) ),
        ( ( -1, -1, -1 ), ( -1, -1, +1 ), ( -1, +1, +1 ), ( -1, +1, -1 ) ),
        ( ( +1, -1, +1 ), ( -1, -1, +1 ), ( -1, -1, -1 ), ( +1, -1, -1 ) ),
        ( ( -1, -1, +1 ), ( +1, -1, +1 ), ( +1, +1, +1 ), ( -1, +1, +1 ) )
    )

    clicked = QtCore.Signal()

    def __init__(self, parent, shareWidget):
        QtOpenGL.QGLWidget.__init__(self, parent, shareWidget)

        self.clearColor = QtCore.Qt.black
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.clearColor = QtGui.QColor()
        self.lastPos = QtCore.QPoint()

    def freeGLResources(self):
        GLWidget.refCount -= 1
        if GLWidget.refCount == 0:
            self.makeCurrent()
            glDeleteLists(self.__class__.sharedObject, 1)

    def minimumSizeHint(self):
        return QtCore.QSize(50, 50)

    def sizeHint(self):
        return QtCore.QSize(200, 200)

    def rotateBy(self, xAngle, yAngle, zAngle):
        self.xRot = (self.xRot + xAngle) % 5760
        self.yRot = (self.yRot + yAngle) % 5760
        self.zRot = (self.zRot + zAngle) % 5760
        self.updateGL()

    def setClearColor(self, color):
        self.clearColor = color
        self.updateGL()

    def initializeGL(self):
        if not GLWidget.sharedObject:
            self.textures = []
            for i in range(6):
                self.textures.append(self.bindTexture(QtGui.QPixmap(":/images/side%d.png" % (i + 1))))
            GLWidget.sharedObject = self.makeObject()
        GLWidget.refCount += 1

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_TEXTURE_2D)

    def paintGL(self):
        self.qglClearColor(self.clearColor)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -10.0)
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        glCallList(GLWidget.sharedObject)

    def resizeGL(self, width, height):
        side = min(width, height)
        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        glMatrixMode(GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = QtCore.QPoint(event.pos())

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.rotateBy(8 * dy, 8 * dx, 0)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.rotateBy(8 * dy, 0, 8 * dx)

        self.lastPos = QtCore.QPoint(event.pos())

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def makeObject(self):
        dlist = glGenLists(1)
        glNewList(dlist, GL_COMPILE)

        for i in range(6):
            glBindTexture(GL_TEXTURE_2D, self.textures[i])

            glBegin(GL_QUADS)
            for j in range(4):
                tx = {False: 0, True: 1}[j == 0 or j == 3]
                ty = {False: 0, True: 1}[j == 0 or j == 1]
                glTexCoord2d(tx, ty)
                glVertex3d(0.2 * GLWidget.coords[i][j][0],
                           0.2 * GLWidget.coords[i][j][1],
                           0.2 * GLWidget.coords[i][j][2])

            glEnd()

        glEndList()
        return dlist


class Window(QtGui.QWidget):
    NumRows = 2
    NumColumns = 3

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        mainLayout = QtGui.QGridLayout()
        self.glWidgets = []

        for i in range(Window.NumRows):
            self.glWidgets.append([])
            for j in range(Window.NumColumns):
                self.glWidgets[i].append(None)

        for i in range(Window.NumRows):
            for j in range(Window.NumColumns):
                clearColor = QtGui.QColor()
                clearColor.setHsv(((i * Window.NumColumns) + j) * 255
                                  / (Window.NumRows * Window.NumColumns - 1),
                                  255, 63)

                self.glWidgets[i][j] = GLWidget(self, self.glWidgets[0][0])
                self.glWidgets[i][j].setClearColor(clearColor)
                self.glWidgets[i][j].rotateBy(+42 * 16, +42 * 16, -21 * 16)
                mainLayout.addWidget(self.glWidgets[i][j], i, j)

                self.glWidgets[i][j].clicked.connect(self.setCurrentGlWidget)
                QtGui.qApp.lastWindowClosed.connect(self.glWidgets[i][j].freeGLResources)

        self.setLayout(mainLayout)

        self.currentGlWidget = self.glWidgets[0][0]

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.rotateOneStep)
        timer.start(20)

        self.setWindowTitle(self.tr("Textures"))

    def setCurrentGlWidget(self):
        self.currentGlWidget = self.sender()

    def rotateOneStep(self):
        if self.currentGlWidget:
            self.currentGlWidget.rotateBy(+2 * 16, +2 * 16, -1 * 16)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
