from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui


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

    def onVarDataTypeChanged(self, dataType):
        self.out.disconnectAll()
        self.out.dataType = dataType
        self.out.color = getPortColorByType(dataType)
        self.out.update()
        self.out.setData(getDefaultDataValue(dataType))

    def postCreate(self, template):
        Node.postCreate(self, template)
        self.label().setPlainText(self.var.name)

    def onVarNameChanged(self, newName):
        self.label().setPlainText(newName)

    def onVarValueChanged(self):
        push(self.out)

    @staticmethod
    def category():
        return 'Variables'

    def compute(self):
        self.out.setData(self.var.value)
