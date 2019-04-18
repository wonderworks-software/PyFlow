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
        actionAddOut.triggered.connect(lambda: self.onAddOutPin())
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.inputsLayout)
        self.minWidth = 25

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

    def onAddOutPin(self, name=None):
        rawPin = self._rawNode.addOutPin(name)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.getLabel()().setColor(Colors.AbsoluteBlack)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def postCreate(self, jsonTemplate):
        # this call will create wrappers for raw pins
        UINodeBase.postCreate(self, jsonTemplate)
        for uiPin in self.UIPins.values():
            uiPin.getLabel()().setColor(Colors.AbsoluteBlack)

        self.pinCreated.connect(self.canvasRef().inPinCreated.emit)

        try:
            self.displayName = jsonTemplate['name']
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
        actionAddOut.triggered.connect(lambda: self.onAddInPin())
        self.label().hide()
        self.resizable = True
        self.portsMainLayout.removeItem(self.outputsLayout)
        self.minWidth = 25

    def rename(self):
        name, confirmed = QInputDialog.getText(None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            self.displayName = self.canvasRef().getUniqNodeDisplayName(name)
            self.update()

    def onAddInPin(self, name=None):
        rawPin = self._rawNode.addInPin(name)
        uiPin = self._createUIPinWrapper(rawPin)
        uiPin.getLabel()().setColor(Colors.AbsoluteBlack)
        uiPin.setDynamic(True)
        uiPin.setRenamingEnabled(True)
        self.updateWidth()
        self.pinCreated.emit(uiPin)
        return uiPin

    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        for uiPin in self.UIPins.values():
            uiPin.getLabel()().setColor(Colors.AbsoluteBlack)
        # recreate dynamically created pins
        self.pinCreated.connect(self.canvasRef().outPinCreated.emit)

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
