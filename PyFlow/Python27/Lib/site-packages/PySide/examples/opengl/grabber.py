#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2004-2005 Trolltech AS. All rights reserved.
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
#############################################################################

import sys
import math

from PySide import QtCore, QtGui, QtOpenGL

try:
    from OpenGL.GL import *
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL grabber",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)


class GLWidget(QtOpenGL.QGLWidget):
    xRotationChanged = QtCore.Signal(int)
    yRotationChanged = QtCore.Signal(int)
    zRotationChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

        self.gear1 = 0
        self.gear2 = 0
        self.gear3 = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0
        self.gear1Rot = 0

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.advanceGears)
        timer.start(20)

    def __del__(self):
        self.makeCurrent()
        glDeleteLists(self.gear1, 1)
        glDeleteLists(self.gear2, 1)
        glDeleteLists(self.gear3, 1)

    def setXRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.updateGL()

    def setYRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.updateGL()

    def setZRotation(self, angle):
        self.normalizeAngle(angle)

        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.updateGL()

    def initializeGL(self):
        lightPos = (5.0, 5.0, 10.0, 1.0)
        reflectance1 = (0.8, 0.1, 0.0, 1.0)
        reflectance2 = (0.0, 0.8, 0.2, 1.0)
        reflectance3 = (0.2, 0.2, 1.0, 1.0)

        glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)

        self.gear1 = self.makeGear(reflectance1, 1.0, 4.0, 1.0, 0.7, 20)
        self.gear2 = self.makeGear(reflectance2, 0.5, 2.0, 2.0, 0.7, 10)
        self.gear3 = self.makeGear(reflectance3, 1.3, 2.0, 0.5, 0.7, 10)

        glEnable(GL_NORMALIZE)
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)

        self.drawGear(self.gear1, -3.0, -2.0, 0.0, self.gear1Rot / 16.0)
        self.drawGear(self.gear2, +3.1, -2.0, 0.0,
                -2.0 * (self.gear1Rot / 16.0) - 9.0)

        glRotated(+90.0, 1.0, 0.0, 0.0)
        self.drawGear(self.gear3, -3.1, -1.8, -2.2,
                +2.0 * (self.gear1Rot / 16.0) - 2.0)

        glPopMatrix()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        glViewport((width - side) / 2, (height - side) / 2, side, side)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-1.0, +1.0, -1.0, 1.0, 5.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -40.0)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & QtCore.Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & QtCore.Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def advanceGears(self):
        self.gear1Rot += 2 * 16
        self.updateGL()    

    def xRotation(self):
        return self.xRot

    def yRotation(self):
        return self.yRot

    def zRotation(self):
        return self.zRot

    def makeGear(self, reflectance, innerRadius, outerRadius, thickness, toothSize, toothCount):
        list = glGenLists(1)
        glNewList(list, GL_COMPILE)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, reflectance)

        r0 = innerRadius
        r1 = outerRadius - toothSize / 2.0
        r2 = outerRadius + toothSize / 2.0
        delta = (2.0 * math.pi / toothCount) / 4.0
        z = thickness / 2.0

        glShadeModel(GL_FLAT)

        for i in range(2):
            if i == 0:
                sign = +1.0
            else:
                sign = -1.0

            glNormal3d(0.0, 0.0, sign)

            glBegin(GL_QUAD_STRIP)

            for j in range(toothCount+1):
                angle = 2.0 * math.pi * j / toothCount
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

            glBegin(GL_QUADS)

            for j in range(toothCount):
                angle = 2.0 * math.pi * j / toothCount                
                glVertex3d(r1 * math.cos(angle), r1 * math.sin(angle), sign * z)
                glVertex3d(r2 * math.cos(angle + delta), r2 * math.sin(angle + delta), sign * z)
                glVertex3d(r2 * math.cos(angle + 2 * delta), r2 * math.sin(angle + 2 * delta), sign * z)
                glVertex3d(r1 * math.cos(angle + 3 * delta), r1 * math.sin(angle + 3 * delta), sign * z)

            glEnd()

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount):
            for j in range(2):
                angle = 2.0 * math.pi * (i + (j / 2.0)) / toothCount
                s1 = r1
                s2 = r2

                if j == 1:
                    s1, s2 = s2, s1

                glNormal3d(math.cos(angle), math.sin(angle), 0.0)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), +z)
                glVertex3d(s1 * math.cos(angle), s1 * math.sin(angle), -z)

                glNormal3d(s2 * math.sin(angle + delta) - s1 * math.sin(angle), s1 * math.cos(angle) - s2 * math.cos(angle + delta), 0.0)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), +z)
                glVertex3d(s2 * math.cos(angle + delta), s2 * math.sin(angle + delta), -z)

        glVertex3d(r1, 0.0, +z)
        glVertex3d(r1, 0.0, -z)
        glEnd()

        glShadeModel(GL_SMOOTH)

        glBegin(GL_QUAD_STRIP)

        for i in range(toothCount+1):
            angle = i * 2.0 * math.pi / toothCount
            glNormal3d(-math.cos(angle), -math.sin(angle), 0.0)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), +z)
            glVertex3d(r0 * math.cos(angle), r0 * math.sin(angle), -z)

        glEnd()

        glEndList()

        return list    

    def drawGear(self, gear, dx, dy, dz, angle):
        glPushMatrix()
        glTranslated(dx, dy, dz)
        glRotated(angle, 0.0, 0.0, 1.0)
        glCallList(gear)
        glPopMatrix()

    def normalizeAngle(self, angle):
        while (angle < 0):
            angle += 360 * 16

        while (angle > 360 * 16):
            angle -= 360 * 16


