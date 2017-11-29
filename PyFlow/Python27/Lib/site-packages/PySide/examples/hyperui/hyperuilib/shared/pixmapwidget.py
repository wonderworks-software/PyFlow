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

from utils import *


class PixmapWidgetPrivate(object):
    def __init__(self, pixmap=None):
        self.topBorder = 0
        self.leftBorder = 0
        self.rightBorder = 0
        self.bottomBorder = 0
        self.pixmap = pixmap


class PixmapWidget(QGraphicsWidget):
    def __init__(self, pixmap, parent = None):
        QGraphicsWidget.__init__(self, parent)

        self._d = PixmapWidgetPrivate()
        self.setPixmap(pixmap)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed);


    def pixmap(self):
        return self._d.pixmap

    def setPixmap(self, pixmap):
        self._d.pixmap = pixmap

        if pixmap.isNull():
            self.setPreferredSize(QSizeF())
        else:
            self.setPreferredSize(QSizeF(pixmap.size()))

        self.update()
        self.updateGeometry()

    def getBorders(self):
        return (self._d.leftBorder, self._d.topBorder, self._d.topBorder, self._d.rightBorder, self._d.bottomBorder)

    def setBorders(self, left, top, right, bottom):
        self._d.leftBorder = left
        self._d.topBorder = top
        self._d.rightBorder = right
        self._d.bottomBorder = bottom
        seld.update()

    def paint(self, painter, option, widget):
        bDrawPixmap(painter, self._d.pixmap, self.boundingRect(), self._d.leftBorder, self._d.topBorder, self._d.rightBorder, self._d.bottomBorder)
