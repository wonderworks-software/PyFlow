from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QComboBox,QCheckBox

from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow import findPinClassByType


from PyFlow.Core.Common import *

class UIMakeDictNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIMakeDictNode, self).__init__(raw_node)
        self.prevDataType = "AnyPin"

    def postCreate(self, jsonTemplate=None):
        super(UIMakeDictNode, self).postCreate(jsonTemplate)
        self.input = self.getPin("KeyType")

    def changeType(self,dataType):
        #self.input._rawPin.enableOptions(PinOptions.ChangeTypeOnConnection)
        self.input._rawPin.initType(self.input._rawPin._defaultSupportedDataTypes[dataType],True)
        #self.input._rawPin.disableOptions(PinOptions.ChangeTypeOnConnection)

    def selectStructure(self,name):
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets ( self,propertiesWidget):
        inputsCategory = super(UIMakeDictNode, self).createInputWidgets(propertiesWidget)
        selector = QComboBox()
        for i in self.input._rawPin._defaultSupportedDataTypes:
            selector.addItem(i)         

        selector.setCurrentIndex(self.input._rawPin._defaultSupportedDataTypes.index(self.input._rawPin.dataType))

        selector.activated.connect(self.changeType)
        inputsCategory.insertWidget(0,"DataType",selector)
        