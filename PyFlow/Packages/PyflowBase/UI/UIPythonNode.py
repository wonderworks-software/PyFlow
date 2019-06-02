import uuid

from Qt.QtWidgets import QAction
from Qt import QtGui, QtCore


from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Views.CodeEditor import CodeEditor


class UIPythonNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIPythonNode, self).__init__(raw_node)

        self.actionEdit = self._menu.addAction("Edit")
        self.actionEdit.triggered.connect(self.onEdit)

    @property
    def compute(self, *args, **kwargs):
        return self._rawNode.compute

    @compute.setter
    def compute(self, value):
        self._rawNode.compute = value

    @property
    def currentComputeCode(self):
        return self._rawNode.currentComputeCode

    @currentComputeCode.setter
    def currentComputeCode(self, value):
        self._rawNode.currentComputeCode = value

    def onEdit(self):
        editCmd = None
        print(editCmd)
