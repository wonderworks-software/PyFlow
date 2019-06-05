"""@file UIGetVarNode.py

Builtin node to access variable value.
"""
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Utils.Settings import *
from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UICommon import *


# Variable getter node
class UIGetVarNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIGetVarNode, self).__init__(raw_node)
        self.image = RESOURCES_DIR + "/gear.svg"
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray

    @property
    def var(self):
        return self._rawNode.var

    def postCreate(self, jsonTemplate=None):
        super(UIGetVarNode, self).postCreate(jsonTemplate)

        self.updateNodeShape()

        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

        outPin = list(self._rawNode.pins)[0]
        outPin.setName(self.var.name)

        # do not allow changing data type from node
        # change it using variable's properties
        pinWrapper = outPin.getWrapper()
        if pinWrapper:
            pinWrapper().setMenuItemEnabled("InitAs", False)
            # do not allow renaming pin
            outPin.disableOptions(PinOptions.RenamingEnabled)
            pinWrapper().syncRenamable()

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarDataTypeChanged(self, dataType):
        # recreate pin
        currentPinName = self._rawNode.out.name
        recreatedPin = self._rawNode.recreateOutput(dataType)
        recreatedPin.setName(currentPinName)
        recreatedPin.disableOptions(PinOptions.RenamingEnabled)
        self.UIOut = self._createUIPinWrapper(self._rawNode.out)
        self.updateNodeShape()

    def onVarNameChanged(self, newName):
        pin = list(self._rawNode.pins)[0]
        pin.setName(newName)
        self.updateNodeShape()

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
