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


from Qt.QtWidgets import QComboBox
from PyFlow.UI.Canvas.UINodeBase import UINodeBase


class UIMakeDictNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIMakeDictNode, self).__init__(raw_node)
        self.prevDataType = "AnyPin"

    def postCreate(self, jsonTemplate=None):
        super(UIMakeDictNode, self).postCreate(jsonTemplate)
        self.input = self.getPinSG("KeyType")

    def changeType(self, dataType):
        self.input._rawPin.initType(
            self.input._rawPin._defaultSupportedDataTypes[dataType], True
        )

    def selectStructure(self, name):
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets(self, inputsCategory, inGroup=None, pins=True):
        if pins:
            super(UIMakeDictNode, self).createInputWidgets(inputsCategory, inGroup)
        selector = QComboBox()
        for i in self.input._rawPin._defaultSupportedDataTypes:
            selector.addItem(i)

        selector.setCurrentIndex(
            self.input._rawPin._defaultSupportedDataTypes.index(
                self.input._rawPin.dataType
            )
        )

        selector.activated.connect(self.changeType)
        inputsCategory.insertWidget(0, "DataType", selector, group=inGroup)
