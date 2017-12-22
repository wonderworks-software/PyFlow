from AbstractGraph import *
from Settings import *
from Node import Node
from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu
from CodeEditor import CodeEditor
import weakref
import uuid


class PythonNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(PythonNode, self).__init__(name, graph)
        self.menu = QMenu()
        self.actionEdit = self.menu.addAction('edit')
        self.actionEdit.triggered.connect(self.openEditor)
        self.actionEdit.setIcon(QtGui.QIcon(':/icons/resources/py.png'))
        self.editorUUID = None
        self.bKillEditor = True
        self.label().icon = QtGui.QImage(':/icons/resources/py.png')
        self.currentComputeCode = "def compute(self):\n\tprint('Hello')"

    def computeCode(self):
        return self.currentComputeCode

    def openEditor(self):
        self.editorUUID = uuid.uuid4()
        self.graph().codeEditors[self.editorUUID] = CodeEditor(self, self.editorUUID)
        self.graph().codeEditors[self.editorUUID].show()

    def kill(self):
        if self.editorUUID in self.graph().codeEditors:
            ed = self.graph().codeEditors.pop(self.editorUUID)
            ed.deleteLater()
        Node.kill(self)

    @staticmethod
    def category():
        return 'Utils'

    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    @staticmethod
    def keywords():
        return ['Code', 'Expression']

    @staticmethod
    def description():
        return 'default description'

    def compute(self):
        print("Old")
