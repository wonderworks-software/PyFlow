#!/usr/bin/env python

# Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# Contact: PySide Team (pyside@openbossa.org)
#
# This file is part of the examples of PySide: Python for Qt.
#
# You may use this file under the terms of the BSD license as follows:
#
# "Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
#     the names of its contributors may be used to endorse or promote
#     products derived from this software without specific prior written
#     permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *

class PersonModel (QAbstractListModel):

    MyRole = Qt.UserRole + 1

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self.setRoleNames({
            PersonModel.MyRole : 'modelData',
            Qt.DisplayRole : 'display' # Qt asserts if you don't define a display role
            })
        self._data = []

    def rowCount(self, index):
        return len(self._data)

    def data(self, index, role):
        d = self._data[index.row()]

        if role == Qt.DisplayRole:
            return d['name']
        elif role == Qt.DecorationRole:
            return Qt.black
        elif role == PersonModel.MyRole:
            return d['myrole']
        return None

    def populate(self):
        self._data.append({'name':'Qt', 'myrole':'role1'})
        self._data.append({'name':'PySide', 'myrole':'role2'})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QDeclarativeView()

    myModel = PersonModel()
    myModel.populate()

    view.rootContext().setContextProperty("myModel", myModel)
    view.setSource('view.qml')
    view.show()

    app.exec_()


