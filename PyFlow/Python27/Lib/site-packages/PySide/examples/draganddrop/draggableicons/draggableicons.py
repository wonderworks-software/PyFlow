#!/usr/bin/env python

############################################################################
##
## Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
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
from PySide import QtCore, QtGui

import draggableicons_rc


class DragWidget(QtGui.QFrame):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)

        self.setMinimumSize(200, 200)
        self.setFrameStyle(QtGui.QFrame.Sunken | QtGui.QFrame.StyledPanel)
        self.setAcceptDrops(True)

        boatIcon = QtGui.QLabel(self)
        boatIcon.setPixmap(QtGui.QPixmap(':/images/boat.png'))
        boatIcon.move(20, 20)
        boatIcon.show()
        boatIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        carIcon = QtGui.QLabel(self)
        carIcon.setPixmap(QtGui.QPixmap(':/images/car.png'))
        carIcon.move(120, 20)
        carIcon.show()
        carIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        houseIcon = QtGui.QLabel(self)
        houseIcon.setPixmap(QtGui.QPixmap(':/images/house.png'))
        houseIcon.move(20, 120)
        houseIcon.show()
        houseIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            if event.source() == self:
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-dnditemdata'):
            itemData = event.mimeData().data('application/x-dnditemdata')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

            pixmap = QtGui.QPixmap()
            offset = QtCore.QPoint()
            dataStream >> pixmap >> offset

            newIcon = QtGui.QLabel(self)
            newIcon.setPixmap(pixmap)
            newIcon.move(event.pos() - offset)
            newIcon.show()
            newIcon.setAttribute(QtCore.Qt.WA_DeleteOnClose)

            if event.source() == self:
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        child = self.childAt(event.pos())
        if not child:
            return

        pixmap = QtGui.QPixmap(child.pixmap())

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << pixmap << QtCore.QPoint(event.pos() - child.pos())

        mimeData = QtCore.QMimeData()
        mimeData.setData('application/x-dnditemdata', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos() - child.pos())

        tempPixmap = QtGui.QPixmap(pixmap)
        painter = QtGui.QPainter()
        painter.begin(tempPixmap)
        painter.fillRect(pixmap.rect(), QtGui.QColor(127, 127, 127, 127))
        painter.end()

        child.setPixmap(tempPixmap)

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            child.close()
        else:
            child.show()
            child.setPixmap(pixmap)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    mainWidget = QtGui.QWidget()
    horizontalLayout = QtGui.QHBoxLayout()
    horizontalLayout.addWidget(DragWidget())
    horizontalLayout.addWidget(DragWidget())

    mainWidget.setLayout(horizontalLayout)
    mainWidget.setWindowTitle(QtCore.QObject.tr(mainWidget, "Draggable Icons"))
    mainWidget.show()

    sys.exit(app.exec_())
