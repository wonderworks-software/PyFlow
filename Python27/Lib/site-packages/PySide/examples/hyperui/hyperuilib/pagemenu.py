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

from PySide.QtCore import *
from PySide.QtGui import *

from hyperuilib.shared.dataresource import *


class PageMenu(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._background = Resource.pixmap("top_bar_active.png")
        textFont = QFont(Resource.stringValue("default/font-family"))
        textFont.setPixelSize(Resource.intValue("page-menu/font-size"))
        self.setFont(textFont)

        self._text = None
        self._textRect = Resource.value("page-menu/label-rect")
        self._fontColor = QColor(Resource.stringValue("default/font-color"))

        self.setMinimumSize(QSizeF(self._background.size()))
        self.setMaximumSize(QSizeF(self._background.size()))

    def text(self):
        return self._text

    def setText(self, text):
        if self._text != text:
            self._text = text
            self.update()

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self._background)
        metrics = QFontMetrics(self.font())
        elidedText = metrics.elidedText(self._text, Qt.ElideRight, self._textRect.width())

        painter.setFont(self.font())
        painter.setPen(self._fontColor)
        painter.drawText(self._textRect, Qt.TextSingleLine | Qt.AlignCenter, elidedText)
