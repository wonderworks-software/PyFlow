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


from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QComboBox, QCheckBox

from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow import findPinClassByType


from PyFlow.Core.Common import *


class UIConstantNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIConstantNode, self).__init__(raw_node)
        self.hover = False
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.headColor = self.headColorOverride = QtGui.QColor(
            *findPinClassByType("AnyPin").color())
        if self.headColor.lightnessF() > 0.75:
            self.labelTextColor = QtCore.Qt.black
        else:
            self.labelTextColor = QtCore.Qt.white
        self.prevDataType = "AnyPin"

    def kill(self, *args, **kwargs):
        inp = list(self.UIinputs.values())[0]
        out = list(self.UIoutputs.values())[0]
        newOuts = []
        for i in self.UIoutputs.values():
            for connection in i.connections:
                newOuts.append([connection.destination(),
                                connection.drawDestination])
        if inp.connections:
            source = inp.connections[0].source()
            for out in newOuts:
                drawSource = inp.connections[0].drawSource
                self.canvasRef().connectPins(source, out[0])
        super(UIConstantNode, self).kill()

    def postCreate(self, jsonTemplate=None):
        super(UIConstantNode, self).postCreate(jsonTemplate)
        self.input = self.getPinSG("in")
        self.output = self.getPinSG("out")
        self.input.OnPinChanged.connect(self.changeOnConection)
        self.output.OnPinChanged.connect(self.changeOnConection)
        self.changeType(self.input.dataType)
        self.updateNodeShape()

    def changeOnConection(self, other):
        if other.dataType != self.prevDataType:
            self.prevDataType = other.dataType
            self.changeType(other.dataType)

    def changeType(self, dataType):
        self.headColor = self.headColorOverride = QtGui.QColor(
            *findPinClassByType(dataType).color())
        if self.headColor.lightnessF() > 0.75:
            self.labelTextColor = QtCore.Qt.black
        else:
            self.labelTextColor = QtCore.Qt.white
        self.update()

    def updateType(self, valToUpdate, inputsCategory, group):
        if valToUpdate is not None:
            par = valToUpdate.parent().parent()
            del par
            super(UIConstantNode, self).createInputWidgets(inputsCategory, group)

    def selectStructure(self, valToUpdate, inputsCategory, group):
        if valToUpdate is not None:
            del valToUpdate
            super(UIConstantNode, self).createInputWidgets(
                inputsCategory, group)

    def createInputWidgets(self, inputsCategory, inGroup=None, pins=True):
        inputVal = None
        preIndex = inputsCategory.Layout.count()
        if pins:
            super(UIConstantNode, self).createInputWidgets(inputsCategory, inGroup)
            inputVal = inputsCategory.getWidgetByName("in")

        selector = QComboBox()

        for i in self._rawNode.pinTypes:
            selector.addItem(i)
        if self.input.dataType in self._rawNode.pinTypes:
            selector.setCurrentIndex(
                self._rawNode.pinTypes.index(self.input.dataType))

        structSelector = QComboBox()
        for i in [i.name for i in list(StructureType)]:
            structSelector.addItem(i)
        structSelector.inputsCategory = inputsCategory

        structSelector.setCurrentIndex(self.input._rawPin._currStructure)
        selector.activated.connect(self._rawNode.updateType)
        selector.activated.connect(
            lambda: self.updateType(inputVal, inputsCategory, inGroup))
        structSelector.activated.connect(self._rawNode.selectStructure)
        structSelector.activated.connect(
            lambda: self.selectStructure(inputVal, inputsCategory, inGroup))

        inputsCategory.insertWidget(
            preIndex, "DataType", selector, group=inGroup)
        inputsCategory.insertWidget(preIndex + 1, "Structure", structSelector, group=inGroup)
