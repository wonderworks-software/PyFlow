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

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QString', 2)

from PySide import QtCore, QtGui

import draggabletext_rc


class DragLabel(QtGui.QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(text, parent)

        self.setAutoFillBackground(True)
        self.setFrameShape(QtGui.QFrame.Panel)
        self.setFrameShadow(QtGui.QFrame.Raised)

    def mousePressEvent(self, event):
        hotSpot = event.pos()

        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())
        mimeData.setData('application/x-hotspot',
                '%d %d' % (hotSpot.x(), hotSpot.y()))

        pixmap = QtGui.QPixmap(self.size())
        self.render(pixmap)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction, QtCore.Qt.CopyAction)

        if dropAction == QtCore.Qt.MoveAction:
            self.close()
            self.update()


class DragWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)

        dictionaryFile = QtCore.QFile(':/dictionary/words.txt')
        dictionaryFile.open(QtCore.QIODevice.ReadOnly)

        x = 5
        y = 5

        for word in QtCore.QTextStream(dictionaryFile).readAll().split():
            wordLabel = DragLabel(word, self)
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.width() + 2
            if x >= 195:
                x = 5
                y += wordLabel.height() + 2

        newPalette = self.palette()
        newPalette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        self.setPalette(newPalette)

        self.setAcceptDrops(True)
        self.setMinimumSize(400, max(200, y))
        self.setWindowTitle("Draggable Text")

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            mime = event.mimeData()
            pieces = mime.text().split()
            position = event.pos()
            hotSpot = QtCore.QPoint()

            hotSpotPos = mime.data('application/x-hotspot').split(' ')
            if len(hotSpotPos) == 2:
               hotSpot.setX(hotSpotPos[0].toInt()[0])
               hotSpot.setY(hotSpotPos[1].toInt()[0])

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position - hotSpot)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec_())
