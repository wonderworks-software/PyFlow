from Qt import QtCore

from PyFlow.UI.UINodeBase import UINodeBase
from PyFlow.UI.NodePainter import NodePainter


# self.graph().inPinCreated.connect(self.printTest)
class UIGraphInputs(UINodeBase):
    pinCreated = QtCore.Signal(object)

    def __init__(self, raw_node):
        super(UIGraphInputs, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.onAddOutPin)
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.inputsLayout)
        self.minWidth = 25

    def onAddOutPin(self):
        rawPin = self._rawNode.addOutPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        uiPin.setDisplayName("Input_{}".format(str(len(self.outputs) - 1)))
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def updateNodeShape(self, label=None):
        UINodeBase.updateNodeShape(self, label)

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        self.pinCreated.connect(self.graph().inPinCreated.emit)
        createdPinNames = [pin.name for pin in self.outputs.values()]
        for outPin in jsonTemplate["outputs"]:
            if outPin['name'] not in createdPinNames:
                uiPin = self.onAddOutPin()
        self._displayName = "Inputs"
        self.label().setPlainText("Inputs")
        if "resize" in jsonTemplate['meta']:
            self._rect.setBottom(jsonTemplate['meta']['resize']['h'])
            self._rect.setRight(jsonTemplate['meta']['resize']['w'])
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
        actionAddOut = self._menu.addAction("Add pin")
        actionAddOut.triggered.connect(self.onAddInPin)
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.outputsLayout)
        self.minWidth = 25

    def onAddInPin(self):
        rawPin = self._rawNode.addInPin()
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        uiPin.setDisplayName("Output_{}".format(str(len(self.inputs) - 1)))
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def updateNodeShape(self, label=None):
        UINodeBase.updateNodeShape(self, label)

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        # recreate dynamically created pins
        self.pinCreated.connect(self.graph().outPinCreated.emit)
        createdPinNames = [pin.name for pin in self.inputs.values()]
        for inPin in jsonTemplate["inputs"]:
            if inPin['name'] not in createdPinNames:
                uiPin = self.onAddInPin()
        self._displayName = "outputs"
        self.label().setPlainText("outputs")
        self._rect.setWidth(25)
        self.updateWidth()
        self.nodeMainGWidget.setGeometry(QtCore.QRectF(0, 0, self.w, self.boundingRect().height()))

    def paint(self, painter, option, widget):
        NodePainter.asGraphSides(self, painter, option, widget)
