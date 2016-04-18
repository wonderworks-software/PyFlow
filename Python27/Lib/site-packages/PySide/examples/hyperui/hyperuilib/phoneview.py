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
from hyperuilib.shared.label import *
from hyperuilib.qt_global import *
from hyperuilib.shared.button import *
from hyperuilib.contactlist import *
from hyperuilib.contactresource import *
from hyperuilib.view import *


def resourceButtonFont():
    font = QFont(Resource.stringValue("default/font-family"))
    font.setBold(True)
    font.setPixelSize(Resource.intValue("button/font-size"))
    return font


class Overlay(QObject, QGraphicsRectItem):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        QGraphicsRectItem.__init__(self)
        self.setProperty("opacity", 0.0);
        self.setProperty("visible", True);

    def mousePressEvent(self, e):
        pass

class DialerWidget(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)
        background = QGraphicsPixmapItem(Resource.pixmap("dialer/background.png"), self)
        background.setPos(0, 0)
        background.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        margin = Resource.intValue("dialer-widget/margin")
        spacing = Resource.intValue("dialer-widget/spacing")

        self._layout = QGraphicsGridLayout()
        self._layout.setSpacing(spacing)
        self._layout.setContentsMargins(margin, margin, margin, margin)

        self.addButton("1", 0, 0, "dialer/top_left_key")
        self.addButton("2", 0, 1, "dialer/middle_key")
        self.addButton("3", 0, 2, "dialer/top_right_key")
        self.addButton("4", 1, 0, "dialer/middle_key")
        self.addButton("5", 1, 1, "dialer/middle_key")
        self.addButton("6", 1, 2, "dialer/middle_key")
        self.addButton("7", 2, 0, "dialer/middle_key")
        self.addButton("8", 2, 1, "dialer/middle_key")
        self.addButton("9", 2, 2, "dialer/middle_key")
        self.addButton("*", 3, 0, "dialer/bottom_left_key")
        self.addButton("0", 3, 1, "dialer/middle_key")
        self.addButton("#", 3, 2, "dialer/bottom_right_key")

        self.setLayout(self._layout)

    def addButton(self, label, row, col, imagePrefix):
        normalPath = "%s.png" % imagePrefix
        pressedPath = "%s_pressed.png" % imagePrefix

        button = Button(Resource.pixmap(normalPath),
                        Resource.pixmap(pressedPath), None, None)
        button.setText(label)
        button.setFont(resourceButtonFont())

        self.connect(button, SIGNAL("clicked()"), SLOT("onButtonClicked()"))
        self._layout.addItem(button, row, col)

    def onButtonClicked(self):
        button = self.sender()

        if button:
            self.emit(SIGNAL("buttonClicked(QString)"), button.text())


