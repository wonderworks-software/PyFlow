from Qt import QtCore
from Qt.QtWidgets import QInputDialog

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.Painters import NodePainter
from PyFlow.UI.Utils.Settings import *


class UIGraphInputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphInputs, self).__init__(raw_node)
        actionRename = self._menu.addAction("Rename")
        actionRename.triggered.connect(self.rename)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.onAddOutPin)
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.inputsLayout)
        self.minWidth = 25

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin, color=Colors.AbsoluteBlack)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        uiPin.setDisplayName("Input_{}".format(str(len(self._rawNode.outputs) - 1)))
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        self.pinCreated.connect(self.canvasRef().inPinCreated.emit)
        createdPinNames = [pin.name for pin in self.UIoutputs.values()]
        for outPin in jsonTemplate["outputs"]:
            if outPin['name'] not in createdPinNames:
                uiPin = self.onAddOutPin()
        try:
            self.displayName = jsonTemplate['meta']['label']
        except:
            self.displayName = self.canvasRef().getUniqNodeDisplayName("Inputs")
        self.label().setPlainText(self.displayName)
        if "resize" in jsonTemplate['meta']:
            self._rect.setBottom(jsonTemplate['meta']['resize']['h'])
            self._rect.setRight(jsonTemplate['meta']['resize']['w'])
            self.updateWidth()
            self.w = self._rect.width()
        else:
            self._rect.setWidth(25)
            self.updateWidth()
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w, self.boundingRect().height()))

    def paint(self, painter, option, widget):
        NodePainter.asGraphSides(self, painter, option, widget)


class UIGraphOutputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphOutputs, self).__init__(raw_node)
        actionRename = self._menu.addAction("Rename")
        actionRename.triggered.connect(self.rename)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.onAddInPin)
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.outputsLayout)
        self.minWidth = 25

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

    def onAddInPin(self):
        rawPin = self._rawNode.addInPin()
        uiPin = self._createUIPinWrapper(rawPin, color=Colors.AbsoluteBlack)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        uiPin.setDisplayName("Output_{}".format(str(len(self._rawNode.inputs) - 1)))
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        self.pinCreated.connect(self.canvasRef().outPinCreated.emit)
        createdPinNames = [pin.name for pin in self.UIinputs.values()]
        for inPin in jsonTemplate["inputs"]:
            if inPin['name'] not in createdPinNames:
                uiPin = self.onAddInPin()
        try:
            self.displayName = jsonTemplate['meta']['label']
        except:
            self.displayName = self.canvasRef().getUniqNodeDisplayName("Outputs")
        self.label().setPlainText(self.displayName)
        if "resize" in jsonTemplate['meta']:
            self._rect.setBottom(jsonTemplate['meta']['resize']['h'])
            self._rect.setRight(jsonTemplate['meta']['resize']['w'])
            self.updateWidth()
            self.w = self._rect.width()
        else:
            self._rect.setWidth(25)
            self.updateWidth()
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w, self.boundingRect().height()))

    def paint(self, painter, option, widget):
        NodePainter.asGraphSides(self, painter, option, widget)
