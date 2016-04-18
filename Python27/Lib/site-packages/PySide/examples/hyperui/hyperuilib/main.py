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
    USE_MAEMO = True
except:
    USE_MAEMO = False

from hyperuilib.shared.qt_system import *
from hyperuilib.shared.dataresource import *
from hyperuilib.mainwindow import *
from hyperuilib.resource.hyperui_rc import *


def main():
    qInitResources()
    QApplication.setGraphicsSystem("raster")

    Resource.setIniFile(":/hyperui.ini")
    Resource.setPixmapPrefix(":/images/")

    app = QApplication([])

    width = Resource.intValue("window/width")
    height = Resource.intValue("window/height")

    scene = QGraphicsScene()
    view = QGraphicsView(scene)

    view.setWindowTitle(view.tr("Hiper UI"))
    view.setFrameShape(QFrame.NoFrame)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)

    view.resize(width, height)
    scene.setSceneRect(0, 0, width, height)

    mainWindow = MainWindow()
    scene.addItem(mainWindow)
    mainWindow.setGeometry(0, 0, width, height)

    System.setViewMode(view, System.PortraitMode)

    if USE_MAEMO:
        view.showFullScreen()
    else:
        view.setFixedSize(width, height);
        view.show();

    return app.exec_()

if __name__ == "__main__":
    main()