class CallBoard(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._top = Resource.pixmap("dialer_bk_top.png")
        self._bottom = Resource.pixmap("dialer_bk_bottom.png")
        self._middleline = Resource.pixmap("dialer_bk_lineexpand.png")

        # read settings
        self._font = QFont(Resource.stringValue("default/font-family"))
        self._margin = Resource.intValue("call-board/margin")
        self._phoneColor = Resource.stringValue("call-board/phone-font-color")
        self._subPanelRect = Resource.value("call-board/sub-panel-rect")
        self._dialPos = Resource.value("call-board/dial-button-pos")
        self._mutePos = Resource.value("call-board/mute-button-pos")
        self._speakerPos = Resource.value("call-board/speaker-button-pos")
        self._dialIconPos = Resource.value("call-board/dial-icon-pos")
        self._callLabelRect = Resource.value("call-board/call-label-rect")
        self._nameLabelRect = Resource.value("call-board/name-label-rect")
        self._phoneLabelRect = Resource.value("call-board/phone-label-rect")
        self._bigNameLabelRect = Resource.value("call-board/big-name-label-rect")

        # initialize interface
        self.setMinimumSize(self._top.size().width(),
                            self._top.size().height() +
                            self._bottom.size().height() +
                            self._middleline.size().height())

        # create main panel and photo
        self._contents = QGraphicsWidget(self)
        self._contents.setFlag(QGraphicsItem.ItemHasNoContents)
        self._contents.setGeometry(self.geometry())

        self._photo = QGraphicsPixmapItem(self._contents)
        self._photo.setPos(self._margin, self._margin)
        self._photo.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        self._icon = QGraphicsPixmapItem(self._contents)
        self._icon.setPixmap(Resource.pixmap("dialer_bullet_phone.png"))
        self._icon.setPos(QPointF(self._dialIconPos))
        self._icon.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)

        # create 'wait' sub-panel
        self._panelWait = QGraphicsWidget(self._contents)
        self._panelWait.setFlag(QGraphicsItem.ItemHasNoContents)
        self._panelWait.setGeometry(QRectF(self._subPanelRect))

        self._font.setPixelSize(Resource.intValue("call-board/small-font-size"))

        self._callLabel = Label(self._panelWait)
        self._callLabel.setFont(self._font)
        self._callLabel.setText(self.tr("Calling..."))
        self._callLabel.setGeometry(QRectF(self._callLabelRect))

        self._font.setPixelSize(Resource.intValue("call-board/font-size"))

        self._nameLabel = Label(self._panelWait)
        self._nameLabel.setFont(self._font)
        self._nameLabel.setGeometry(QRectF(self._nameLabelRect))

        self._phoneLabel = Label(self._panelWait)
        self._phoneLabel.setFont(self._font)
        self._phoneLabel.setFontColor(QColor(self._phoneColor))
        self._phoneLabel.setGeometry(QRectF(self._phoneLabelRect))

        # create 'in-call' sub-panel
        self._panelInCall = QGraphicsWidget(self._contents)
        self._panelInCall.setFlag(QGraphicsItem.ItemHasNoContents)
        self._panelInCall.setGeometry(QRectF(self._subPanelRect))

        self._bigNameLabel = Label(self._panelInCall)
        self._bigNameLabel.setFont(self._font)
        self._bigNameLabel.setGeometry(QRectF(self._bigNameLabelRect))

        dialButton = Button(Resource.pixmap("dialer_bt_dialer.png"), None, None, self._panelInCall)
        dialButton.setPos(QPointF(self._dialPos))

        muteButton = Button(Resource.pixmap("dialer_bt_mute.png"), None, None, self._panelInCall)
        muteButton.setPos(QPointF(self._mutePos))

        speakerButton = Button(Resource.pixmap("dialer_bt_speaker.png"), None, None, self._panelInCall)
        speakerButton.setPos(QPointF(self._speakerPos))

    def setName(self, name):
        self._nameLabel.setText(name)
        self._bigNameLabel.setText(name)

    def setPhone(self, phone):
        self._phoneLabel.setText(phone)

    def setPhoto(self, photo):
        self._photo.setPixmap(photo)

    def paint(self, painter, style, widget):
        tw = self._top.width()
        th = self._top.height()
        by = self.size().height() - self._bottom.height()

        painter.drawPixmap(0, 0, self._top)
        painter.drawTiledPixmap(0, int(th), int(tw), int(by - th), self._middleline)
        painter.drawPixmap(0, int(by), self._bottom)


class DialerDisplay(QGraphicsWidget):
    def __init__(self, parent):
        QGraphicsWidget.__init__(self, parent)

        self._background = Resource.pixmap("dialer_display_background.png")
        self.setMinimumSize(QSizeF(self._background.size()))

        self._label = Label(self)
        self._label.setElideMode(Qt.ElideLeft)
        self._label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        font = self._label.font()
        font.setPixelSize(Resource.intValue("phone-view/display-font-size"))
        self._label.setFont(font)

        self._cancel = Button(Resource.pixmap("dialer_display_bt_cancel.png"), None, None)
        self.connect(self._cancel, SIGNAL("clicked()"), SLOT("clear()"))

        layout = QGraphicsLinearLayout(Qt.Horizontal)
        layout.addItem(self._label)
        layout.addItem(self._cancel)
        self.setLayout(layout)

        layout.setAlignment(self._cancel, Qt.AlignBottom)

    def text(self):
        return self._label.text()

    def append(self, value):
        old = self._label.text()
        if old is None:
            old = ""
        self._label.setText(old + value)

    def clear(self):
        value = self._label.text()

        if value:
            self._label.setText(value[:-1])

    def paint(self, painter, style, widget):
        painter.drawPixmap(0, 0, self._background)


