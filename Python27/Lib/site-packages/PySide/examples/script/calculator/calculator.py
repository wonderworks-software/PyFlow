#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the PySide examples project.
#
# Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
#
# Contact: PySide team <contact@pyside.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# version 2.1 as published by the Free Software Foundation. Please
# review the following information to ensure the GNU Lesser General
# Public License version 2.1 requirements will be met:
# http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
# #
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

import sys

from PySide.QtCore import QIODevice, QFile, SIGNAL, SLOT
from PySide.QtGui import QApplication, QLineEdit
from PySide.QtScript import QScriptEngine
from PySide.QtUiTools import QUiLoader

try:
    from PySide.QtScriptTools import QScriptEngineDebugger
    HAS_DEBUGGER = True
except ImportError:
    HAS_DEBUGGER = False

import calculator_rc

calculator_rc.qInitResources()

def main(argv=None):
    if argv is None:
        argv = sys.argv

    app = QApplication(argv)
    engine = QScriptEngine()

    if HAS_DEBUGGER:
        debugger = QScriptEngineDebugger()
        debugger.attachTo(engine)
        debugWindow = debugger.standardWindow()
        debugWindow.resize(1024, 640)

    scriptFileName = './calculator.js'
    scriptFile = QFile(scriptFileName)
    scriptFile.open(QIODevice.ReadOnly)
    engine.evaluate(unicode(scriptFile.readAll()), scriptFileName)
    scriptFile.close()

    loader = QUiLoader()
    ui = loader.load(':/calculator.ui')

    ctor = engine.evaluate('Calculator')
    scriptUi = engine.newQObject(ui, QScriptEngine.ScriptOwnership)
    calc = ctor.construct([scriptUi])

    if HAS_DEBUGGER:
        display = ui.findChild(QLineEdit, 'display')
        display.connect(display, SIGNAL('returnPressed()'),
                        debugWindow, SLOT('show()'))

    ui.show()
    return app.exec_()

if __name__ == '__main__':
    main()
