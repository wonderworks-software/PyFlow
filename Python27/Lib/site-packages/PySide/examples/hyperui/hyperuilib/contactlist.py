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
from hyperuilib.contactresource import *
from hyperuilib.shared.label import *
from hyperuilib.scrollarea import *
from hyperuilib.shared.pixmapwidget import *


class LetterScroll(PixmapWidget):
    def __init__(self, list):
        PixmapWidget.__init__(self, Resource.pixmap("list_abc.png"))
        self._lastChar = ''
        self._list = list

        self._marker = QGraphicsPixmapItem(Resource.pixmap("list_abcmarker.png"), self)
        self._marker.setX(-self._marker.boundingRect().width())
        self._marker.hide()

        self._markerLabel = QGraphicsSimpleTextItem(self._marker)
        self._markerLabel.setBrush(Qt.white)
        self._markerLabel.setText("")
        self._markerLabel.setX(0.08 * self._marker.boundingRect().width())
        self._markerLabel.setY(0.07 * self._marker.boundingRect().height())

        font = QFont(Resource.stringValue("default/font-family"))
        font.setPixelSize(Resource.intValue("contact-list/marker-font-size"))
        self._markerLabel.setFont(font)

        self.setMinimumSize(self.preferredSize())
        self.setMaximumSize(self.preferredSize())

    def mousePressEvent(self, e):
        self.gotoPosition(e.pos().y())
        self._marker.show()

    def mouseMoveEvent(self, e):
        self.gotoPosition(e.pos().y())

    def mouseReleaseEvent(self, e):
        self._marker.hide()
        self._lastChar = 0

    def gotoPosition(self, y):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ#"

        # assume monospaced letters
        _len = len(letters)
        index = int(y / (self.size().height() / _len))
        center = self._marker.boundingRect().height() / 2
        value = max(-center, min(y - center, self.size().height() - center))
        self._marker.setY(value)

        if index >= 0 and index < _len:
            c = letters[index]
            self._markerLabel.setText(c)
            if self._list.containsLetter(c):
                opacity = 1.0
            else:
                opacity = 0.3
            self._marker.setOpacity(opacity)

            if (self._lastChar != c):
                self._lastChar = c
                self.emit(SIGNAL("letterPressed(QString)"), c)


class ContactLabel(QGraphicsWidget):
    def __init__(self, text, parent = None):
        QGraphicsWidget.__init__(self, parent)

        self._text = text
        self._divisor = Resource.pixmap("list_divisor.png")
        self._color = Resource.stringValue("contact-list/label-font-color")

        font = QFont(Resource.stringValue("default/font-family"))
        font.setPixelSize(Resource.intValue("contact-list/label-font-size"))
        self.setFont(font)
        self.setMinimumHeight(Resource.intValue("contact-list/label-height"))

    def paint(self, painter, option, widget):
        size = self.size()
        painter.setPen(QColor(self._color))
        painter.setFont(self.font());
        painter.drawText(int(size.width() * 0.03),
                         int(size.height() * 0.80), self._text)
        painter.drawPixmap(0, int(size.height() - self._divisor.height()), self._divisor)


class ContactPhoto(QGraphicsWidget):
    def __init__(self, index, list):
        QGraphicsWidget.__init__(self, list)

        self._index = index
        self._list = list
        self._color = QColor(Resource.stringValue("contact-list/thumb-bg-color"))
        self._label = Label()

        photoPath = ContactResource.photo(index)
        self._photo = PixmapWidget(Resource.pixmap(photoPath))

        font = QFont(Resource.stringValue("default/font-family"))
        font.setBold(True);
        font.setPixelSize(Resource.intValue("contact-list/thumb-font-size"))

        self._label.setFont(font)
        self._label.setText(ContactResource.name(index))

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setSpacing(1)
        layout.setContentsMargins(3, 3, 3, 3)
        layout.addItem(self._photo)
        layout.addItem(self._label)

        self.setLayout(layout)

        self.setMinimumHeight(Resource.intValue("contact-list/thumb-height"))

    def paint(self, painter, option, widget):
        painter.fillRect(self.boundingRect(), self._color)

    def mousePressEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        self.emit(SIGNAL("contactClicked(int)"), self._index)

