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
        self.input = self.getPin("in")
        self.output = self.getPin("out")
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
        self.canvasRef().tryFillPropertiesView(self)

    def selectStructure(self, name):
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets(self, propertiesWidget, categoryName=None):
        inputsCategory = super(
            UIConstantNode, self).createInputWidgets(propertiesWidget, categoryName)
        selector = QComboBox()
        overrideType = QCheckBox()

        for i in self._rawNode.pinTypes:
            selector.addItem(i)
        if self.input.dataType in self._rawNode.pinTypes:
            selector.setCurrentIndex(
                self._rawNode.pinTypes.index(self.input.dataType))

        structSelector = QComboBox()
        for i in [i.name for i in list(PinStructure)]:
            structSelector.addItem(i)

        # overrideType.setChecked(self.input._rawPin.optionEnabled(PinOptions.ChangeTypeOnConnection))
        structSelector.setCurrentIndex(self.input._rawPin._currStructure)
        # selector.setEnabled(self.input._rawPin.checkFree([self.output._rawPin],False))

        # overrideType.stateChanged.connect(selector.setEnabled)
        # overrideType.stateChanged.connect(self._rawNode.overrideTypeChanged)
        selector.activated.connect(self._rawNode.updateType)
        structSelector.activated.connect(self._rawNode.selectStructure)
        structSelector.activated.connect(self.selectStructure)

        inputsCategory.insertWidget(0, "DataType", selector)
        #inputsCategory.insertWidget(1,"Change Type On Connection",overrideType)
        inputsCategory.insertWidget(1, "Structure", structSelector)
