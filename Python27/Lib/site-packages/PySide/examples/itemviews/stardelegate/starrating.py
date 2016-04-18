#!/usr/bin/python

"""**************************************************************************
**
** Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
** All rights reserved.
** Contact: Nokia Corporation (qt-info@nokia.com)
**
** This file is part of the examples of the Qt Toolkit.
**
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
**     the names of its contributors may be used to endorse or promote
**     products derived from this software without specific prior written
**     permission.
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
*****************************************************************************
** February 2011
** - stardelegate example ported to PySide by Arun Srinivasan 
**   <rulfzid@gmail.com>
**************************************************************************"""

from math import (cos, sin, pi)

from PySide.QtGui import (QPainter, QPolygonF)
from PySide.QtCore import (QPointF, QSize, Qt)

PAINTING_SCALE_FACTOR = 20


class StarRating(object):
    """ Handle the actual painting of the stars themselves. """

    def __init__(self, starCount=1, maxStarCount=5):
        self.starCount = starCount
        self.maxStarCount = maxStarCount

        # Create the star shape we'll be drawing.
        self.starPolygon = QPolygonF()
        self.starPolygon.append(QPointF(1.0, 0.5))
        for i in range(1, 5):
            self.starPolygon.append(QPointF(0.5 + 0.5 * cos(0.8 * i * pi),
                                    0.5 + 0.5 * sin(0.8 * i * pi)))
        
        # Create the diamond shape we'll show in the editor 
        self.diamondPolygon = QPolygonF()
        diamondPoints = [QPointF(0.4, 0.5), QPointF(0.5, 0.4), 
                         QPointF(0.6, 0.5), QPointF(0.5, 0.6), 
                         QPointF(0.4, 0.5)]
        for point in diamondPoints:
            self.diamondPolygon.append(point)

    def sizeHint(self):
        """ Tell the caller how big we are. """
        return PAINTING_SCALE_FACTOR * QSize(self.maxStarCount, 1)

    def paint(self, painter, rect, palette, isEditable=False):
        """ Paint the stars (and/or diamonds if we're in editing mode). """
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        if isEditable:
            painter.setBrush(palette.highlight())
        else:
            painter.setBrush(palette.windowText())

        yOffset = (rect.height() - PAINTING_SCALE_FACTOR) / 2
        painter.translate(rect.x(), rect.y() + yOffset)
        painter.scale(PAINTING_SCALE_FACTOR, PAINTING_SCALE_FACTOR)

        for i in range(self.maxStarCount):
            if i < self.starCount:
                painter.drawPolygon(self.starPolygon, Qt.WindingFill)
            elif isEditable:
                painter.drawPolygon(self.diamondPolygon, Qt.WindingFill)
            painter.translate(1.0, 0.0)

        painter.restore()