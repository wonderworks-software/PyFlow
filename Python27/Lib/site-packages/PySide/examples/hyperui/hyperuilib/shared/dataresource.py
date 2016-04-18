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


from PySide.QtCore import QSettings
from PySide.QtGui import QPixmap
from hyperuilib.resource.hyperui_rc import *

class Resource(object):
    _instance_ = None

    def __init__(self):
        self._settings = QSettings()
        self._pixmapPrefix = ":/"

    @staticmethod
    def instance():
        if not Resource._instance_:
            Resource._instance_ = Resource()

        return Resource._instance_

    @staticmethod
    def setIniFile(fileName):
        d = Resource.instance();
        if d._settings:
            d._settings = None

        d._settings = QSettings(fileName, QSettings.IniFormat)

    @staticmethod
    def pixmap(path):
        d = Resource.instance()
        f = d._pixmapPrefix + path
        p = QPixmap(f)
        if p.isNull():
            print("Pixmap not found: " + f)
        return p



    @staticmethod
    def setPixmapPrefix(prefix):
        d = Resource.instance()
        d._pixmapPrefix = prefix

    @staticmethod
    def containsValue(key):
        d = Resource.instance()
        return d._settings.contains(key)

    @staticmethod
    def value(key, value=None):
        d = Resource.instance()

        if d._settings.contains(key):
            return d._settings.value(key, value)
        else:
            print("Resource: key '%s' not found" % key)

    @staticmethod
    def intValue(key, value=0):
        return int(Resource.value(key, value))

    @staticmethod
    def doubleValue(key, value=0):
        return float(Resource.value(key, value))

    @staticmethod
    def stringValue(key, value=0):
        return Resource.value(key, value)