class PhoneView(View):
    def __init__(self, parent=None):
        View.__init__(self, parent)

        self.setTitle(self.tr("CONTACTS"))

        # read settings
        callTimeout = Resource.intValue("phone-view/call-timeout")
        displayPos = Resource.value("phone-view/display-pos")
        dialerBackPos = Resource.value("phone-view/dialer-back-pos")
        callButtonPos = Resource.value("phone-view/call-button-pos")
        contactsButtonPos = Resource.value("phone-view/contacts-button-pos")

        # initialize interface
        self.setFlag(QGraphicsItem.ItemHasNoContents)

        self._frame = QGraphicsWidget(self)

        self._display = DialerDisplay(self._frame)
        self._display.setPos(QPointF(displayPos))

        self._contactsButton = Button(Resource.pixmap("dialer_bt_contacts.png"),
                                      Resource.pixmap("dialer_bt_contacts_over.png"), None,
                                      self._frame)
        self._contactsButton.setPos(QPointF(contactsButtonPos))
        self._contactsButton.setFont(resourceButtonFont())

        self._overlay = Overlay(self._frame)
        self._overlay.setBrush(QBrush(Qt.black))
        self._overlay.setRect(QRectF(Resource.value("phone-view/overlay-rect")))

        self._callButton = Button(Resource.pixmap("dialer_bt_call.png"),
                                  Resource.pixmap("dialer_bt_call_over.png"), None, self._frame)
        self._callButton.setText(self.tr("CALL"))
        self._callButton.setPos(QPointF(callButtonPos))
        self._callButton.setFont(resourceButtonFont())

        self._endCallButton = Button(Resource.pixmap("dialer_bt_endcall.png"),
                                     Resource.pixmap("dialer_bt_endcall_over.png"), None, self._frame)
        self._endCallButton.setText(self.tr("END CALL"))
        self._endCallButton.setPos(QPointF(callButtonPos))
        self._endCallButton.setFont(resourceButtonFont())

        self._board = CallBoard(self._frame)
        self._board.setPos(QPointF(dialerBackPos))
        self._board.setPhoto(Resource.pixmap("call_photo_nobody.png"))

        self._dialer = DialerWidget(self._frame)
        self._dialer.setPos(QPointF(dialerBackPos))
        self.connect(self._dialer, SIGNAL("buttonClicked(const QString &)"),
                                   SLOT("dialButtonClicked(const QString &)"))

        self._contactList = ContactList(self)
        self._contactList.setGeometry(QRectF(Resource.value("phone-view/contactlist-rect")))
        self._contactList.hide()
        self.connect(self._contactList, SIGNAL("contactClicked(int)"), self.contactClicked)

        self._callTimer = QTimer()
        self._callTimer.setInterval(callTimeout)
        self._callTimer.setSingleShot(True)

        self.setOpacity(0.0)
        self.createStateMachine()

        self.connect(self._callButton, SIGNAL("clicked()"), SLOT("callClicked()"))

    def callClicked(self):
        # update phone number
        self._board.setName(self._display.text())
        self._board.setPhone("")
        self._board.setPhoto(Resource.pixmap("call_photo_nobody.png"))

        # simulate call wait
        self._callTimer.start()

    def contactClicked(self,  index):
        self._board.setName(ContactResource.name(index))
        self._board.setPhone(ContactResource.phone(index))

        photo = ContactResource.photo(index, ContactResource.LargePhoto)
        if photo:
            self._board.setPhoto(Resource.pixmap(photo))
        else:
            self._board.setPhoto(Resource.pixmap("call_photo_nobody.png"))

        self.emit(SIGNAL("callContact()"))

        # simulate call wait
        self._callTimer.start()

    def dialButtonClicked(self, value):
        self._display.append(value)

    def createStateMachine(self):
        self._machine = QStateMachine(self)

        state0 = QState()
        state0.assignProperty(self, "opacity", 0.0)

        # create default state
        state1 = QState()
        state1.assignProperty(self, "opacity", 1.0)
        state1.assignProperty(self._frame, "opacity", 1.0)
        state1.assignProperty(self._frame, "visible", True)
        state1.assignProperty(self._dialer, "opacity", 1.0)
        state1.assignProperty(self._display, "visible", True)
        state1.assignProperty(self._board, "visible", False)
        state1.assignProperty(self._callButton, "visible", True)
        state1.assignProperty(self._endCallButton, "visible", False)
        state1.assignProperty(self._board._contents, "opacity", 0.0)
        state1.assignProperty(self._board, "geometry", self._board.geometry())
        state1.assignProperty(self._overlay, "opacity", 0.0)
        state1.assignProperty(self._overlay, "visible", False)
        state1.assignProperty(self._contactList, "y", self._contactList.size().height() * 1.5)
        state1.assignProperty(self._contactList, "visible", False)

        # create calling state
        state2 = QState()
        state2.assignProperty(self._frame, "opacity", 1.0)
        state2.assignProperty(self._frame, "visible", True)
        state2.assignProperty(self._dialer, "opacity", 0.0)
        state2.assignProperty(self._display, "visible", False)
        state2.assignProperty(self._board, "visible", True)
        state2.assignProperty(self._callButton, "visible", False)
        state2.assignProperty(self._endCallButton, "visible", True)
        state2.assignProperty(self._board._contents, "opacity", 1.0)
        offsetY = -(self._board.pos().y() - self._display.pos().y())
        state2.assignProperty(self._board, "geometry",
                               self._board.geometry().adjusted(0, offsetY, 0, 0))

        state2.assignProperty(self._board._panelWait, "opacity", 1.0)
        state2.assignProperty(self._board._panelInCall, "opacity", 0.0)
        state2.assignProperty(self._board._panelWait, "visible", True)
        state2.assignProperty(self._board._panelInCall, "visible", False)
        state2.assignProperty(self._overlay, "opacity", 0.5)
        state2.assignProperty(self._overlay, "visible", True)
        state2.assignProperty(self._contactList, "y", self._contactList.size().height() * 1.5)
        state2.assignProperty(self._contactList, "visible", False)

        #create in-call state
        state3 = QState()
        state3.assignProperty(self._board._panelWait, "opacity", 0.0)
        state3.assignProperty(self._board._panelInCall, "opacity", 1.0)
        state3.assignProperty(self._board._panelWait, "visible", False)
        state3.assignProperty(self._board._panelInCall, "visible", True)
        state3.assignProperty(self._overlay, "opacity", 0.5)
        state3.assignProperty(self._overlay, "visible", True)

        # create contact list state
        state4 = QState()
        state4.assignProperty(self._frame, "opacity", 0.0)
        state4.assignProperty(self._frame, "visible", False)
        state4.assignProperty(self._contactList, "y", 0)
        state4.assignProperty(self._contactList, "visible", True)

        # associates state1-state2 transition
        transition1 = state1.addTransition(self._callButton, SIGNAL("clicked()"), state2)
        transition1.addAnimation(self.createCallAnimation())

        #associates state2-state1 transition
        transition2 = state2.addTransition(self._endCallButton, SIGNAL("clicked()"), state1)
        transition2.addAnimation(self.createEndCallAnimation())

        # associates state3-state1 transition
        transition3 = state3.addTransition(self._endCallButton, SIGNAL("clicked()"), state1)
        transition3.addAnimation(self.createEndCallAnimation())

        # associates state2-state3 transition
        transition4 = state2.addTransition(self._callTimer, SIGNAL("timeout()"), state3)
        transition4.addAnimation(self.createInCallAnimation())

        # associates state0-state1 transition
        transition5 = state0.addTransition(self, SIGNAL("transitionInStarted()"), state1)
        transition5.addAnimation(self.createInOutAnimation(False))

        # associates state1-state0 transition
        transition6 = state1.addTransition(self, SIGNAL("transitionOutStarted()"), state0)
        transition6.addAnimation(self.createInOutAnimation(True))

        #associates state1-state4 transition
        transition7 = state1.addTransition(self._contactsButton, SIGNAL("clicked()"), state4)
        transition7.addAnimation(self.createContactAnimation(False))

        # associates state4-state2 transition
        transition8 = state4.addTransition(self, SIGNAL("callContact()"), state2)
        transition8.addAnimation(self.createContactAnimation(True))

        # associates state4-state0 transition
        transition9 = state4.addTransition(self, SIGNAL("transitionOutStarted()"), state0)
        transition9.addAnimation(self.createInOutAnimation(True))

        self._machine.addState(state0)
        self._machine.addState(state1)
        self._machine.addState(state2)
        self._machine.addState(state3)
        self._machine.addState(state4)

        self._machine.setInitialState(state0)
        self._machine.start()

    def createInOutAnimation(self, out):
        result = QSequentialAnimationGroup()
        result.addAnimation(propertyAnimation(self, "opacity", 400))

        if not out:
            self.connect(result, SIGNAL("finished()"), SIGNAL("transitionInFinished()"))
        else:
            self.connect(result, SIGNAL("finished()"), SIGNAL("transitionOutFinished()"))

        return result

    def createContactAnimation(self, close):
        result = QSequentialAnimationGroup()

        if close:
            result.addAnimation(propertyAnimation(self._contactList, "y", 600,
                                                   QEasingCurve.InQuart))
            result.addAnimation(propertyAnimation(self._contactList, "visible", 0))
            result.addAnimation(propertyAnimation(self._frame, "visible", 0))
            result.addAnimation(propertyAnimation(self._frame, "opacity", 400))
        else:
            result.addAnimation(propertyAnimation(self._contactList, "visible", 0))
            result.addAnimation(propertyAnimation(self._frame, "opacity", 400))
            result.addAnimation(propertyAnimation(self._contactList, "y", 600,
                                                   QEasingCurve.OutQuart))
            result.addAnimation(propertyAnimation(self._frame, "visible", 0))

        return result

    def createCallAnimation(self):
        result = QSequentialAnimationGroup()
        result.addAnimation(propertyAnimation(self._dialer, "opacity", 200))
        result.addAnimation(propertyAnimation(self._board, "geometry", 300))
        result.addAnimation(propertyAnimation(self._board._contents, "opacity", 200))
        result.addAnimation(propertyAnimation(self._overlay, "opacity", 200))

        return result

    def createInCallAnimation(self):
        result = QSequentialAnimationGroup()
        result.addAnimation(propertyAnimation(self._overlay, "opacity", 200))
        result.addAnimation(propertyAnimation(self._board._panelWait, "opacity", 300))
        result.addAnimation(propertyAnimation(self._board._panelWait, "visible", 0))
        result.addAnimation(propertyAnimation(self._board._panelInCall, "opacity", 300))
        result.addAnimation(propertyAnimation(self._overlay, "visible", 0))

        return result

    def createEndCallAnimation(self):
        result = QSequentialAnimationGroup()
        result.addAnimation(propertyAnimation(self._overlay, "opacity", 200))
        result.addAnimation(propertyAnimation(self._board._contents, "opacity", 200))
        result.addAnimation(propertyAnimation(self._board, "geometry", 300))
        result.addAnimation(propertyAnimation(self._dialer, "opacity", 200))
        result.addAnimation(propertyAnimation(self._board, "visible", False))
        result.addAnimation(propertyAnimation(self._display, "visible", False))
        result.addAnimation(propertyAnimation(self._overlay, "visible", False))

        return result
