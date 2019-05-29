from Qt.QtWidgets import *
from Qt import QtCore, QtGui


class KeyboardModifiersCaptureWidget(QPushButton):
    """docstring for KeyboardModifiersCaptureWidget."""
    def __init__(self, parent=None):
        super(KeyboardModifiersCaptureWidget, self).__init__(parent)
        self._currentModifiers = QtCore.Qt.NoModifier
        self.setText("None")
        self.bCapturing = False
        self.setCheckable(True)
        self.setToolTip("<b>Left click</b> to start capturing.<br><b>Enter</b> to accept.<br><b>Esc</b> to clear")

    @staticmethod
    def modifiersToString(modifiers):
        if modifiers == QtCore.Qt.KeyboardModifier.NoModifier:
            return "None"
        return QtGui.QKeySequence(modifiers).toString()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
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

    def keyPressEvent(self, event):
        super(KeyboardModifiersCaptureWidget, self).keyPressEvent(event)
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.currentModifiers = QtCore.Qt.NoModifier
            return

        if key == QtCore.Qt.Key_Return and self.bCapturing:
            self.bCapturing = False
            self.setChecked(False)

        if self.bCapturing:
            self.currentModifiers = event.modifiers()


if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)

    w = KeyboardModifiersCaptureWidget()
    w.show()

    sys.exit(a.exec_())