class MainWindow(QtGui.QMainWindow):
    def __init__(self):        
        super(MainWindow, self).__init__()

        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)

        self.glWidget = GLWidget()
        self.pixmapLabel = QtGui.QLabel()

        self.glWidgetArea = QtGui.QScrollArea()
        self.glWidgetArea.setWidget(self.glWidget)
        self.glWidgetArea.setWidgetResizable(True)
        self.glWidgetArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.glWidgetArea.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.glWidgetArea.setMinimumSize(50, 50)

        self.pixmapLabelArea = QtGui.QScrollArea()
        self.pixmapLabelArea.setWidget(self.pixmapLabel)
        self.pixmapLabelArea.setSizePolicy(QtGui.QSizePolicy.Ignored,
                QtGui.QSizePolicy.Ignored)
        self.pixmapLabelArea.setMinimumSize(50, 50)

        xSlider = self.createSlider(self.glWidget.xRotationChanged,
                self.glWidget.setXRotation)
        ySlider = self.createSlider(self.glWidget.yRotationChanged,
                self.glWidget.setYRotation)
        zSlider = self.createSlider(self.glWidget.zRotationChanged,
                self.glWidget.setZRotation)

        self.createActions()
        self.createMenus()

        centralLayout = QtGui.QGridLayout()
        centralLayout.addWidget(self.glWidgetArea, 0, 0)
        centralLayout.addWidget(self.pixmapLabelArea, 0, 1)
        centralLayout.addWidget(xSlider, 1, 0, 1, 2)
        centralLayout.addWidget(ySlider, 2, 0, 1, 2)
        centralLayout.addWidget(zSlider, 3, 0, 1, 2)
        centralWidget.setLayout(centralLayout)

        xSlider.setValue(15 * 16)
        ySlider.setValue(345 * 16)
        zSlider.setValue(0 * 16)

        self.setWindowTitle("Grabber")
        self.resize(400, 300)

    def renderIntoPixmap(self):
        size = self.getSize()

        if size.isValid():
            pixmap = self.glWidget.renderPixmap(size.width(), size.height())
            self.setPixmap(pixmap)

    def grabFrameBuffer(self):
        image = self.glWidget.grabFrameBuffer()
        self.setPixmap(QtGui.QPixmap.fromImage(image))

    def clearPixmap(self):
        self.setPixmap(QtGui.QPixmap())

    def about(self):
        QtGui.QMessageBox.about(self, "About Grabber",
                "The <b>Grabber</b> example demonstrates two approaches for "
                "rendering OpenGL into a Qt pixmap.")

    def createActions(self):
        self.renderIntoPixmapAct = QtGui.QAction("&Render into Pixmap...",
                self, shortcut="Ctrl+R", triggered=self.renderIntoPixmap)

        self.grabFrameBufferAct = QtGui.QAction("&Grab Frame Buffer", self,
                shortcut="Ctrl+G", triggered=self.grabFrameBuffer)

        self.clearPixmapAct = QtGui.QAction("&Clear Pixmap", self,
                shortcut="Ctrl+L", triggered=self.clearPixmap)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.renderIntoPixmapAct)
        self.fileMenu.addAction(self.grabFrameBufferAct)
        self.fileMenu.addAction(self.clearPixmapAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createSlider(self, changedSignal, setterSlot):
        slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 360 * 16)
        slider.setSingleStep(16)
        slider.setPageStep(15 * 16)
        slider.setTickInterval(15 * 16)
        slider.setTickPosition(QtGui.QSlider.TicksRight)

        slider.valueChanged.connect(setterSlot)
        changedSignal.connect(slider.setValue)

        return slider

    def setPixmap(self, pixmap):
        self.pixmapLabel.setPixmap(pixmap)
        size = pixmap.size()

        if size - QtCore.QSize(1, 0) == self.pixmapLabelArea.maximumViewportSize():
            size -= QtCore.QSize(1, 0)

        self.pixmapLabel.resize(size)

    def getSize(self):
        text, ok = QtGui.QInputDialog.getText(self, "Grabber",
                "Enter pixmap size:", QtGui.QLineEdit.Normal,
                "%d x %d" % (self.glWidget.width(), self.glWidget.height()))

        if not ok:
            return QtCore.QSize()

        regExp = QtCore.QRegExp("([0-9]+) *x *([0-9]+)")

        if regExp.exactMatch(text):
            width = int(regExp.cap(1))
            height = int(regExp.cap(2))
            if width > 0 and width < 2048 and height > 0 and height < 2048:
                return QtCore.QSize(width, height)

        return self.glWidget.size()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())    
