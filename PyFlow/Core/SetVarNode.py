"""@file GetVarNode.py

Builtin node to set variable value.
"""
from AbstractGraph import *
from Settings import *
from Core import Node
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLineEdit
from Qt import QtCore
from Qt import QtGui
from Commands import RemoveNodes
from InputWidgets import getInputWidget


## Variable setter node
class SetVarNode(Node, NodeBase):
    """docstring for SetVarNode"""
    def __init__(self, name, graph, var):
        super(SetVarNode, self).__init__(name, graph)
        self.var = var
        self.inExec = self.addInputPin('in0', DataTypes.Exec, self.compute, hideLabel=True)
        self.outExec = self.addOutputPin('out0', DataTypes.Exec, hideLabel=True)
        self.value = self.addInputPin('inp', self.var.dataType)
        self.outValue = self.addOutputPin('out', self.var.dataType)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.killed.connect(self.kill)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)
        pinAffects(self.value, self.outValue)

    def serialize(self):
        template = Node.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onUpdatePropertyView(self, formLayout):
        # var name
        leName = QLineEdit(self.var.name)
        leName.setReadOnly(True)
        formLayout.addRow("Name", leName)

        # var type
        leType = QLineEdit(getDataTypeName(self.var.dataType))
        leType.setReadOnly(True)
        formLayout.addRow("Type", leType)

        # input value
        w = getInputWidget(self.value.dataType, self.value.setData, self.var.value)
        if w:
            w.setWidgetValue(self.value.currentData())
            w.setObjectName(self.value.getName())
            formLayout.addRow(self.value.name, w)
            if self.value.hasConnections():
                w.setEnabled(False)

    def onVarDataTypeChanged(self, dataType):
        cmd = RemoveNodes([self], self.graph())
        self.graph().undoStack.push(cmd)

    def postCreate(self, template):
        self.label().setPlainText('Set {}'.format(self.var.name))
        Node.postCreate(self, template)

    def onVarNameChanged(self, newName):
        self.label().setPlainText('Set {}'.format(newName))
        self.name = newName

    @staticmethod
    def category():
        return 'Variables'

    def compute(self):
        val = self.value.getData()

        self.var.value = val
        self.outValue.setData(val)

        self.outExec.call()
