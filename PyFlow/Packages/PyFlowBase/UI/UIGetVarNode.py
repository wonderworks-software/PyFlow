## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Utils.stylesheet import Colors
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

    def onVariableWasChanged(self):
        if self.var is not None:
            self._createUIPinWrapper(self._rawNode.out)

    @property
    def var(self):
        return self._rawNode.var

    @var.setter
    def var(self, newVar):
        self._rawNode.var = newVar

    def postCreate(self, jsonTemplate=None):
        super(UIGetVarNode, self).postCreate(jsonTemplate)

        self.updateNodeShape()

        self.var.nameChanged.connect(self.onVarNameChanged)

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
        if self.var is not None:
            if self.var.name == varName:
                return
        else:
            self._rawNode.inp.disconnectAll()
            self._rawNode.out.disconnectAll()

        var = self.canvasRef().graphManager.findVariableByName(varName)
        free = self._rawNode.out.checkFree([])

        if var:
            linkedTo = getConnectedPins(self._rawNode.out)
            self.var = var
            self._rawNode.updateStructure()
            for i in linkedTo:
                if i.isAny():
                    i.setDefault()
                self.canvasRef().connectPinsInternal(self._rawNode.out.getWrapper()(), i.getWrapper()())
            self.updateHeaderText()
        self.canvasRef().pyFlowInstance.onRequestFillProperties(self.createPropertiesWidget)
        self._rawNode.checkForErrors()
        self.update()

    def createInputWidgets(self, inputsCategory, group=None, pins=True):
        validVars = self.graph().getVarList()
        cbVars = EnumComboBox([v.name for v in validVars])
        if self.var is not None:
            cbVars.setCurrentText(self.var.name)
        else:
            cbVars.setCurrentText("")
        cbVars.changeCallback.connect(self.onVarSelected)
        inputsCategory.addWidget("var", cbVars, group=group)

    def updateHeaderText(self):
        self.setHeaderHtml("Get {0}".format(self.var.name))
        self.updateNodeShape()

    def onVarNameChanged(self, newName):
        self.updateHeaderText()

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
