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

from PySide.QtGui import *
from PySide.QtCore import *

from hyperuilib.shared.dataresource import *
from hyperuilib.qt_global import *

class ClockEvent(object):
    def __init__(self, begin, end, color, text):
        self._begin = begin
        self._end = end
        self._color = color
        self._text = text


class ClockWidget(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)

        self._events = []
        self._background = Resource.pixmap("idle_clock_structure.png")
        self._divLine = Resource.pixmap("idle_line.png")
        self._middleKnob = Resource.pixmap("idle_clock_pointers_middle.png")
        self._hourPointer = Resource.pixmap("idle_clock_pointer_hour.png")
        self._minutePointer = Resource.pixmap("idle_clock_pointer_minutes.png")

        defaultFont = QFont(Resource.stringValue("default/font-family"))
        self._fontColor = QColor(Resource.stringValue("clock-widget/font-color"))
        self._dayFont = defaultFont
        self._dayFont.setBold(True)
        self._dayFont.setPixelSize(Resource.intValue("clock-widget/day-font-size"))
        self._labelFont = defaultFont
        self._labelFont.setPixelSize(Resource.intValue("clock-widget/label-font-size"))

        self._weekDayFont = defaultFont
        self._weekDayFont.setPixelSize(Resource.intValue("clock-widget/wday-font-size"))

        self._labelHeight = Resource.intValue("clock-widget/label-height")
        self._labelPos = Resource.value("clock-widget/label-init-pos")
        self._knobPoint = Resource.value("clock-widget/knob-pos")
        self._middlePoint = Resource.value("clock-widget/middle-pos")
        self._dayRect = Resource.value("clock-widget/day-label-rect")
        self._weekDayRect = Resource.value("clock-widget/wday-label-rect")
        self._eventsPixmapRect = Resource.value("clock-widget/events-pixmap-rect")
        self._eventsInnerOffset = Resource.intValue("clock-widget/events-inner-offset")
        self._eventsInnerDiameter = Resource.intValue("clock-widget/events-inner-diameter")
        self.setMinimumSize(QSizeF(self._background.size()))
        self.setMaximumSize(QSizeF(self._background.size()))

        self._timer = QTimer()
        self.connect(self._timer, SIGNAL("timeout()"), self.updateTime)
        self._timer.start(Resource.intValue("clock-widget/update-timeout"))

        self._eventsPixmap = QPixmap(self._eventsPixmapRect.size())

    def addEvent(self, begin, end, color, text):
        self._events.append(ClockEvent(begin, end, color, text))
        self.updateEvents()
        self.update()

    def updateTime(self):
        self.update()

    def paint(self, painter, option, widget):
        #store and adjust render hints
        hints = painter.renderHints()
        painter.setRenderHints(hints | QPainter.SmoothPixmapTransform)

        # draw clock base pixmap
        painter.drawPixmap(0, 0, self._background)

        # draw day information
        dateTime = QDateTime.currentDateTime()
        painter.setPen(self._fontColor)
        painter.setFont(self._dayFont)
        painter.drawText(self._dayRect, Qt.AlignHCenter | Qt.AlignVCenter, dateTime.toString("dd"))
        painter.setFont(self._weekDayFont);
        painter.drawText(self._weekDayRect, Qt.AlignHCenter | Qt.AlignVCenter, dateTime.toString("ddd").upper())
        painter.drawPixmap(self._eventsPixmapRect.x(), self._eventsPixmapRect.y(), self._eventsPixmap);

        # calculate min/hour pointer angles
        time = dateTime.time();
        hourAngle = 180 + qRound(30.0 * (time.hour() + time.minute() / 60.0));
        minuteAngle = 180 + qRound(6.0 * (time.minute() + time.second() / 60.0));

        # paint minute pointer
        painter.save()
        painter.translate(self._middlePoint)
        painter.rotate(minuteAngle)
        painter.drawPixmap(-self._minutePointer.width() / 2, 0, self._minutePointer)
        painter.restore()

        # paint hour pointer
        painter.save();
        painter.translate(self._middlePoint);
        painter.rotate(hourAngle);
        painter.drawPixmap(-self._hourPointer.width() / 2, 0, self._hourPointer)
        painter.restore()

        # paint middle knob
        painter.drawPixmap(self._knobPoint, self._middleKnob);

        i = 0;
        bx = self._labelPos.x()
        by = self._labelPos.y()
        bw = self._divLine.width()

        lastText = ""
        font = self._labelFont;
        painter.drawPixmap(bx, by, self._divLine)

        # paint events descriptions
        for event in self._events:
            # show different events
            if event._text == lastText:
                continue;

            lastText = event._text

            painter.setPen(event._color)
            painter.setBrush(event._color)
            painter.drawRoundedRect(bx + 4, int(by + 0.3 * self._labelHeight),
                                    int(0.1 * bw), int(0.5 * self._labelHeight), 2, 2)

            font.setBold(True)
            painter.setFont(font)
            drawTextWithShadow(painter, int(bx + 0.13 * bw), int(by + 0.75 * self._labelHeight),
                                    event._begin.toString("hh:mm"), Qt.white);

            font.setBold(False)
            painter.setFont(font);
            drawTextWithShadow(painter, int(bx + 0.3 * bw), int(by + 0.75 * self._labelHeight),
                                    event._text, self._fontColor)

            painter.drawPixmap(bx, by + self._labelHeight, self._divLine)

            by += self._labelHeight

            # show just two events
            i += 1
            if i > 1:
                break

        # restore render hints
        painter.setRenderHints(hints)

    def updateEvents(self):
        # clear the cache
        self._eventsPixmap.fill(Qt.transparent)

        painter = QPainter(self._eventsPixmap)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        painter.setOpacity(0.9)
        painter.setPen(Qt.NoPen)

        inner = self._eventsInnerOffset
        diameter = self._eventsInnerDiameter

        for event in self._events:
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

            # calculate start angle
            ta = event._begin.time()
            ia = round(30.0 * (ta.hour() + ta.minute() / 60.0))

            # calculate end angle
            tb = event._end.time();
            ib = round(30.0 * (tb.hour() + tb.minute() / 60.0)) - ia

            # drawPie parameters must be specified in 1/16th of a degree
            # and it's counter-clockwise. so we must adjust to the right values.
            ia = ia * -16 + 90 * 16
            ib = ib * -16

            # draw the event pie
            painter.setBrush(event._color);
            painter.drawPie(0, 0, diameter, diameter, int(ia), int(ib))

            # draw some gradients to simulate light effects
            gradient = QRadialGradient(diameter / 2, diameter / 2, diameter / 2 - 35)
            gradient.setColorAt(0.9, QColor.fromRgbF(1, 1, 1, 0.5))
            gradient.setColorAt(1, QColor.fromRgbF(0, 0, 0, 0.0))
            painter.setBrush(gradient)
            painter.drawPie(0, 0, diameter, diameter, int(ia), int(ib))

            gradient2 = QRadialGradient(diameter / 2, diameter / 2, diameter / 2)
            gradient2.setColorAt(0.98, QColor.fromRgbF(0, 0, 0, 0.0));
            gradient2.setColorAt(1, QColor.fromRgbF(0, 0, 0, 0.5));
            painter.setBrush(gradient2)
            painter.drawPie(0, 0, diameter, diameter, int(ia), int(ib))

            gradient3 = QRadialGradient(diameter / 2, diameter / 2, diameter / 2)
            gradient3.setColorAt(0, QColor.fromRgbF(1, 1, 1, 0.4))
            gradient3.setColorAt(1, QColor.fromRgbF(1, 1, 1, 0.0))

            gradient3.setFocalPoint(100, 100)
            painter.setBrush(gradient3)
            painter.drawPie(0, 0, diameter, diameter, int(ia), int(ib))

        # clear the middle of the pies
        painter.setBrush(Qt.transparent);
        painter.setCompositionMode(QPainter.CompositionMode_Clear)
        painter.drawPie(inner, inner, diameter - inner * 2,
                        diameter - inner * 2, 0, 360 * 16)
