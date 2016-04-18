#!/usr/bin/python

# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# All rights reserved.
# Contact: PySide Team (pyside@openbossa.org)
#
# This file is part of the examples of PySide: Python for Qt.
#
# $QT_BEGIN_LICENSE:BSD$
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
# $QT_END_LICENSE$


from PySide import QtCore, QtGui, QtDeclarative

class Console(QtCore.QObject):
    """Output stuff on the console."""

    @QtCore.Slot(str)
    @QtCore.Slot('double')
    def output(self, s):
        """
        An overloaded output function.
        
        At the moment, QML is unable to handle overloaded slots correctly
        and is very finicky about the order in which the slots are declared.
        See http://bugreports.qt.nokia.com/browse/QTBUG-11604 for details.
        As a temporary solution, use separate functions with one slot per
        function.
        """
        print(s)

    @QtCore.Slot(str)
    def outputStr(self, s):
        print(s)

    @QtCore.Slot('double')
    def outputFloat(self, x):
        print(x)


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    view = QtDeclarative.QDeclarativeView()

    # instantiate the Python object
    con = Console()

    # expose the object to QML
    context = view.rootContext()
    context.setContextProperty("con", con)

    view.setSource(QtCore.QUrl('view.qml'))
    view.show()

    sys.exit(app.exec_())

