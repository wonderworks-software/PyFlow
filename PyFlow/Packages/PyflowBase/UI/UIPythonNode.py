import uuid

from Qt import QtGui

from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.CodeEditor import CodeEditor


class UIPythonNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIPythonNode, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Edit")
        actionAddOut.triggered.connect(self.onEdit)
        self.label().icon = QtGui.QImage(':/icons/resources/py.png')
        self.editorUUID = None
        self.resizable = True

    def postCreate(self, jsonTemplate):
        super(UIPythonNode, self).postCreate(jsonTemplate)

    @property
    def compute(self):
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
        self.editorUUID = uuid.uuid4()
        self.graph().codeEditors[self.editorUUID] = CodeEditor(self.graph(), self, self.editorUUID)
        self.graph().codeEditors[self.editorUUID].show()
