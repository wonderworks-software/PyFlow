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


from Qt.QtWidgets import *
from Qt import QtCore, QtGui


class KeyboardModifiersCaptureWidget(QPushButton):
    """docstring for KeyboardModifiersCaptureWidget."""

    captured = QtCore.Signal(object)

    def __init__(self, parent=None):
        super(KeyboardModifiersCaptureWidget, self).__init__(parent)
        self._currentModifiers = QtCore.Qt.NoModifier
        self.setText("NoModifier")
        self.bCapturing = False
        self.setCheckable(True)
        self.setToolTip(
            "<b>Left click</b> to start capturing.<br><b>Enter</b> to accept.<br><b>Esc</b> to clear"
        )

        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionReset = QAction("Reset", None)
        self.actionReset.triggered.connect(self.resetToDefault)
        self.addAction(self.actionReset)

    def resetToDefault(self):
        self.currentModifiers = QtCore.Qt.NoModifier
        self.bCapturing = False
        self.setChecked(False)

    @staticmethod
    def modifiersToString(modifiers):
        if modifiers == QtCore.Qt.KeyboardModifier.NoModifier:
            return "NoModifier"
        return QtGui.QKeySequence(modifiers).toString()[:-1]

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if not self.bCapturing:
                self.bCapturing = True
                super(KeyboardModifiersCaptureWidget, self).mousePressEvent(event)
                self.setText("capturing...")

    @property
    def currentModifiers(self):
        return self._currentModifiers

    @currentModifiers.setter
    def currentModifiers(self, value):
        self._currentModifiers = value
        self.setText(self.modifiersToString(self._currentModifiers))
        self.captured.emit(self._currentModifiers)

    def keyPressEvent(self, event):
        super(KeyboardModifiersCaptureWidget, self).keyPressEvent(event)
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.resetToDefault()
            self.bCapturing = False
            self.setChecked(False)
            return

        if key == QtCore.Qt.Key_Return and self.bCapturing:
            self.bCapturing = False
            self.setChecked(False)
            self.update()

        if self.bCapturing:
            self.currentModifiers = event.modifiers()


if __name__ == "__main__":
    import sys

    a = QApplication(sys.argv)

    w = KeyboardModifiersCaptureWidget()
    w.show()

    sys.exit(a.exec_())
