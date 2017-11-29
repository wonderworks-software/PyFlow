#!/usr/bin/env python

"""PySide port of the painting/svgviewer example from Qt v4.x"""

import sys
from PySide import QtCore, QtGui, QtOpenGL, QtSvg

import svgviewer_rc


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.currentPath = ""

        self.area = SvgWindow()

        fileMenu = QtGui.QMenu(self.tr("&File"), self)
        self.openAction = fileMenu.addAction(self.tr("&Open..."))
        self.openAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+O")))
        self.quitAction = fileMenu.addAction(self.tr("E&xit"))
        self.quitAction.setShortcut(QtGui.QKeySequence(self.tr("Ctrl+Q")))

        self.menuBar().addMenu(fileMenu)

        rendererMenu = QtGui.QMenu(self.tr("&Renderer"), self)
        self.nativeAction = rendererMenu.addAction(self.tr("&Native"))
        self.nativeAction.setCheckable(True)

        if QtOpenGL.QGLFormat.hasOpenGL():
            self.glAction = rendererMenu.addAction(self.tr("&OpenGL"))
            self.glAction.setCheckable(True)

        self.imageAction = rendererMenu.addAction(self.tr("&Image"))
        self.imageAction.setCheckable(True)
        self.imageAction.setChecked(True)

        rendererGroup = QtGui.QActionGroup(self)
        rendererGroup.addAction(self.nativeAction)

        if QtOpenGL.QGLFormat.hasOpenGL():
            rendererGroup.addAction(self.glAction)

        rendererGroup.addAction(self.imageAction)

        self.menuBar().addMenu(rendererMenu)

        self.connect(self.openAction, QtCore.SIGNAL("triggered()"), self.openFile)
        self.connect(self.quitAction, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(rendererGroup, QtCore.SIGNAL("triggered(QAction *)"), self.setRenderer)

        self.setCentralWidget(self.area)
        self.setWindowTitle(self.tr("SVG Viewer"))

    def openFile(self, path=""):
        if path=="":
            fileName = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open SVG File"),
                                                         self.currentPath, "*.svg")[0]
        else:
            fileName = path

        if fileName!="":
            self.area.openFile(fileName)
            if not fileName.startswith(":/"):
                self.currentPath = fileName
                self.setWindowTitle(self.tr("%s - SVGViewer") % self.currentPath)

    def setRenderer(self, action):
        if action == self.nativeAction:
            self.area.setRenderer(SvgWindow.Native)
        elif action == self.glAction:
            if QtOpenGL.QGLFormat.hasOpenGL():
                self.area.setRenderer(SvgWindow.OpenGL)
        elif action == self.imageAction:
            self.area.setRenderer(SvgWindow.Image)


class SvgWindow(QtGui.QScrollArea):
    Native, OpenGL, Image = range(3)

    def __init__(self):
        QtGui.QScrollArea.__init__(self)

        self.mousePressPos = QtCore.QPoint()
        self.scrollBarValuesOnMousePress = QtCore.QPoint()
        self.currentPath = ""

        self.view = QtGui.QWidget(self)
        self.renderer = SvgWindow.Image
        self.setWidget(self.view)

    def openFile(self, path):
        self.currentPath = path
        self.setRenderer(self.renderer)

    def setRenderer(self, renderer):
        self.renderer = renderer

        if self.renderer == SvgWindow.OpenGL:
            if QtOpenGL.QGLFormat.hasOpenGL():
                view = SvgGLView(self.currentPath, self)
            else:
                view = QtGui.QWidget()
        elif self.renderer == SvgWindow.Image:
            view = SvgRasterView(self.currentPath, self)
        else:
            view = SvgNativeView(self.currentPath, self)

        self.setWidget(view)
        view.show()

    def mousePressEvent(self, event):
        self.mousePressPos = QtCore.QPoint(event.pos())
        self.scrollBarValuesOnMousePress.setX(self.horizontalScrollBar().value())
        self.scrollBarValuesOnMousePress.setY(self.verticalScrollBar().value())
        event.accept()

    def mouseMoveEvent(self, event):
        if self.mousePressPos.isNull():
            event.ignore()
            return

        self.horizontalScrollBar().setValue(self.scrollBarValuesOnMousePress.x() - event.pos().x() + self.mousePressPos.x())
        self.verticalScrollBar().setValue(self.scrollBarValuesOnMousePress.y() - event.pos().y() + self.mousePressPos.y())
        self.horizontalScrollBar().update()
        self.verticalScrollBar().update()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.mousePressPos = QtCore.QPoint()
        event.accept()


