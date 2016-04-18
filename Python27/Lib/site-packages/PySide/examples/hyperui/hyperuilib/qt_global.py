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


def drawTextWithShadow(painter, x, y, text, color):
    painter.setPen(QColor(30, 30, 30));
    painter.drawText(x + 2, y + 2, text);

    painter.setPen(color)
    painter.drawText(x, y, text)

def propertyAnimation(obj, property, time, type = QEasingCurve.Linear):
    result = QPropertyAnimation(obj, property)
    result.setDuration(int(time))
    result.setEasingCurve(QEasingCurve(type))
    return result
