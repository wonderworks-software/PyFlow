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

class DraggablePreview(QGraphicsWidget):

    def SCALED_POS(self, sw, sh, scale):
        return QPointF(round(sw * 0.5 - (sw * 0.5 + self._leftMargin) * scale),
                   round(sh - (sh + self._topMargin) * 0.5 * scale))

    def __init__(self, item, screenSize, parent = None):
        QGraphicsWidget.__init__(self, parent)

        self._item = item
        self._screenSize = screenSize
        self._border = Resource.intValue("draggable-preview/border")
        self._topMargin = Resource.intValue("draggable-preview/margin-top")
        self._leftMargin = Resource.intValue("draggable-preview/margin-left")
        self._maximizeRange = Resource.doubleValue("draggable-preview/maximize-range")
        self._minimumOffset = Resource.intValue("draggable-preview/minimum-offset")
        self.setFlag(QGraphicsItem.ItemHasNoContents)
        self.setupInterface()

    def setupInterface(self):
        # add background item
        self._backgroundPixmap = Resource.pixmap("screen_unlock.png")
        self._background = QGraphicsPixmapItem(self._backgroundPixmap, self)
        self._background.setPos(0, 0)
        self._background.setFlag(QGraphicsItem.ItemStacksBehindParent)
        self._background.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        # add embedded widget
        self._item.setParentItem(self)
        self._item.setFlag(QGraphicsItem.ItemStacksBehindParent)
        self._item.setPos(self._leftMargin + self._border, self._topMargin + self._border)
        self._item.resize(QSizeF(self._screenSize))

        # resize to the background size
        self.resize(QSizeF(self._backgroundPixmap.size()))

        sw = self._screenSize.width()
        sh = self._screenSize.height()

        minimumScale = Resource.doubleValue("draggable-preview/minimum-scale")
        draggableScale = Resource.doubleValue("draggable-preview/first-zoom-scale")

        self._draggablePos = self.SCALED_POS(sw, sh, draggableScale)
        minimumPos = self.SCALED_POS(sw, sh, minimumScale)
        maximumPos = QPointF(-self._leftMargin - self._border, -self._topMargin - self._border)

        self._maximumOffset = minimumPos.y()

        self._machine = QStateMachine(self)

        self._minimizedState = QState()
        self._minimizedState.assignProperty(self, "pos", minimumPos)
        self._minimizedState.assignProperty(self, "scale", minimumScale)

        self._draggableState = QState()
        self._draggableState.assignProperty(self, "pos", self._draggablePos)
        self._draggableState.assignProperty(self, "scale", draggableScale)

        self._maximizedState = QState()
        self._maximizedState.assignProperty(self, "pos", maximumPos)
        self._maximizedState.assignProperty(self, "scale", 1.0)

        restoreTime = Resource.intValue("draggable-preview/restore-time")
        maximizeTime = Resource.intValue("draggable-preview/maximize-time")
        firstZoomTime = Resource.intValue("draggable-preview/first-zoom-time")

        # create minimized > draggable state transition
        transition = self._minimizedState.addTransition(self, SIGNAL("draggableStarted()"),
                                                              self._draggableState)

        transition.addAnimation(self.createAnimation(firstZoomTime))

        # create draggable > minimized state transition
        transition = self._draggableState.addTransition(self, SIGNAL("minimizeStarted()"),
                                                              self._minimizedState)
        transition.addAnimation(self.createAnimation(restoreTime))

        # create draggable > maximized state transition
        transition = self._draggableState.addTransition(self, SIGNAL("maximizeStarted()"),
                                                              self._maximizedState)
        transition.addAnimation(self.createAnimation(maximizeTime, SLOT("onMaximizeFinished()")))

        # this is used just to update the final value when still animating
        transition = self._draggableState.addTransition(self, SIGNAL("draggableUpdate()"),
                                                              self._draggableState)
        transition.addAnimation(self.createAnimation(0))

        # add states
        self._machine.addState(self._minimizedState)
        self._machine.addState(self._draggableState)
        self._machine.addState(self._maximizedState)

        self.setPos(minimumPos)
        self.setScale(minimumScale)

        self._machine.setInitialState(self._minimizedState)
        self._machine.start()

    def createAnimation(self, time, slot = None):
        result = QParallelAnimationGroup()

        posAnimation = QPropertyAnimation(self, "pos")
        posAnimation.setEasingCurve(QEasingCurve(QEasingCurve.InSine))
        posAnimation.setDuration(time)

        scaleAnimation = QPropertyAnimation(self, "scale")
        scaleAnimation.setEasingCurve(QEasingCurve(QEasingCurve.InSine))
        scaleAnimation.setDuration(time)

        result.addAnimation(posAnimation)
        result.addAnimation(scaleAnimation)

        if slot:
            self.connect(result, SIGNAL("finished()"), slot)

        return result

    def onMaximizeFinished(self):
        # hide background
        self._background.hide()

        # move menu to front to not block events
        self._item.setFlag(QGraphicsItem.ItemStacksBehindParent, False)

        self.emit(SIGNAL("maximizeFinished()"))

        # detach from parent to avoid inherit transformations
        self._item.setParentItem(None)
        self._item.setPos(0, 0)

    def mousePressEvent(self, e):
        self._lastPos = e.scenePos()
        self._draggableState.assignProperty(self, "pos", self._draggablePos)
        self.emit(SIGNAL("draggableStarted()"))

    def mouseMoveEvent(self, e):
        offset = round(self.pos().y() +  e.scenePos().y() - self._lastPos.y())
        self._lastPos = e.scenePos()

        fy = max(self._minimumOffset, min(offset, self._maximumOffset))

        if fy < self._draggablePos.y():
            self._draggableState.assignProperty(self, "pos",
                                                QPointF(self._draggablePos.x(), fy))
        self.emit(SIGNAL("draggableUpdate()"))


    def mouseReleaseEvent(self, e):
        if self.pos().y() < self._minimumOffset + self._maximizeRange:
            self.emit(SIGNAL("maximizeStarted()"))
        else:
            self.emit(SIGNAL("minimizeStarted()"))
