from Qt.QtWidgets import *
from Qt import QtCore, QtGui

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

        modifiersLabel = QLabel("Modifiers:")
        modifiersLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.modifiersWidget = KeyboardModifiersCaptureWidget()
        self.modifiersWidget.captured.connect(self.updateActionModifiers)
        self.layout.addWidget(modifiersLabel)
        self.layout.addWidget(self.modifiersWidget)

        if self.actionType == InputActionType.Keyboard:
            keyLabel = QLabel("Key:")
            keyLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
            self.keyCapture = KeyCaptureWidget()
            self.keyCapture.captured.connect(self.updateActionKey)
            self.layout.addWidget(keyLabel)
            self.layout.addWidget(self.keyCapture)

        if self.actionType == InputActionType.Mouse:
            mouseLabel = QLabel("Mouse:")
            mouseLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
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
