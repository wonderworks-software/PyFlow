"""
/*
 * This file is part of PySide: Python for Qt
 *
 * Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
 *
 * Contact: PySide team <contact@pyside.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * version 2.1 as published by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
 * 02110-1301 USA
 *
 */
"""


from PySide.QtGui import *
from PySide.QtCore import *

class Label(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._fontColor = Qt.white
        self._alignment = Qt.AlignLeft
        self._elideMode = Qt.ElideRight
        self._text = None
        self.setFont(QFont("Nokia Sans"))

    def text(self):
        return self._text;

    def setText(self, value):
        if self._text != value:
            self._text = value
            self.update()

    def fontColor(self):
        return self._fontColor

    def setFontColor(self, color):
        if self._fontColor != color:
            self._fontColor = color
            self.update()

    def elideMode(self):
        return self._elideMode

    def setElideMode(self, mode):
        if self._elideMode != mode:
            self._elideMode = mode
            self.update();

    def setAlignment(self, alignment):
        if self._alignment != alignment:
            self._alignment = alignment;
            self.update()

    def paint(self, painter, option, widget):
        if not self._text or len(self._text) == 0:
            return

        textRect = self.boundingRect().toRect()

        metrics = QFontMetrics(self.font())
        elidedText = metrics.elidedText(self._text, self._elideMode, textRect.width())

        painter.setFont(self.font())
        painter.setPen(self._fontColor)
        painter.drawText(textRect, Qt.TextSingleLine | self._alignment, elidedText)
