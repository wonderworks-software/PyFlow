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

import fridgemagnets_rc


class DragLabel(QtGui.QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(parent)

        metric = QtGui.QFontMetrics(self.font())
        size = metric.size(QtCore.Qt.TextSingleLine, text)

        image = QtGui.QImage(size.width() + 12, size.height() + 12,
                QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtGui.qRgba(0, 0, 0, 0))

        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.ForceOutline)

        painter = QtGui.QPainter()
        painter.begin(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtCore.Qt.white)
        painter.drawRoundedRect(QtCore.QRectF(0.5, 0.5, image.width()-1,
                image.height()-1), 25, 25, QtCore.Qt.RelativeSize)

        painter.setFont(font)
        painter.setBrush(QtCore.Qt.black)
        painter.drawText(QtCore.QRect(QtCore.QPoint(6, 6), size),
                QtCore.Qt.AlignCenter, text)
        painter.end()

        self.setPixmap(QtGui.QPixmap.fromImage(image))
        self.labelText = text

    def mousePressEvent(self, event):
        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << QtCore.QByteArray(str(self.labelText)) << QtCore.QPoint(event.pos() - self.rect().topLeft())

        mimeData = QtCore.QMimeData()
        mimeData.setData('application/x-fridgemagnet', itemData)
        mimeData.setText(self.labelText)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        drag.setPixmap(self.pixmap())

        self.hide()

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            self.close()
        else:
            self.show()


class DragWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DragWidget, self).__init__(parent)

        dictionaryFile = QtCore.QFile(':/dictionary/words.txt')
        dictionaryFile.open(QtCore.QFile.ReadOnly)

        x = 5
        y = 5

        for word in QtCore.QTextStream(dictionaryFile).readAll().split():
            wordLabel = DragLabel(word, self)
            wordLabel.move(x, y)
            wordLabel.show()
            x += wordLabel.width() + 2
            if x >= 245:
                x = 5
                y += wordLabel.height() + 2

        newPalette = self.palette()
        newPalette.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        self.setPalette(newPalette)

        self.setMinimumSize(400, max(200, y))
        self.setWindowTitle("Fridge Magnets")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('application/x-fridgemagnet'):
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            event.acceptProposedAction()
        else:
            event.ignore()

    dragMoveEvent = dragEnterEvent

    def dropEvent(self, event):
        if event.mimeData().hasFormat('application/x-fridgemagnet'):
            mime = event.mimeData()
            itemData = mime.data('application/x-fridgemagnet')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

            text = QtCore.QByteArray()
            offset = QtCore.QPoint()
            dataStream >> text >> offset

            try:
                # Python v3.
                text = str(text, encoding='latin1')
            except TypeError:
                # Python v2.
                text = str(text)

            newLabel = DragLabel(text, self)
            newLabel.move(event.pos() - offset)
            newLabel.show()

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        elif event.mimeData().hasText():
            pieces = event.mimeData().text().split()
            position = event.pos()

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position)
                newLabel.show()

                position += QtCore.QPoint(newLabel.width(), 0)

            event.acceptProposedAction()
        else:
            event.ignore()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = DragWidget()
    window.show()
    sys.exit(app.exec_())
