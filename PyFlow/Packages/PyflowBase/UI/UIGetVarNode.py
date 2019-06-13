"""@file UIGetVarNode.py

Builtin node to access variable value.
"""
from copy import copy

from Qt import QtCore
from Qt import QtGui

from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Utils.Settings import *
from PyFlow.Core.Common import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UICommon import *
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.UI.Widgets.EnumComboBox import EnumComboBox


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

    @var.setter
    def var(self, newVar):
        self.var.nameChanged.disconnect(self.onVarNameChanged)
        self.var.dataTypeChanged.disconnect(self.onVarDataTypeChanged)
        self._rawNode.var = newVar
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

    def onVarStructureChanged(self, newStruct):
        self.canvasRef().pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        self._rawNode.checkForErrors()
        self.update()
        self.update()

    def postCreate(self, jsonTemplate=None):
        super(UIGetVarNode, self).postCreate(jsonTemplate)

        self.updateNodeShape()

        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

        outPin = list(self._rawNode.pins)[0]
        outPin.setName(self.var.name)

        pinWrapper = outPin.getWrapper()
        if pinWrapper:
            pinWrapper().setMenuItemEnabled("InitAs", False)
            outPin.disableOptions(PinOptions.RenamingEnabled)
            pinWrapper().syncRenamable()
        self.updateHeaderText()

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarSelected(self, varName):
        if self.var.name == varName:
            return

        var = self.canvasRef().graphManager.findVariable(varName)
        free = self._rawNode.out.checkFree([])

        if var:
            linkedTo = getConnectedPins(self._rawNode.out)
            self.var = var

            self._createUIPinWrapper(self._rawNode.out)
            self._rawNode.updateStructure()
            for i in linkedTo:
                if i.isAny():
                    i.setDefault()
                self.canvasRef().connectPinsInternal(self._rawNode.out.getWrapper()(), i.getWrapper()())
            self.updateHeaderText()
        self.canvasRef().pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        self._rawNode.checkForErrors()
        self.update()

    def createInputWidgets(self, propertiesWidget):
        inputsCategory = CollapsibleFormWidget(headName="Inputs")
        validVars = self.graph().getVarList()
        cbVars = EnumComboBox([v.name for v in validVars])
        cbVars.setCurrentText(self.var.name)
        cbVars.changeCallback.connect(self.onVarSelected)
        inputsCategory.addWidget("var", cbVars)

        propertiesWidget.addWidget(inputsCategory)

    def onVarDataTypeChanged(self, dataType):
        self._rawNode.out.disconnectAll()
        if self._rawNode.out.isAny():
            self._rawNode.out.setType(dataType)
        else:
            self._rawNode.recreateOutput(dataType)
        self.canvasRef().pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        self._rawNode.checkForErrors()
        self.update()

    def updateHeaderText(self):
        self.setHeaderHtml("Get {0}".format(self.var.name))
        self.updateNodeShape()

    def onVarNameChanged(self, newName):
        self.updateHeaderText()

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
