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

class View(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)
        self._pageView = None
        self._title = None

    def pageView(self):
        return self._pageView

    def setPageView(self, widget):
        self._pageView = widget

    def title(self):
        return self._title

    def setTitle(self, title):
        if self._title != title:
            self._title = title
            self.emit(SIGNAL("titleChanged()"))

    def doTransitionIn(self):
        self.emit(SIGNAL("transitionInStarted()"))

    def doTransitionOut(self):
        self.emit(SIGNAL("transitionOutStarted()"))
