"""@file UIGetVarNode.py

Builtin node to access variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import VisibilityPolicy
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Views.VariablesWidget import VariablesWidget
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.Canvas.Painters import NodePainter


# Variable getter node
class UIGetVarNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIGetVarNode, self).__init__(raw_node)
        self.drawlabel = False
        # self.label().opt_font.setPointSizeF(6.5)

    @property
    def var(self):
        return self._rawNode.var

    def postCreate(self, jsonTemplate=None):
        super(UIGetVarNode, self).postCreate(jsonTemplate)

        self.updateNodeShape(label=jsonTemplate['meta']['label'])

        self.var.valueChanged.connect(self.onVarValueChanged)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

        self.displayName = "Get {}".format(self.var.name)

        for out in self.UIoutputs.values():
            out.bLabelHidden = True

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarDataTypeChanged(self, dataType):
        # recreate pin
        recreatedPin = self._rawNode.recreateOutput(dataType)
        self.UIOut = self._createUIPinWrapper(self._rawNode.out)
        self.onVarNameChanged(self.var.name)

    def onVarNameChanged(self, newName):
        self.displayName = "Get {}".format(newName)
        self.setName(newName)
        self.updateNodeShape(label=self.displayName)

    def onVarValueChanged(self, *args, **kwargs):
        for out in self._rawNode.outputs.values():
            push(out)

    def paint(self, painter, option, widget):
        # NodePainter.default(self, painter, option, widget)
        NodePainter.asVariableGetter(self, painter, option, widget)
