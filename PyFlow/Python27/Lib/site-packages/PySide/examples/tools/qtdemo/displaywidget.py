############################################################################
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
############################################################################

from PySide import QtCore, QtGui, QtNetwork, QtXml


class DisplayWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.empty = True
        self.emptying = False
        self.shapes = []
        self.timer = QtCore.QBasicTimer()

        self.enableUpdates()

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setMouseTracking(True)

    def appendShape(self, shape):
        self.shapes.append(shape)
        self.empty = False
        self.enableUpdates()

    def insertShape(self, position, shape):
        self.shapes.insert(position, shape)
        self.empty = False
        self.enableUpdates()

    def minimumSizeHint(self):
        return QtCore.QSize(800, 600)

    def mouseMoveEvent(self, event):
        if self.emptying:
            return

        updated = False

        for shape in self.shapes:
            if shape.rect().contains(QtCore.QPointF(event.pos())):
                if shape.isInteractive() and "fade" not in shape.metadata and "highlight" not in shape.metadata:
                    shape.metadata["highlight"] = True
                    updated = True
            elif shape.isInteractive() and "highlight" in shape.metadata and shape.metadata["highlight"]:
                shape.metadata["highlight"] = False
                updated = True

        if updated:
            self.enableUpdates()

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            return

        if self.emptying:
            return

        for shape in self.shapes:
            if shape.rect().contains(QtCore.QPointF(event.pos())) and "fade" not in shape.metadata:
                if "action" in shape.metadata:
                    self.emit(QtCore.SIGNAL("actionRequested"), shape.metadata["action"])
                elif "category" in shape.metadata:
                    self.emit(QtCore.SIGNAL("categoryRequested"), shape.metadata["category"])
                elif "example" in shape.metadata:
                    self.emit(QtCore.SIGNAL("exampleRequested"), shape.metadata["example"])
                elif "documentation" in shape.metadata:
                    self.emit(QtCore.SIGNAL("documentationRequested"), shape.metadata["documentation"])
                    shape.metadata["highlight"] = False
                    self.enableUpdates()
                elif "launch" in shape.metadata:
                    self.emit(QtCore.SIGNAL("launchRequested"), shape.metadata["launch"])
                    shape.metadata["fade"] = -5
                    self.enableUpdates()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)
        for shape in self.shapes:
            if shape.rect().intersects(QtCore.QRectF(event.rect())):
                shape.paint(painter)
        painter.end()

    def reset(self):
        if self.emptying:
            return

        if len(self.shapes) == 0:
            self.empty = True
            self.timer.stop()
            self.emit(QtCore.SIGNAL("displayEmpty()"))
        else:
            self.enableUpdates()
            self.emptying = True
            self.empty = False
            for shape in self.shapes:
                shape.metadata["fade"] = -15
                shape.metadata["fade minimum"] = 0

    def shape(self, index):
        return self.shapes[index]

    def shapesCount(self):
        return len(self.shapes)

    def enableUpdates(self):
        if not self.timer.isActive():
            self.timer.start(50, self)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            discard = []

            updated = 0

            for shape in self.shapes:
                oldRect = shape.rect().toRect().adjusted(-1, -1, 1, 1)

                if shape.animate():
                    self.update(oldRect)
                    newRect = shape.rect().toRect().adjusted(-1, -1, 1, 1)
                    updated += 1

                    if "destroy" in shape.metadata:
                        discard.append(shape)
                    else:
                        self.update(newRect)

            if updated == 0:
                self.timer.stop()

            for shape in discard:
                self.shapes.remove(shape)

            if len(self.shapes) == 0 and not self.empty:
                self.empty = True
                self.emptying = False
                self.timer.stop()
                self.emit(QtCore.SIGNAL("displayEmpty()"))
        else:
            QtGui.QWidget.timerEvent(self, event)
