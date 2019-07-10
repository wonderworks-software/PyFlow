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
            self.input._rawPin._defaultSupportedDataTypes[dataType], True)

    def selectStructure(self, name):
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets(self, inputsCategory, group=None, pins=True):
        if pins:
            super(UIMakeDictNode, self).createInputWidgets(inputsCategory, group)
        selector = QComboBox()
        for i in self.input._rawPin._defaultSupportedDataTypes:
            selector.addItem(i)

        selector.setCurrentIndex(self.input._rawPin._defaultSupportedDataTypes.index(
            self.input._rawPin.dataType))

        selector.activated.connect(self.changeType)
        inputsCategory.insertWidget(0, "DataType", selector, group=group)
