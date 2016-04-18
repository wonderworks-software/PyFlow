#!/usr/bin/env python

"""PySide port of the opengl/samplebuffers example from Qt v4.x"""

import sys
import math
from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL samplebuffers",
                            "PyOpenGL must be installed to run this example.",
                            QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default,
                            QtGui.QMessageBox.NoButton)
    sys.exit(1)


class GLWidget(QtOpenGL.QGLWidget):
    GL_MULTISAMPLE = 0x809D
    rot = 0.0

    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers), parent)

        self.list_ = []

        self.startTimer(40)
        self.setWindowTitle(self.tr("Sample Buffers"))

    def initializeGL(self):
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho( -.5, .5, .5, -.5, -1000, 1000)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClearColor(1.0, 1.0, 1.0, 1.0)

        self.makeObject()

    def resizeGL(self, w, h):
        GL.glViewport(0, 0, w, h)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glPushMatrix()
        GL.glEnable(GLWidget.GL_MULTISAMPLE)
        GL.glTranslatef( -0.25, -0.10, 0.0)
        GL.glScalef(0.75, 1.15, 0.0)
        GL.glRotatef(GLWidget.rot, 0.0, 0.0, 1.0)
        GL.glCallList(self.list_)
        GL.glPopMatrix()

        GL.glPushMatrix()
        GL.glDisable(GLWidget.GL_MULTISAMPLE)
        GL.glTranslatef(0.25, -0.10, 0.0)
        GL.glScalef(0.75, 1.15, 0.0)
        GL.glRotatef(GLWidget.rot, 0.0, 0.0, 1.0)
        GL.glCallList(self.list_)
        GL.glPopMatrix()

        GLWidget.rot += 0.2

        self.qglColor(QtCore.Qt.black)
        self.renderText(-0.35, 0.4, 0.0, "Multisampling enabled")
        self.renderText(0.15, 0.4, 0.0, "Multisampling disabled")

    def timerEvent(self, event):
        self.update()

    def makeObject(self):
        trolltechGreen = QtGui.QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        Pi = 3.14159265358979323846
        NumSectors = 15
        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.list_ = GL.glGenLists(1)
        GL.glNewList(self.list_, GL.GL_COMPILE)

        for i in range(NumSectors):
            angle1 = float((i * 2 * Pi) / NumSectors)
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = float(((i + 1) * 2 * Pi) / NumSectors)
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.qglColor(trolltechGreen)
            self.quad(GL.GL_QUADS, x5, y5, x6, y6, x7, y7, x8, y8)
            self.qglColor(QtCore.Qt.black)
            self.quad(GL.GL_LINE_LOOP, x5, y5, x6, y6, x7, y7, x8, y8)

        self.qglColor(trolltechGreen)
        self.quad(GL.GL_QUADS, x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(GL.GL_QUADS, x3, y3, x4, y4, y4, x4, y3, x3)

        self.qglColor(QtCore.Qt.black)
        self.quad(GL.GL_LINE_LOOP, x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(GL.GL_LINE_LOOP, x3, y3, x4, y4, y4, x4, y3, x3)

        GL.glEndList()

    def quad(self, primitive, x1, y1, x2, y2, x3, y3, x4, y4):
        GL.glBegin(primitive)

        GL.glVertex2d(x1, y1)
        GL.glVertex2d(x2, y2)
        GL.glVertex2d(x3, y3)
        GL.glVertex2d(x4, y4)

        GL.glEnd()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    if not QtOpenGL.QGLFormat.hasOpenGL():
        QMessageBox.information(0, "OpenGL pbuffers",
                                "This system does not support OpenGL.",
                                QMessageBox.Ok)
        sys.exit(1)

    f = QtOpenGL.QGLFormat.defaultFormat()
    f.setSampleBuffers(True)
    QtOpenGL.QGLFormat.setDefaultFormat(f)

    widget = GLWidget()
    widget.resize(640, 480)
    widget.show()

    sys.exit(app.exec_())
