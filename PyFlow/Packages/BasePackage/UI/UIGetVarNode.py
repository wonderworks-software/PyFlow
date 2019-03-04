"""@file UIGetVarNode.py

Builtin node to acess variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.Settings import *
from PyFlow.Core.AGraphCommon import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.NodePainter import NodePainter

## Variable getter node
class UIGetVarNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIGetVarNode, self).__init__(raw_node)
        self.label().hide()
        self.label().opt_font.setPointSizeF(6.5)
        self.UIOut = None

    @property
    def var(self):
        return self._rawNode.var

    def postCreate(self, jsonTemplate=None):
        # create self._rawNode.var and raw self._rawNode.out pin
        self._rawNode.postCreate(jsonTemplate)

        self.UIOut = self._createUIPinWrapper(self._rawNode.out)
        self.UIOut.getLabel()().hide()
        self.UIoutputs[self.UIOut.uid] = self.UIOut

        self.updateNodeShape(label=jsonTemplate['meta']['label'])

        self.var.valueChanged.connect(self.onVarValueChanged)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.killed.connect(self.kill)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

    def boundingRect(self):
        return QtCore.QRectF(0, -3, self.w, 20)

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onUpdatePropertyView(self, formLayout):
        self.var.onUpdatePropertyView(formLayout)

    def onVarDataTypeChanged(self, dataType):
        cmd = RemoveNodes([self], self.graph())
        self.graph().undoStack.push(cmd)

    def onVarNameChanged(self, newName):
        self.label().setPlainText(newName)
        self.setName(newName)
        self.updateNodeShape(label=self.label().toPlainText())

    def onVarValueChanged(self):
        push(self.UIOut)
       
    def paint(self, painter, option, widget):
        NodePainter.asVariableGetter(self, painter, option, widget)
    
