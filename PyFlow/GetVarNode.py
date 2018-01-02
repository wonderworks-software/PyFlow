from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui
from Pin import updatePins
from Commands import RemoveNodes


class GetVarNode(Node, NodeBase):
    """docstring for GetVarNode"""
    def __init__(self, name, graph, var):
        super(GetVarNode, self).__init__(name, graph)
        self.var = var
        self.out = self.addOutputPin('val', self.var.dataType, hideLabel=True)
        self.var.valueChanged.connect(self.onVarValueChanged)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.killed.connect(self.kill)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

    def serialize(self):
        template = Node.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def kill(self):
        self.var.killed.disconnect()
        Node.kill(self)

    def onUpdatePropertyView(self, formLayout):
        self.var.onUpdatePropertyView(formLayout)

    def onVarDataTypeChanged(self, dataType):
        cmd = RemoveNodes([self], self.graph())
        self.graph().undoStack.push(cmd)

    def postCreate(self, template):
        Node.postCreate(self, template)
        self.label().setPlainText(self.var.name)

    def onVarNameChanged(self, newName):
        self.label().setPlainText(newName)
        self.name = newName

    def onVarValueChanged(self):
        push(self.out)
        updatePins(self.out)

    @staticmethod
    def category():
        return 'Variables'

    def compute(self):
        self.out.setData(self.var.value)
