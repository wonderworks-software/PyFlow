from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QComboBox,QCheckBox

from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow import findPinClassByType


from PyFlow.Core.Common import *

class UIConstantNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIConstantNode, self).__init__(raw_node)
        self.hover = False
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.headColor = self.headColorOverride = QtGui.QColor(*findPinClassByType("AnyPin").color())
        self.selector = None
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
                newOuts.append([connection.destination(), connection.drawDestination])
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
        self.displayName = "constant"
        self.updateNodeShape()

    def changeOnConection(self,other):
        if other.dataType != self.prevDataType:
            self.prevDataType = other.dataType
            self.changeType(other.dataType)

    def changeType(self,dataType):
        self.headColor = self.headColorOverride = QtGui.QColor(*findPinClassByType(dataType).color())
        if self.headColor.lightnessF() > 0.75:
            self.labelTextColor = QtCore.Qt.black
        else:
            self.labelTextColor = QtCore.Qt.white
        self.update()
        self.canvasRef().tryFillPropertiesView(self)

    def overrideTypeChanged(self,toogle):
        self.input._rawPin.changeTypeOnConnection = bool(toogle)
        self.output._rawPin.changeTypeOnConnection = bool(toogle)
        self.selector.setEnabled(toogle)
        
    def createInputWidgets ( self,propertiesWidget):
        inputsCategory = super(UIConstantNode, self).createInputWidgets(propertiesWidget)
        self.selector = QComboBox()
        self.overrideType = QCheckBox()
        self.overrideType.setChecked(self.input._rawPin.changeTypeOnConnection)
        self.overrideType.stateChanged.connect(self.overrideTypeChanged)
        for i in self._rawNode.pinTypes:
            self.selector.addItem(i)         
        if self.input.dataType in self._rawNode.pinTypes:
            self.selector.setCurrentIndex(self._rawNode.pinTypes.index(self.input.dataType))
        self.selector.activated.connect(self._rawNode.updateType)
        self.selector.setEnabled(self.input._rawPin.changeTypeOnConnection)
        inputsCategory.insertWidget(0,"dataType",self.selector)
        inputsCategory.insertWidget(1,"Change Type On Connection",self.overrideType)
        