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

class ButtonPrivate(object):
    def __init__(self, qptr):

        self._q = qptr
        self._text = ""
        self._isPressed = False
        self._normalPixmap = QPixmap()
        self._pressedPixmap = QPixmap()
        self._disabledPixmap = QPixmap()

    def init(self):
        self._q.setMinimumSize(QSizeF(self._normalPixmap.size()))
        self._q.setMaximumSize(QSizeF(self._normalPixmap.size()))


class Button(QGraphicsWidget):
    def __init__(self, normal, pressed, disabled, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._d = ButtonPrivate(self)
        self._d._normalPixmap = normal
        self._d._pressedPixmap = pressed
        self._d._disabledPixmap = disabled
        self._d.init()

    def setPixmap(self, state, pixmap):
        dirty = false

        if state == NormalState:
            self._d._normalPixmap = pixmap
            dirty = (not self._d._isPressed and self.isEnabled())
            self.setMinimumSize(d._normalPixmap.size())
            self.setMaximumSize(d._normalPixmap.size())
        elif state == PressedState:
            dirty = self._d._isPressed
            self._d._pressedPixmap = pixmap
        elif state == DisabledState:
            dirty = not self.isEnabled()
            self._d._disabledPixmap = pixmap

        if dirty:
            self.update()

    def text(self):
        return self._d._text

    def setText(self, value):
        if self._d._text != value:
            self._d._text = value
            self.update()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._d._isPressed = True
            self.update();
            self.emit(SIGNAL("pressed()"))

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            isClick = self._d._isPressed
            self._d._isPressed = False
            self.update()
            self.emit(SIGNAL("released()"))

            if isClick and self.contains(e.pos()):
                self.emit(SIGNAL("clicked()"))

    def isValid(self, pixmap):
        return pixmap and not pixmap.isNull()

    def paint(self, painter, option, widget):
        if not (option.state and QStyle.State_Enabled):
            support = not self._d._disabledPixmap.isNull()
            if support:
                pixmap = self._d._disabledPixmap
            else:
                pixmap = self._d._normalPixmap

            painter.drawPixmap(0, 0, pixmap)
        elif self._d._isPressed and self.isValid(self._d._pressedPixmap):
            painter.drawPixmap(0, 0, self._d._pressedPixmap)
        elif self.isValid(self._d._normalPixmap):
            painter.drawPixmap(0, 0, self._d._normalPixmap)

        if len(self._d._text) > 0:
            textRect = self.boundingRect().toRect()

            metrics = QFontMetrics(self.font())
            elidedText = metrics.elidedText(self._d._text, Qt.ElideRight,
                                            textRect.width())

            painter.setFont(self.font())
            painter.setPen(Qt.white)
            painter.drawText(textRect, Qt.TextSingleLine | Qt.AlignCenter, elidedText)
