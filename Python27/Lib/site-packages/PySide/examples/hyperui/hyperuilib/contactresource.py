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


class ContactResource(object):
    SmallPhoto = 0
    LargePhoto = 1

    _instance_ = None

    def __init__(self):
        fp = QFile(":/contactlist.txt")
        fp.open(QIODevice.ReadOnly)

        self._values = []
        buffer = QTextStream(fp)

        while not buffer.atEnd():
            line = buffer.readLine().strip()

            if not line:
                continue

            parts = line.split(':')

            values = {}
            values[0] = parts[0]
            values[1] = parts[1]

            if not parts[2]:
                values[2] = ""
                values[3] = ""
            else:
                values[2] = "list_photo_%s" % parts[2]
                values[3] = "call_photo_%s" % parts[2]

            self._values.append(values)

        fp.close()

    def data(self, index, role):
        if index < 0 or index >= len(self._values):
            return ""
        else:
            if role in self._values[index]:
                return self._values[index][role]
            else:
                return ""

    @staticmethod
    def instance():
        if not ContactResource._instance_:
            ContactResource._instance_ = ContactResource()

        return ContactResource._instance_

    @staticmethod
    def count():
        return len(ContactResource.instance()._values)

    @staticmethod
    def name(index):
        return ContactResource.instance().data(index, 0)

    @staticmethod
    def phone(index):
        return ContactResource.instance().data(index, 1)

    @staticmethod
    def photo(index, type = SmallPhoto):
        int_type = 3
        if type == ContactResource.SmallPhoto:
            int_type = 2

        return ContactResource.instance().data(index, int_type)

    @staticmethod
    def indexFromPhone(phone):
        d = ContactResource.instance()

        total = ContactResource.count()
        for i in range(total):
            if phone == d.data(i, 1):
                return i
        return -1
