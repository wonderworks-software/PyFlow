## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from qtpy.QtWidgets import *
from qtpy import QtCore, QtGui

from PyFlow.Input import InputActionType
from PyFlow.UI.Widgets.KeyboardModifiersCapture import KeyboardModifiersCaptureWidget
from PyFlow.UI.Widgets.KeyCapture import KeyCaptureWidget
from PyFlow.UI.Widgets.MouseButtonCapture import MouseButtonCaptureWidget


class InputActionWidget(QWidget):
    """docstring for InputActionWidget."""
    def __init__(self, parent=None, inputActionRef=None):
        super(InputActionWidget, self).__init__(parent)
        self.currentActionRef = inputActionRef
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        modifiersLabel = QLabel()
        modifiersLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        modifiersLabel.setPixmap(QtGui.QPixmap(":/shift-32.png"))
        self.modifiersWidget = KeyboardModifiersCaptureWidget()
        self.modifiersWidget.captured.connect(self.updateActionModifiers)
        self.layout.addWidget(modifiersLabel)
        self.layout.addWidget(self.modifiersWidget)

        if self.actionType == InputActionType.Keyboard:
            keyLabel = QLabel()
            keyLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            keyLabel.setPixmap(QtGui.QPixmap(":/keyboard-32.png"))
            self.keyCapture = KeyCaptureWidget()
            self.keyCapture.captured.connect(self.updateActionKey)
            self.layout.addWidget(keyLabel)
            self.layout.addWidget(self.keyCapture)

        if self.actionType == InputActionType.Mouse:
            mouseLabel = QLabel("Mouse:")
            mouseLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            mouseLabel.setPixmap(QtGui.QPixmap(":/mouse-32.png"))
            self.mouseCapture = MouseButtonCaptureWidget()
            self.mouseCapture.captured.connect(self.updateActionMouse)
            self.layout.addWidget(mouseLabel)
            self.layout.addWidget(self.mouseCapture)

    def updateActionMouse(self, value):
        if self.currentActionRef is not None:
            self.currentActionRef.setMouseButton(value)

    def updateActionKey(self, value):
        if self.currentActionRef is not None:
            self.currentActionRef.setKey(value)

    def updateActionModifiers(self, value):
        if self.currentActionRef is not None:
            self.currentActionRef.setModifiers(value)

    def setAction(self, inputAction):
        self.modifiersWidget.currentModifiers = inputAction.getModifiers()
        try:
            self.keyCapture.currentKey = inputAction.getKey()
        except:
            pass

        try:
            self.mouseCapture.currentButton = inputAction.getMouseButton()
        except:
            pass

    def getModifiers(self):
        return self.modifiersWidget.currentModifiers

    def getKey(self):
        try:
            return self.keyCapture.currentKey
        except:
            return None

    def getMouseButton(self):
        try:
            return self.mouseCapture.currentButton
        except:
            return None

    @property
    def actionType(self):
        return self.currentActionRef.actionType
