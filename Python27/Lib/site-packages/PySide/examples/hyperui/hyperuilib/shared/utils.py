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

def bTileRectAt(order, size, leftBorder, topBorder, rightBorder, bottomBorder):
    w = size.width()
    h = size.height()

    if order == 0:
        return QRect(0, 0, leftBorder, topBorder)
    elif order == 1:
        return QRect(leftBorder, 0,
                     w - leftBorder - rightBorder, topBorder)
    elif order == 2:
        return QRect(w - rightBorder, 0, rightBorder, topBorder)
    elif order == 3:
        return QRect(0, topBorder,
                     leftBorder, h - topBorder - bottomBorder);
    elif order == 4:
        return QRect(leftBorder, topBorder,
                     w - leftBorder - rightBorder,
                     h - topBorder - bottomBorder);
    elif order == 5:
        return QRect(w - rightBorder, topBorder,
                     rightBorder, h - topBorder - bottomBorder);
    elif order == 6:
        return QRect(0, h - bottomBorder, leftBorder, bottomBorder);
    elif order == 7:
        return QRect(leftBorder, h - bottomBorder,
                     w - leftBorder - rightBorder, bottomBorder);
    elif order == 8:
        return QRect(w - rightBorder, h - bottomBorder,
                     rightBorder, bottomBorder);
    else:
        return QRect();


def bDrawPixmap(painter, pixmap, boundingRect, leftBorder, topBorder, rightBorder, bottomBorder):
    if pixmap.isNull():
        return

    if leftBorder <= 0 and rightBorder <= 0 and topBorder <= 0 and bottomBorder <= 0:
        painter.drawPixmap(boundingRect.toRect(), pixmap)
    else:
        for i in range(9):
            oRect = bTileRectAt(i, pixmap.size(), leftBorder, topBorder, rightBorder, bottomBorder)
            dRect = bTileRectAt(i, boundingRect.size().toSize(), leftBorder, topBorder, rightBorder, bottomBorder)

            dRect.translate(boundingRect.x(), boundingRect.y())

            if oRect and dRect:
                painter.drawPixmap(dRect, pixmap, oRect)
