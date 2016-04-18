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


from hyperuilib.shared.dataresource import *
from hyperuilib.pageview import *
from hyperuilib.menuview import *
from hyperuilib.clockwidget import *
from hyperuilib.draggablepreview import *


class MainWindow(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._background = Resource.pixmap("background.png")
        self._clockWidget = ClockWidget(self)
        self._clockWidget.setPos(0, 0)

        # cache the clock into a pixmap to improve drag performance
        self._clockWidget.setCacheMode(QGraphicsItem.ItemCoordinateCache)

        width = Resource.intValue("window/width")
        height = Resource.intValue("window/height")

        self._overlay = QGraphicsRectItem(self)
        self._overlay.setBrush(QColor(0, 0, 0, 100))
        self._overlay.setRect(0, 0, width, height)
        self._overlay.hide()

        self._mainView = PageView();
        self._mainView.add(MenuView())
        self._preview = DraggablePreview(self._mainView, QSize(width, height), self)
        self.connect(self._preview, SIGNAL("draggableStarted()"), SLOT("onDragModeIn()"))
        self.connect(self._preview, SIGNAL("minimizeStarted()"), SLOT("onDragModeOut()"))
        self.connect(self._preview, SIGNAL("maximizeFinished()"), SLOT("onMaximizeFinished()"))

        phoneLabel = QGraphicsSimpleTextItem(self.tr("T-Mobile"), self)
        self_hourLabel = QGraphicsSimpleTextItem(self)

        labelFont = QFont(Resource.stringValue("default/font-family"))
        labelFont.setBold(True)
        labelFont.setPixelSize(Resource.intValue("topbar/font-size"))
        phoneLabel.setFont(labelFont)
        phoneLabel.setBrush(QColor(Resource.stringValue("default/font-color")))

        self._hourLabel = QGraphicsSimpleTextItem(self)
        self._hourLabel.setFont(labelFont)
        self._hourLabel.setBrush(QColor(Resource.stringValue("default/font-color")))

        p = Resource.pixmap("topbar_battery.png")
        iconBattery = QGraphicsPixmapItem(Resource.pixmap("topbar_battery.png"), self)
        icon3G = QGraphicsPixmapItem(Resource.pixmap("topbar_3g.png"), self)
        iconNetwork = QGraphicsPixmapItem(Resource.pixmap("topbar_network.png"), self)

        self._hourLabel.setPos(Resource.value("topbar/hour-label-pos"))
        phoneLabel.setPos(Resource.value("topbar/label-pos"))
        iconNetwork.setPos(Resource.value("topbar/icon-network-pos"))
        icon3G.setPos(Resource.value("topbar/icon-3g-pos"))
        iconBattery.setPos(Resource.value("topbar/icon-battery-pos"))

        self.updateTime()
        self.createDummyDailyEvents()

        # update time each 30 seconds
        self.startTimer(30000)

    def timerEvent(self, event):
        self.updateTime()

    def updateTime(self):
        self._hourLabel.setText(QDateTime.currentDateTime().toString("hh:mm"))

    def onDragModeIn(self):
        self._overlay.show()

    def onDragModeOut(self):
        self._overlay.hide()

    def onMaximizeFinished(self):
        self._overlay.hide()
        self._clockWidget.hide()

    def createDummyDailyEvents(self):
        color1 = QColor("#80A2BF")
        color2 = QColor("#FF5E74")
        color3 = QColor("#A05284")

        cd = QDate.currentDate()
        self._clockWidget.addEvent(QDateTime(cd, QTime(15, 20, 0)),
                                   QDateTime(cd, QTime(16, 30, 0)), color1,
                                   self.tr("Development Meeting"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(16, 34, 0)),
                                   QDateTime(cd, QTime(17, 15, 0)), color1,
                                   self.tr("Development Meeting"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(17, 19, 0)),
                                   QDateTime(cd, QTime(18, 17, 0)), color1,
                                   self.tr("Development Meeting"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(18, 25, 0)),
                                   QDateTime(cd, QTime(18, 53, 0)), color1,
                                   self.tr("Development Meeting"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(18, 40, 0)),
                                    QDateTime(cd, QTime(19, 20, 0)), color3,
                                    self.tr("Project Presentation"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(19, 24, 0)),
                                    QDateTime(cd, QTime(20, 20, 0)), color3,
                                    self.tr("Project Presentation"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(19, 55, 0)),
                                    QDateTime(cd, QTime(20, 45, 0)), color2,
                                    self.tr("Dinner with Managers"))
        self._clockWidget.addEvent(QDateTime(cd, QTime(21, 25, 0)),
                                   QDateTime(cd, QTime(22, 20, 0)), color2,
                                   self.tr("Dinner with Managers"))

    def paint(self, painter, option, widget):
        painter.drawPixmap(0, 0, self._background)
