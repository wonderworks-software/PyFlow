from copy import copy

from Qt import QtCore
from Qt.QtWidgets import QDialog
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QVBoxLayout
from Qt.QtWidgets import QDialogButtonBox
from Qt.QtWidgets import QTextEdit

from PyFlow.UI.Utils.Settings import *


class TextEditDialog(QDialog):
    def __init__(self, font, textColor, parent=None):
        super(TextEditDialog, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.resize(QtCore.QSize(400, 300))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.te = QTextEdit()
        self._font = font
        self._font = QtGui.QFont(font)
        self.te.setFont(self._font)
        self.te.setTextColor(textColor)
        self.layout.addWidget(self.te)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttons.accepted.connect(self.onAccept)
        self.buttons.rejected.connect(self.onReject)
        self.layout.addWidget(self.buttons)
        self._result = None
        self.te.textChanged.connect(lambda color=textColor: self.te.setTextColor(color))

    def zoomIn(self, factor):
        self.te.zoomIn(factor)

    def setHtml(self, html):
        self.te.setHtml(html)

    def onReject(self):
        self._result = "", False
        self.reject()

    def getResult(self):
        return self._result

    def onAccept(self):
        self.te.selectAll()
        # self._font.setPointSize(self.initialPointSize)
        self.te.setFont(self._font)
        self._result = self.te.toHtml(), True
        self.accept()
