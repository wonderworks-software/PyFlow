"""@file UIGetVarNode.py

Builtin node to access variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import VisibilityPolicy
from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Views.VariablesWidget import VariablesWidget
from PyFlow.Core.Common import *
from PyFlow.Core.NodeBase import NodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Canvas.UICommon import *


# Variable getter node
class UIGetVarNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIGetVarNode, self).__init__(raw_node)
        self.image = QtGui.QImage(RESOURCES_DIR + "/variable.png")
        # self.drawlabel = False
        self.headColor = Colors.Gray
        # self.pinsLayout.removeItem(self.inputsLayout)

    @property
    def var(self):
        return self._rawNode.var

    def postCreate(self, jsonTemplate=None):
        super(UIGetVarNode, self).postCreate(jsonTemplate)

        self.updateNodeShape(label=jsonTemplate['meta']['label'])

        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

        outPin = list(self._rawNode.pins)[0]
        outPin.setName(self.var.name)

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onVarDataTypeChanged(self, dataType):
        # recreate pin
        currentPinName = self._rawNode.out.name
        recreatedPin = self._rawNode.recreateOutput(dataType)
        self.UIOut = self._createUIPinWrapper(self._rawNode.out)
        recreatedPin.setName(currentPinName)
        self.updateNodeShape()

    def onVarNameChanged(self, newName):
        uiPin = list(self._rawNode.pins)[0]
        uiPin.setName(newName)
        self.updateNodeShape()

    def sizeHint(self, which, constraint):
        pinSize = PinDefaults().PIN_SIZE
        size = super(UIGetVarNode, self).sizeHint(which, constraint)
        if len(self.UIPins) > 0:
            uiPin = list(self.UIPins.values())[0]
            textWidth = QtGui.QFontMetrics(uiPin._font).width(uiPin.name)
            size.setWidth(textWidth + pinSize * 2 + NodeDefaults().CONTENT_MARGINS * 2 + NodeDefaults().PINS_LAYOUT_SPACING)
            nodeNameWidth = QtGui.QFontMetrics(self.nodeNameFont).width(self.displayName) + NodeDefaults().PINS_LAYOUT_SPACING
            if size.width() < nodeNameWidth:
                size.setWidth(nodeNameWidth)
        return size

    def paint(self, painter, option, widget):
        NodePainter.default(self, painter, option, widget)
