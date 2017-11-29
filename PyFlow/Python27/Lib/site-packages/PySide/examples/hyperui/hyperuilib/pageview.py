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
from hyperuilib.view import *
from hyperuilib.shared.button import *
from hyperuilib.pagemenu import *


class PageSlot(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._contents = None
        self.setFlags(QGraphicsItem.ItemHasNoContents)

    def contents(self):
        return self._contents

    def setContents(self, contents):
        if self._contents and self._contents.parentItem() == self:
            self._contents.setParentItem(None)

        self._contents = contents
        if contents:
            contents.setParentItem(self)
            contents.setGeometry(0, 0, self.size().width(), self.size().height())

    def resizeEvent(self, event):
        QGraphicsWidget.resizeEvent(self, event)
        if self._contents:
            self._contents.resize(event.newSize())


class PageView(QGraphicsWidget):
    def __init__(self, parent=None):
        QGraphicsWidget.__init__(self, parent)

        self._views = []
        self._keepAlive = {}
        self._isBack = False
        self._isAnimating = False
        self._topOffset = Resource.intValue("page-view/margin-top")

        self.setFlag(QGraphicsItem.ItemHasNoContents)

        layout = QGraphicsLinearLayout(Qt.Vertical)
        layout.setContentsMargins(20 * 0.75, 40, 20 * 0.75, 0)

        topLayout = QGraphicsLinearLayout(Qt.Horizontal)
        topLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        layout.addItem(topLayout)
        layout.addStretch(1)

        self._menu = PageMenu()

        self._backButton = Button(Resource.pixmap("top_bt_back.png"),
                                  QPixmap(),
                                  Resource.pixmap("top_bt_back_disabled.png"))

        self._optionsButton = Button(Resource.pixmap("top_bt_options.png"),
                                     QPixmap(),
                                     Resource.pixmap("top_bt_options_disabled.png"))

        self.connect(self._backButton, SIGNAL("clicked()"), SLOT("backClicked()"))
        self.connect(self._optionsButton, SIGNAL("clicked()"), SLOT("optionsClicked()"))

        topLayout.addItem(self._optionsButton)
        topLayout.addStretch(1)
        topLayout.addItem(self._menu)
        topLayout.addStretch(1)
        topLayout.addItem(self._backButton)

        self._optionsButton.setEnabled(False)

        self._oldSlot = PageSlot(self)
        self._newSlot = PageSlot(self)
        self._oldSlot.setPos(0, self._topOffset)
        self._newSlot.setPos(0, self._topOffset)

    def add(self, view, keepAlive=False):
        if not view or self.isAnimating():
            return False

        view.setPageView(self)
        self._keepAlive[view] = keepAlive

        if len(self._views) == 0:
            self._views.append(view)
            self._menu.setText(view.title())
            self._oldSlot.setContents(view)
        else:
            self.animateTransition(self._views[-1], view, False)

        return True

    def back(self):
        if len(self._views) < 2 or self.isAnimating():
            return False

        oldView = self._views.pop()
        newView = self._views[-1]

        self.animateTransition(oldView, newView, True)
        return True

    def isAnimating(self):
        return self._isAnimating

    def backClicked(self):
        if self.isAnimating():
            return

        if len(self._views) < 2:
            QApplication.quit()
        else:
            self.back()

    def optionsClicked(self):
        pass

    def transitionFinished(self):
        newView = self._newSlot.contents()
        oldView = self._oldSlot.contents()

        self.disconnect(newView, SIGNAL("transitionInFinished()"),
                        self.transitionFinished)
        self.disconnect(oldView, SIGNAL("transitionOutFinished()"),
                        newView.doTransitionOut)

        if self._isBack:
            self._oldSlot.setContents(0)
            keepAlive = self._keepAlive[oldView]
            del self._keepAlive[oldView]
            if not keepAlive:
                oldView = None
        else:
            oldView.hide()
            self._views.append(newView)

        self._isAnimating = False
        self._menu.setText(newView.title())

    def animateTransition(self, oldView, newView, isBack):
        self._isAnimating = True

        self._isBack = isBack
        self._oldSlot.setContents(oldView)
        self._newSlot.setContents(newView)

        newView.show()

        self.connect(newView, SIGNAL("transitionInFinished()"),
                     self.transitionFinished)
        self.connect(oldView, SIGNAL("transitionOutFinished()"),
                     newView.doTransitionIn)

        oldView.doTransitionOut()

    def resizeEvent(self, event):
        QGraphicsWidget.resizeEvent(self, event)

        newSize = event.newSize()
        newSize.setHeight(newSize.height() - self._topOffset)

        self._oldSlot.resize(QSizeF(newSize))
        self._newSlot.resize(QSizeF(newSize))
