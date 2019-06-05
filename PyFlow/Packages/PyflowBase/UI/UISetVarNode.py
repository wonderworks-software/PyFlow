"""@file GetVarNode.py

Builtin node to set variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLineEdit
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Utils.Settings import *
from PyFlow.Core.Common import *
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.Widgets.InputWidgets import createInputWidget


# Variable setter node
class UISetVarNode(UINodeBase):
    """docstring for UISetVarNode"""
    def __init__(self, raw_node):
        super(UISetVarNode, self).__init__(raw_node)
        self.image = RESOURCES_DIR + "/gear.svg"
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray

    @property
    def var(self):
        return self._rawNode.var

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarDataTypeChanged(self, dataType):
        # recreate inpnut
        inPinName = self._rawNode.inp.name
        recreatedInPin = self._rawNode.recreateInput(dataType)
        recreatedInPin.setName(inPinName)
        self._createUIPinWrapper(self._rawNode.inp)

        # recreate output
        outPinName = self._rawNode.out.name
        recreatedOutPin = self._rawNode.recreateOutput(dataType)
        recreatedOutPin.setName(outPinName)
        self._createUIPinWrapper(self._rawNode.out)

        self.updateNodeShape()

        self.autoAffectPins()

    def postCreate(self, template):
        super(UISetVarNode, self).postCreate(template)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)
        self.onVarNameChanged(self.var.name)

        for pin in self.UIPins.values():
            pin.setMenuItemEnabled("InitAs", False)

    def onVarNameChanged(self, newName):
        self.setName(newName)
        self.updateNodeShape()

    @staticmethod
    def category():
        return 'Variables'
