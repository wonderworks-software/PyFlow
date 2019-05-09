from Qt import QtCore
from Qt.QtWidgets import QInputDialog

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Widgets.SelectPinDialog import SelectPinDialog
from PyFlow.UI.Utils.Settings import *


class UIGraphInputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphInputs, self).__init__(raw_node)
        actionRename = self._menu.addAction("Rename")
        actionRename.triggered.connect(self.rename)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.createPinDialog)
        self.labelTextColor = Colors.AbsoluteBlack

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

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

        try:
            self.displayName = jsonTemplate['name']
        except:
            self.displayName = self.canvasRef().getUniqNodeDisplayName("Inputs")

    def paint(self, painter, option, widget):
        NodePainter.asGraphSides(self, painter, option, widget)


class UIGraphOutputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphOutputs, self).__init__(raw_node)
        actionRename = self._menu.addAction("Rename")
        actionRename.triggered.connect(self.rename)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.createPinDialog)

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

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

        try:
            self.displayName = jsonTemplate['meta']['label']
        except:
            self.displayName = self.canvasRef().getUniqNodeDisplayName("Outputs")

    def paint(self, painter, option, widget):
        NodePainter.asGraphSides(self, painter, option, widget)
