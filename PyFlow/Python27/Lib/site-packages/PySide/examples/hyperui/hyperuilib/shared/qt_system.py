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

try:
    from PySide.QtMaemo5 import *
    USE_MAEMO_5 = True
except:
    USE_MAEMO_5 = False

class System(QObject):
    _instance_ = None

    LandscapeMode = 0
    PortraitMode = 1

    def __init__(self):
        QObject.__init__(self)

    @staticmethod
    def instance():
        if not System._instance_:
            _instance_ = System()

        return _instance_

    @staticmethod
    def setViewMode(window, mode):
        if USE_MAEMO_5:
            enabled = (mode == System.PortraitMode)
            window.setAttribute(Qt.WA_Maemo5ForcePortraitOrientation, enabled)
            window.setAttribute(Qt.WA_Maemo5ForceLandscapeOrientation, not enabled)
