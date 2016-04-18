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
from hyperuilib.qt_global import *
from hyperuilib.shared.button import *
from hyperuilib.phoneview import *


class MenuView(View):

    def FPOS(self, i, j):
        p = QPointF(self._leftMargin + self._vSpacing * i,
                       self._topMargin + self._hSpacing * j)
        return p

    def FNPOS(self, i, j):
        p = QPointF(self._vSpacing * -(i + 3),
                       self._topMargin + self._hSpacing * (j + 2))
        return p


    def __init__(self, parent=None):
        View.__init__(self, parent)

        self.setTitle(self.tr("MENU"))
        self.setFlag(QGraphicsItem.ItemHasNoContents)
        self.setFlag(QGraphicsItem.ItemClipsChildrenToShape)

        # read settings
        self._topMargin = Resource.intValue("menu-view/margin-top")
        self._leftMargin = Resource.intValue("menu-view/margin-left")
        self._vSpacing = Resource.intValue("menu-view/spacing-vertical")
        self._hSpacing = Resource.intValue("menu-view/spacing-horizontal")
        self._mainIconIPos = Resource.value("menu-view/main-icon-pos")
        self._mainIconFPos = Resource.value("menu-view/main-icon-out-pos")

        # initialize interface
        self._btnTwitter = self.addIcon(Resource.pixmap("menu_bt_twitter.png"), self.FPOS(0, 0))
        self._btnEmail = self.addIcon(Resource.pixmap("menu_bt_email.png"), self.FPOS(0, 2))
        self._btnSettings = self.addIcon(Resource.pixmap("menu_bt_settings.png"), self.FPOS(1, 1))
        self._btnMusic = self.addIcon(Resource.pixmap("menu_bt_music.png"), self.FPOS(2, 0))

        self._btnNavigation = self.addIcon(Resource.pixmap("menu_bt_navigation.png"), self.FPOS(0, 4))
        self._btnChat = self.addIcon(Resource.pixmap("menu_bt_chat.png"), self.FPOS(1, 3))
        self._btnGames = self.addIcon(Resource.pixmap("menu_bt_games.png"), self.FPOS(2, 2))
        self._btnWeb = self.addIcon(Resource.pixmap("menu_bt_web.png"), self.FPOS(3, 1))

        self._btnFolder = self.addIcon(Resource.pixmap("menu_bt_folder.png"), self.FPOS(1, 5))
        self._btnCalendar = self.addIcon(Resource.pixmap("menu_bt_calendar.png"), self.FPOS(2, 4))
        self._btnCamera = self.addIcon(Resource.pixmap("menu_bt_camera.png"), self.FPOS(3, 3))

        self._btnPhone = self.addIcon(Resource.pixmap("menu_bt_phone.png"),
                                      self._mainIconIPos, SLOT("onPhoneClicked()"))

        self.createStateMachine()

        # keep always alive to reduce transition time
        self._phoneView = PhoneView()
        self._phoneView.setParent(self)

    def addIcon(self, pixmap, pos, slot=None):
        button = Button(pixmap, None, None, self)
        button.setPos(pos)
        if slot:
            self.connect(button, SIGNAL("clicked()"), slot)

        return button

    def onPhoneClicked(self):
        self.pageView().add(self._phoneView, True)

    def createStateMachine(self):
        self._machine = QStateMachine(self)

        state1 = QState()
        state1.assignProperty(self._btnTwitter, "pos", self.FNPOS(2, 3))
        state1.assignProperty(self._btnEmail, "pos", self.FNPOS(2, 5))
        state1.assignProperty(self._btnSettings, "pos", self.FNPOS(1, 4))
        state1.assignProperty(self._btnMusic, "pos", self.FNPOS(0, 3))
        state1.assignProperty(self._btnNavigation, "pos", self.FNPOS(2, 7))
        state1.assignProperty(self._btnChat, "pos", self.FNPOS(1, 6))
        state1.assignProperty(self._btnGames, "pos", self.FNPOS(0, 5))
        state1.assignProperty(self._btnWeb, "pos", self.FNPOS(-1, 4))
        state1.assignProperty(self._btnFolder, "pos", self.FNPOS(1, 8))
        state1.assignProperty(self._btnCalendar, "pos", self.FNPOS(0, 7))
        state1.assignProperty(self._btnCamera, "pos", self.FNPOS(-1, 6))
        state1.assignProperty(self._btnPhone, "pos", self._mainIconFPos)

        state2 = QState()
        state2.assignProperty(self._btnTwitter, "pos", self.FPOS(0, 0))
        state2.assignProperty(self._btnEmail, "pos", self.FPOS(0, 2))
        state2.assignProperty(self._btnSettings, "pos", self.FPOS(1, 1))
        state2.assignProperty(self._btnMusic, "pos", self.FPOS(2, 0))
        state2.assignProperty(self._btnNavigation, "pos", self.FPOS(0, 4))
        state2.assignProperty(self._btnChat, "pos", self.FPOS(1, 3))
        state2.assignProperty(self._btnGames, "pos", self.FPOS(2, 2))
        state2.assignProperty(self._btnWeb, "pos", self.FPOS(3, 1))
        state2.assignProperty(self._btnFolder, "pos", self.FPOS(1, 5))
        state2.assignProperty(self._btnCalendar, "pos", self.FPOS(2, 4))
        state2.assignProperty(self._btnCamera, "pos", self.FPOS(3, 3))
        state2.assignProperty(self._btnPhone, "pos", self._mainIconIPos)

        transition1 = state1.addTransition(self, SIGNAL("transitionInStarted()"), state2)
        transition1.addAnimation(self.createInOutAnimation(False))

        transition2 = state2.addTransition(self, SIGNAL("transitionOutStarted()"), state1)
        transition2.addAnimation(self.createInOutAnimation(True))

        self._machine.addState(state1)
        self._machine.addState(state2)

        self._machine.setInitialState(state2)
        self._machine.start()

    def createInOutAnimation(self, out):
        result = QParallelAnimationGroup()
        t = 200
        d = 50

        if not out:
            ec = QEasingCurve.OutQuart

            result.addAnimation(propertyAnimation(self._btnWeb, "pos", t, ec))
            result.addAnimation(propertyAnimation(self._btnMusic, "pos", t + d, ec))
            result.addAnimation(propertyAnimation(self._btnCamera, "pos", t + 2 * d, ec))
            result.addAnimation(propertyAnimation(self._btnGames, "pos", t + 3 * d, ec))
            result.addAnimation(propertyAnimation(self._btnSettings, "pos", t + 4 * d, ec))
            result.addAnimation(propertyAnimation(self._btnTwitter, "pos", t + 5 * d, ec))
            result.addAnimation(propertyAnimation(self._btnCalendar, "pos", t + 6 * d, ec))
            result.addAnimation(propertyAnimation(self._btnChat, "pos", t + 7 * d, ec))
            result.addAnimation(propertyAnimation(self._btnEmail, "pos", t + 8 * d, ec))
            result.addAnimation(propertyAnimation(self._btnFolder, "pos", t + 9 * d, ec))
            result.addAnimation(propertyAnimation(self._btnNavigation, "pos", t + 10 * d, ec))
            result.addAnimation(propertyAnimation(self._btnPhone, "pos", t + 11 * d, ec))

            QObject.connect(result, SIGNAL("finished()"), self, SIGNAL("transitionInFinished()"))
        else:
            ec = QEasingCurve.InQuart

            result.addAnimation(propertyAnimation(self._btnPhone, "pos", t, ec))
            result.addAnimation(propertyAnimation(self._btnFolder, "pos", t + d, ec))
            result.addAnimation(propertyAnimation(self._btnNavigation, "pos", t + 2 * d, ec))
            result.addAnimation(propertyAnimation(self._btnCalendar, "pos", t + 3 * d, ec))
            result.addAnimation(propertyAnimation(self._btnChat, "pos", t + 4 * d, ec))
            result.addAnimation(propertyAnimation(self._btnEmail, "pos", t + 5 * d, ec))
            result.addAnimation(propertyAnimation(self._btnCamera, "pos", t + 6 * d, ec))
            result.addAnimation(propertyAnimation(self._btnGames, "pos", t + 7 * d, ec))
            result.addAnimation(propertyAnimation(self._btnSettings, "pos", t + 8 * d, ec))
            result.addAnimation(propertyAnimation(self._btnTwitter, "pos", t + 9 * d, ec))
            result.addAnimation(propertyAnimation(self._btnWeb, "pos", t + 10 * d, ec))
            result.addAnimation(propertyAnimation(self._btnMusic, "pos", t + 11 * d, ec))

            QObject.connect(result, SIGNAL("finished()"), self, SIGNAL("transitionOutFinished()"))

        return result
