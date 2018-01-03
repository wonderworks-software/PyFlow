from AbstractGraph import *
from Settings import *
from Node import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui
from Pin import updatePins
from Commands import RemoveNodes
# from Commands import ChangeVarSetterDataType


class SetVarNode(Node, NodeBase):
    """docstring for SetVarNode"""
    def __init__(self, name, graph, var):
        super(SetVarNode, self).__init__(name, graph)
        self.var = var
        self.inExec = self.addInputPin('in0', DataTypes.Exec, self.compute, hideLabel=True)
        self.outExec = self.addOutputPin('out0', DataTypes.Exec, hideLabel=True)
        self.value = self.addInputPin('val', self.var.dataType, hideLabel=True)
        self.outValue = self.addOutputPin('valOut', self.var.dataType, hideLabel=True)
        # self.var.valueChanged.connect(self.onVarValueChanged)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.killed.connect(self.kill)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

    def serialize(self):
        template = Node.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onUpdatePropertyView(self, formLayout):
        self.var.onUpdatePropertyView(formLayout)

    def onVarDataTypeChanged(self, dataType):
        cmd = RemoveNodes([self], self.graph())
        self.graph().undoStack.push(cmd)

    def postCreate(self, template):
        Node.postCreate(self, template)
        self.label().setPlainText('Set {}'.format(self.var.name))

    def onVarNameChanged(self, newName):
        self.label().setPlainText('Set {}'.format(newName))
        self.name = newName

    def onVarValueChanged(self):
        push(self.value)
        updatePins(self.value)

    @staticmethod
    def category():
        return 'Variables'

    def compute(self):
        val = self.value.getData()

        self.var.value = val
        self.outValue.setData(val)

        self.outExec.call()
