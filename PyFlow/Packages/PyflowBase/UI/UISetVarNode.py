"""@file GetVarNode.py

Builtin node to set variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLineEdit
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.Widgets.InputWidgets import createInputWidget


# Variable setter node
class UISetVarNode(UINodeBase):
    """docstring for UISetVarNode"""

    def __init__(self, raw_node):
        super(UISetVarNode, self).__init__(raw_node)
        self.UIIn = None
        self.UIOut = None

    @property
    def var(self):
        return self._rawNode.var

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarDataTypeChanged(self, dataType):
        # TODO: mark nodes as invalid
        cmd = RemoveNodes([self], self.canvasRef())
        self.canvasRef().undoStack.push(cmd)

    def postCreate(self, template):
        super(UISetVarNode, self).postCreate(template)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)
        self.onVarNameChanged(self.var.name)

    def onVarNameChanged(self, newName):
        self.displayName = 'Set {}'.format(newName)
        self.setName(newName)
        self.updateNodeShape(label=self.displayName)

    @staticmethod
    def category():
        return 'Variables'
