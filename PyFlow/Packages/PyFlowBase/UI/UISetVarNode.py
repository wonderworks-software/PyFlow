"""@file GetVarNode.py

Builtin node to set variable value.
"""
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.Core.Common import *
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Widgets.EnumComboBox import EnumComboBox
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget

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

    @var.setter
    def var(self, newVar):
        if self.var is not None:
            self.var.nameChanged.disconnect(self.updateHeaderText)
        self._rawNode.var = newVar
        if self.var is not None:
            self.var.nameChanged.connect(self.updateHeaderText)

    def onVariableWasChanged(self):
        self._createUIPinWrapper(self._rawNode.inp)
        self._createUIPinWrapper(self._rawNode.out)

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarSelected(self, varName):
        if self.var is not None:
            if self.var.name == varName:
                return
        else:
            self._rawNode.out.disconnectAll()

        var = self.canvasRef().graphManager.findVariableByName(varName)

        if var:
            inLinkedTo = getConnectedPins(self._rawNode.inp)
            outLinkedTo = getConnectedPins(self._rawNode.out)
            self.var = var
            self._rawNode.updateStructure()
            for i in outLinkedTo:
                self.canvasRef().connectPinsInternal(
                    self._rawNode.out.getWrapper()(), i.getWrapper()())

            for o in inLinkedTo:
                self.canvasRef().connectPinsInternal(
                    o.getWrapper()(), self._rawNode.inp.getWrapper()())

            self.updateHeaderText()

    def createInputWidgets(self, inputsCategory, group=None, pins=True):
        inputsCategory.setButtonName("Variable")
        validVars = self.graph().getVarList()
        cbVars = EnumComboBox([v.name for v in validVars])
        if self.var is not None:
            cbVars.setCurrentText(self.var.name)
        else:
            cbVars.setCurrentText("")
        cbVars.changeCallback.connect(self.onVarSelected)
        inputsCategory.addWidget("var", cbVars, group=group)
        if pins:
            super(UISetVarNode, self).createInputWidgets(inputsCategory, group)

    def postCreate(self, template):
        super(UISetVarNode, self).postCreate(template)
        self.var.nameChanged.connect(self.updateHeaderText)
        self.updateHeaderText()

        for pin in self.UIPins.values():
            pin.setMenuItemEnabled("InitAs", False)

    def updateHeaderText(self, name=None):
        self.setHeaderHtml("Set {0}".format(self.var.name))
        self.updateNodeShape()

    @staticmethod
    def category():
        return 'Variables'
