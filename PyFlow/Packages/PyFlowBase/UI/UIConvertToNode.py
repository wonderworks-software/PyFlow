from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QComboBox, QCheckBox

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
