from Qt import QtCore

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Widgets.SelectPinDialog import SelectPinDialog
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UICommon import *


class UIGraphInputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphInputs, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.createPinDialog)
        self.color = Colors.DarkGray
        self.headColorOverride = Colors.Gray
        self.image = RESOURCES_DIR + "/gear.svg"

    def setName(self, name):
        oldName = self.getName()
        super(UIGraphInputs, self).setName(name)
        owningCompoundNode = self.canvasRef().graphManager.findNode(
            self._rawNode.graph().name)
        if owningCompoundNode:
            uiCompoundNode = owningCompoundNode.getWrapper()
            if oldName in uiCompoundNode.groups["input"]:
                grpItem = uiCompoundNode.groups["input"][oldName]
                grpItem.name = name
            if oldName in owningCompoundNode.groups["input"]:
                for inp in owningCompoundNode.groups["input"][oldName]:
                    inp.grop = name
                owningCompoundNode.groups["input"][name] = owningCompoundNode.groups["input"].pop(oldName)

    def createPinDialog(self):
        self.d = SelectPinDialog()
        self.d.exec_()
        dataType = self.d.getResult()
        if dataType is not None:
            self.onAddOutPin(None, dataType)

    def onAddOutPin(self, name=None, dataType="AnyPin"):
        rawPin = self._rawNode.addOutPin(name, dataType)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.labelColor = Colors.AbsoluteBlack
        self.pinCreated.emit(uiPin)
        self.updateNodeShape()
        return uiPin

    def postCreate(self, jsonTemplate):
        # this call will create wrappers for raw pins
        UINodeBase.postCreate(self, jsonTemplate)

        for uiPin in self.UIPins.values():
            uiPin.labelColor = Colors.AbsoluteBlack


class UIGraphOutputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphOutputs, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.createPinDialog)

        self.color = Colors.DarkGray
        self.headColorOverride = Colors.Gray
        self.image = RESOURCES_DIR + "/gear.svg"

    def setName(self, name):
        oldName = self.getName()
        super(UIGraphOutputs, self).setName(name)
        owningCompoundNode = self.canvasRef().graphManager.findNode(
            self._rawNode.graph().name)
        if owningCompoundNode:
            uiCompoundNode = owningCompoundNode.getWrapper()
            if oldName in uiCompoundNode.groups["output"]:
                grpItem = uiCompoundNode.groups["output"][oldName]
                grpItem.name = name

    def createPinDialog(self):
        self.d = SelectPinDialog()
        self.d.exec_()
        dataType = self.d.getResult()
        if dataType is not None:
            self.onAddInPin(None, dataType)

    def onAddInPin(self, name=None, dataType="AnyPin"):
        rawPin = self._rawNode.addInPin(name, dataType)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.labelColor = Colors.AbsoluteBlack
        self.pinCreated.emit(uiPin)
        self.updateNodeShape()
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        for uiPin in self.UIPins.values():
            uiPin.labelColor = Colors.AbsoluteBlack
