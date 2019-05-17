from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLineEdit
from Qt.QtWidgets import QTextBrowser
from Qt.QtWidgets import QComboBox

from PyFlow.Core.Common import getConnectedPins
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget, PropertiesWidget
from PyFlow.UI.Widgets.InputWidgets import createInputWidget



from PyFlow.Core.Common import *

class UIConstantNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIConstantNode, self).__init__(raw_node)
        self.hover = False
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray

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
        self.displayName = "constant"
        self.updateNodeShape()

    def changeType(self,dataType):
        self._rawNode.changeType(dataType)
        self.canvasRef().tryFillPropertiesView(self)

    def createInputWidgets ( self,propertiesWidget):
        inputsCategory = super(UIConstantNode, self).createInputWidgets(propertiesWidget)
        d = QComboBox()#_PinsListWidget()
        for i in self._rawNode.pinTypes:
            d.addItem(i) 
        if self.input.dataType in self._rawNode.pinTypes:
            d.setCurrentIndex(self._rawNode.pinTypes.index(self.input.dataType))
        d.activated.connect(self.changeType)
        inputsCategory.insertWidget(0,"test",d)
        