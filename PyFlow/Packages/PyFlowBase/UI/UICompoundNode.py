from Qt import QtWidgets

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.Core.Common import *


class UICompoundNode(UINodeBase):
    def __init__(self, raw_node):
        super(UICompoundNode, self).__init__(raw_node)
        self._rawNode.pinExposed.connect(self._createUIPinWrapper)
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.image = RESOURCES_DIR + "/gear.svg"
        self.heartBeatDelay = 1.0

    def getGraph(self):
        return self._rawNode.rawGraph

    def stepIn(self):
        self._rawNode.graph().graphManager.selectGraphByName(self.name)

    def mouseDoubleClickEvent(self, event):
        self.stepIn()
        event.accept()

    def kill(self, *args, **kwargs):
        super(UICompoundNode, self).kill()

    def onGraphNameChanged(self, newName):
        self.name = newName
        self.setHeaderHtml(self.name)

    def postCreate(self, jsonTemplate=None):
        super(UICompoundNode, self).postCreate(jsonTemplate)
        self.canvasRef().createWrappersForGraph(self._rawNode.rawGraph)
        self._rawNode.rawGraph.nameChanged.connect(self.onGraphNameChanged)

    def createInputWidgets(self, inputsCategory, group=None, pins=True):
        if pins:
            super(UICompoundNode, self).createInputWidgets(inputsCategory, group)
        nodes = self._rawNode.rawGraph.getNodesList()
        if len(nodes) > 0:
            for node in nodes:
                wrapper = node.getWrapper()
                if wrapper is not None:
                    if wrapper.bExposeInputsToCompound:
                        wrapper.createInputWidgets(inputsCategory, group="{} inputs".format(node.name),pins=False)
