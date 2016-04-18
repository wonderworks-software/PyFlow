#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2009 Riverbank Computing Limited.
## Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
## Contact: Qt Software Information (qt-info@nokia.com)
##
## This file is part of the demonstration applications of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial Usage
## Licensees holding valid Qt Commercial licenses may use this file in
## accordance with the Qt Commercial License Agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and Nokia.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 2.1 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU Lesser General Public License version 2.1 requirements
## will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
##
## In addition, as a special exception, Nokia gives you certain
## additional rights. These rights are described in the Nokia Qt LGPL
## Exception version 1.0, included in the file LGPL_EXCEPTION.txt in this
## package.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3.0 as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL included in the
## packaging of this file.  Please review the following information to
## ensure the GNU General Public License version 3.0 requirements will be
## met: http://www.gnu.org/copyleft/gpl.html.
##
## If you are unsure which license is appropriate for your use, please
## contact the sales department at qt-sales@nokia.com.
## $QT_END_LICENSE$
##
#############################################################################

# This is only needed for Python v2 but is harmless for Python v3.
#import sip
#sip.setapi('QVariant', 2)

from PySide import QtCore, QtGui

import qtdemo_rc

from colors import Colors
from mainwindow import MainWindow
from menumanager import MenuManager


def artisticSleep(sleepTime):
    time = QtCore.QTime()
    time.restart()
    while time.elapsed() < sleepTime:
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents, 50)


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    Colors.parseArgs(sys.argv)

    if sys.platform == 'win32':
        QtGui.QMessageBox.information(None, "Documentation Warning",
                "If you are using the GPL version of PyQt from the binary "
                "installer then you will probably see warning messages about "
                "missing documentation.  This is because the installer does "
                "not include a copy of the Qt documentation as it is so "
                "large.")

    mainWindow = MainWindow()
    MenuManager.instance().init(mainWindow)
    mainWindow.setFocus()

    if Colors.fullscreen:
        mainWindow.showFullScreen()
    else:
        mainWindow.enableMask(True)
        mainWindow.show()

    artisticSleep(500)
    mainWindow.start()

    sys.exit(app.exec_())