class SvgGLView(QtOpenGL.QGLWidget):
    def __init__(self, path, parent):
        QtOpenGL.QGLWidget.__init__(self, QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers))

        self.doc = QtSvg.QSvgRenderer(path, self)
        self.connect(self.doc, QtCore.SIGNAL("repaintNeeded()"),
                     self, QtCore.SLOT("update()"))

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        self.doc.render(p)

    def sizeHint(self):
        if self.doc:
            return self.doc.defaultSize()
        return QtOpenGL.QGLWidget.sizeHint(self)

    def wheelEvent(self, e):
        diff = 0.1
        size = QtCore.QSize(self.doc.defaultSize())
        width = size.width()
        height = size.height()
        if e.delta() > 0:
            width = int(self.width() + self.width() * diff)
            height = int(self.height() + self.height() * diff)
        else:
            width = int(self.width() - self.width() * diff)
            height = int(self.height() - self.height() * diff)

        self.resize(width, height)


class SvgRasterView(QtGui.QWidget):
    def __init__(self, path, parent):
        QtGui.QWidget.__init__(self, parent)

        self.buffer = QtGui.QImage()
        self.m_dirty = False

        self.doc = QtSvg.QSvgRenderer(path, self)
        self.connect(self.doc, QtCore.SIGNAL("repaintNeeded()"), self.poluteImage)

    def paintEvent(self, e):
        if self.buffer.size() != self.size() or self.m_dirty:
            self.buffer = QtGui.QImage(self.size(), QtGui.QImage.Format_ARGB32_Premultiplied)
            p = QtGui.QPainter(self.buffer)
            p.setViewport(0, 0, self.width(), self.height())
            p.eraseRect(0, 0, self.width(), self.height())
            self.doc.render(p)

        pt = QtGui.QPainter(self)
        pt.drawImage(0, 0, self.buffer)

    def sizeHint(self):
        if self.doc:
            return self.doc.defaultSize()
        return QtGui.QWidget.sizeHint(self)

    def poluteImage(self):
        self.m_dirty = True
        self.update()

    def wheelEvent(self, e):
        diff = 0.1
        size = QtCore.QSize(self.doc.defaultSize())
        width = size.width()
        height = size.height()
        if e.delta() > 0:
            width = int(self.width() + self.width() * diff)
            height = int(self.height() + self.height() * diff)
        else:
            width = int(self.width() - self.width() * diff)
            height = int(self.height() - self.height() * diff)

        self.resize(width, height)


class SvgNativeView(QtGui.QWidget):
    def __init__(self, path, parent):
        QtGui.QWidget.__init__(self, parent)

        self.doc = QtSvg.QSvgRenderer(path, self)
        self.connect(self.doc, QtCore.SIGNAL("repaintNeeded()"),
                     self, QtCore.SLOT("update()"))

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setViewport(0, 0, self.width(), self.height())
        self.doc.render(p)

    def sizeHint(self):
        if self.doc:
            return self.doc.defaultSize()
        return QtGui.QWidget.sizeHint(self)

    def wheelEvent(self, e):
        diff = 0.1
        size = QtCore.QSize(self.doc.defaultSize())
        width = size.width()
        height = size.height()
        if e.delta() > 0:
            width = int(self.width() + self.width() * diff)
            height = int(self.height() + self.height() * diff)
        else:
            width = int(self.width() - self.width() * diff)
            height = int(self.height() - self.height() * diff)

        self.resize(width, height)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()
    if len(sys.argv) == 2:
        window.openFile(sys.argv[1])
    else:
        window.openFile(":/files/cubic.svg")
    window.show()
    sys.exit(app.exec_())
