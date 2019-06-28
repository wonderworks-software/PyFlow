from Qt import QtCore, QtGui
from Qt.QtWidgets import QDialog
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QDialogButtonBox
from Qt.QtWidgets import QTextEdit


class TextEditingField(QTextEdit):
    """docstring for TextEditingField."""
    accepted = QtCore.Signal()

    def __init__(self, parent=None):
        super(TextEditingField, self).__init__(parent)

    def keyPressEvent(self, event):
        super(TextEditingField, self).keyPressEvent(event)
        if event.modifiers() == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Return:
            self.accepted.emit()


class TextEditDialog(QDialog):
    def __init__(self, font, textColor, parent=None):
        super(TextEditDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.resize(QtCore.QSize(400, 300))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.te = TextEditingField()
        self.te.accepted.connect(self.onAccept)
        self._font = QtGui.QFont(font)
        self.te.setTextColor(textColor)
        self.layout.addWidget(self.te)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.onAccept)
        self.buttons.rejected.connect(self.onReject)
        self.layout.addWidget(self.buttons)
        self._result = None

    def zoomIn(self, factor):
        self.te.zoomIn(factor)

    def setHtml(self, html):
        self.te.setHtml(html)
        self.te.selectAll()
        self.te.setFontPointSize(20)
        cursor = self.te.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.te.setTextCursor(cursor)

    def onReject(self):
        self._result = "", False
        self.reject()

    def getResult(self):
        return self._result

    def onAccept(self):
        self.te.selectAll()
        self.te.setFontPointSize(self._font.pointSize())
        self._result = self.te.toHtml(), True
        self.accept()