class ContactListItem(QGraphicsWidget):
    def __init__(self, index, list):
        QGraphicsWidget.__init__(self, list)

        self._index = index
        self._list = list
        self._divisor = Resource.pixmap("list_divisor.png")
        self._nameFontSize = Resource.intValue("contact-list/list-item-name-font-size")
        self._phoneFontSize = Resource.intValue("contact-list/list-item-phone-font-size")
        self._font = QFont(Resource.stringValue("default/font-family"))

        self.setMinimumHeight(Resource.intValue("contact-list/list-item-height"))
        self._text = ContactResource.name(index)
        self._phone = ContactResource.phone(index)

        # use random icons
        i = qrand() % 3
        if i == 0:
            self._icon = Resource.pixmap("list_icon_chat.png")
        elif i == 1:
            self._icon = Resource.pixmap("list_icon_world.png")
        else:
            self._icon = QPixmap()

    def paint(self, painter, option, widget):
        w = self.boundingRect().width()
        h = self.boundingRect().height()

        painter.setPen(Qt.white)

        self._font.setBold(True);
        self._font.setPixelSize(self._nameFontSize);
        painter.setFont(self._font);
        painter.drawText(int(w * 0.12), int(h * 0.40), self._text)

        self._font.setBold(False)
        self._font.setPixelSize(self._phoneFontSize)
        painter.setFont(self._font)
        painter.drawText(int(w * 0.12), int(h * 0.75), self._phone)

        if not self._icon.isNull():
            painter.drawPixmap(0, int(h * 0.15), self._icon)

        painter.drawPixmap(0, int(self.boundingRect().height() - self._divisor.height()), self._divisor);

    def mousePressEvent(self, e):
        pass

    def mouseReleaseEvent(self, e):
        self._list.emit(SIGNAL("contactClicked(int)"), self._index)


class ContactList(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self.setFlag(QGraphicsItem.ItemHasNoContents)
        self._labels = {}

        contents = QGraphicsWidget(self)

        scroll = LetterScroll(self)
        self.connect(scroll, SIGNAL("letterPressed(QString)"), self.letterPressed)

        contentsLayout = QGraphicsLinearLayout(Qt.Vertical)
        contentsLayout.setSpacing(0)
        contentsLayout.setContentsMargins(7, 0, 7, 0)

        topLayout = QGraphicsLinearLayout(Qt.Horizontal)
        topLayout.setSpacing(3)
        topLayout.setContentsMargins(0, 0, 0, 0)
        topLayout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        totalContacts = ContactResource.count()

        # just get 3 contacts with photo
        k = 0
        for i in range(totalContacts):
            if k >= 3:
                break

            photo = ContactResource.photo(i)
            if photo:
                k += 1
                topLayout.addItem(ContactPhoto(i, self))

        contentsLayout.addItem(topLayout);

        lastChar = ''
        for i in range(totalContacts):
            name = ContactResource.name(i)

            if not name:
                continue

            c = name[0]

            if lastChar != c:
                lastChar = c
                label = ContactLabel(c)
                contentsLayout.addItem(label)
                self._labels[c] = label

            contentsLayout.addItem(ContactListItem(i, self))

        contents.setLayout(contentsLayout)

        self._scrollArea = ScrollArea();
        self._scrollArea.setWidget(contents)

        scroll.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self._scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QGraphicsLinearLayout(Qt.Horizontal)
        layout.setSpacing(0);
        layout.setContentsMargins(0, 0, 0, 0);

        layout.addItem(self._scrollArea)
        layout.addItem(scroll)
        self.setLayout(layout)

    def containsLetter(self, c):
        return c in self._labels

    def letterPressed(self, c):
        if str(c) in self._labels:
            self._scrollArea.stopKinetic();
            # XXX: check first letter
            offset = 0
            if c != 'A':
                offset = self._labels[c].y()
            self._scrollArea.setOffset(offset)
