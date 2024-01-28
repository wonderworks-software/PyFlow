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


from qtpy import QtCore
from qtpy import QtGui
from qtpy.QtWidgets import QComboBox, QCheckBox

from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow import findPinClassByType


class UIConvertToNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIConvertToNode, self).__init__(raw_node)
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.headColor = self.headColorOverride = QtGui.QColor(
            *findPinClassByType("AnyPin").color())
        if self.headColor.lightnessF() > 0.75:
            self.labelTextColor = QtCore.Qt.black
        else:
            self.labelTextColor = QtCore.Qt.white
        self.prevDataType = "AnyPin"

    def postCreate(self, jsonTemplate=None):
        super(UIConvertToNode, self).postCreate(jsonTemplate)
        self.output = self.getPinSG("result")
        self.output.OnPinChanged.connect(self.changeOnConection)
        self.changeType(self.output.dataType)
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
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets(self, inputsCategory, group=None, pins=True):
        preIndex = inputsCategory.Layout.count()
        if pins:
            super(UIConvertToNode, self).createInputWidgets(inputsCategory, group)
        selector = QComboBox()
        for i in self._rawNode.pinTypes:
            selector.addItem(i)
        if self.output.dataType in self._rawNode.pinTypes:
            selector.setCurrentIndex(
                self._rawNode.pinTypes.index(self.output.dataType))

        selector.activated.connect(self._rawNode.updateType)
        inputsCategory.insertWidget(preIndex, "DataType", selector, group=group)
