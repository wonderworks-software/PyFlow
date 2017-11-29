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

from PySide import QtCore, QtGui


class WigglyWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WigglyWidget, self).__init__(parent)

        self.setBackgroundRole(QtGui.QPalette.Midlight)
        self.setAutoFillBackground(True)

        newFont = self.font()
        newFont.setPointSize(newFont.pointSize() + 20)
        self.setFont(newFont)

        self.timer = QtCore.QBasicTimer()
        self.text = ''

        self.step = 0;
        self.timer.start(60, self)   

    def paintEvent(self, event):
        sineTable = (0, 38, 71, 92, 100, 92, 71, 38, 0, -38, -71, -92, -100, -92, -71, -38)

        metrics = QtGui.QFontMetrics(self.font())
        x = (self.width() - metrics.width(self.text)) / 2
        y = (self.height() + metrics.ascent() - metrics.descent()) / 2
        color = QtGui.QColor()

        painter = QtGui.QPainter(self)

        for i, ch in enumerate(self.text):
            index = (self.step + i) % 16
            color.setHsv((15 - index) * 16, 255, 191)
            painter.setPen(color)
            painter.drawText(x, y - ((sineTable[index] * metrics.height()) / 400), ch)
            x += metrics.width(ch)

    def setText(self, newText):
        self.text = newText

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.step += 1
            self.update()
        else:
            super(WigglyWidget, self).timerEvent(event)


class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)

        wigglyWidget = WigglyWidget()
        lineEdit = QtGui.QLineEdit()

        layout = QtGui.QVBoxLayout()
        layout.addWidget(wigglyWidget)
        layout.addWidget(lineEdit)
        self.setLayout(layout)

        lineEdit.textChanged.connect(wigglyWidget.setText)

        lineEdit.setText("Hello world!")

        self.setWindowTitle("Wiggly")
        self.resize(360, 145)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = Dialog()
    dialog.show();
    sys.exit(app.exec_())    
