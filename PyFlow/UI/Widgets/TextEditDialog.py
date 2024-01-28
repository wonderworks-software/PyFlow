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


from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QDialogButtonBox
from qtpy.QtWidgets import QTextEdit


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
