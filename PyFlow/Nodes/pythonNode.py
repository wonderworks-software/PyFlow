from Core.AbstractGraph import *
from Core.Settings import *
from Core import Node
from Qt import QtGui
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QGraphicsProxyWidget
from Qt.QtWidgets import QMenu
from Core.CodeEditor import WCodeEditor
import weakref
import uuid
from types import MethodType
from collections import OrderedDict


class pythonNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(pythonNode, self).__init__(name, graph)
        self.menu = QMenu()
        self.actionEdit = self.menu.addAction('edit')
        self.actionEdit.triggered.connect(self.openEditor)
        self.actionEdit.setIcon(QtGui.QIcon(':/icons/resources/py.png'))
        self.editorUUID = None
        self.bKillEditor = True
        self.label().icon = QtGui.QImage(':/icons/resources/py.png')
        self.currentComputeCode = Node.jsonTemplate()['computeCode']

    @staticmethod
    def pinTypeHints():
        return {'inputs': [], 'outputs': []}

    def computeCode(self):
        return self.currentComputeCode

    def openEditor(self):
        self.editorUUID = uuid.uuid4()
        self.graph().codeEditors[self.editorUUID] = WCodeEditor(self.graph(), self, self.editorUUID)
        self.graph().codeEditors[self.editorUUID].show()

    def kill(self):
        if self.editorUUID in self.graph().codeEditors:
            ed = self.graph().codeEditors.pop(self.editorUUID)
            ed.deleteLater()
        Node.kill(self)

    @staticmethod
    def category():
        return 'Utils'

    def postCreate(self, jsonTemplate):
        Node.postCreate(self, jsonTemplate)

        # restore compute
        self.currentComputeCode = jsonTemplate['computeCode']
        foo = WCodeEditor.wrapCodeToFunction('compute', jsonTemplate['computeCode'])
        exec(foo)
        self.compute = MethodType(compute, self, Node)

        # restore pins
        for inpJson in jsonTemplate['inputs']:
            pin = None
            if inpJson['dataType'] == DataTypes.Exec:
                pin = self.addInputPin(inpJson['name'], inpJson['dataType'], self.compute, inpJson['bLabelHidden'])
                pin.uid = uuid.UUID(inpJson['uuid'])
            else:
                pin = self.addInputPin(inpJson['name'], inpJson['dataType'], None, inpJson['bLabelHidden'])
                pin.uid = uuid.UUID(inpJson['uuid'])
            pin.setData(inpJson['value'])
        for outJson in jsonTemplate['outputs']:
            pin = self.addOutputPin(outJson['name'], outJson['dataType'], None, outJson['bLabelHidden'])
            pin.uid = uuid.UUID(outJson['uuid'])
            pin.setData(outJson['value'])

        # restore node label
        self.label().setPlainText(jsonTemplate['meta']['label'])

        self.bCallable = self.isCallable()

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
