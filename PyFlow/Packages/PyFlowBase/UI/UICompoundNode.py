## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import json
import logging

from Qt.QtWidgets import QFileDialog

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.Core.Common import *


logger = logging.getLogger(None)


class UICompoundNode(UINodeBase):
    def __init__(self, raw_node):
        super(UICompoundNode, self).__init__(raw_node)
        self._rawNode.pinExposed.connect(self._createUIPinWrapper)
        self.headColorOverride = Colors.Gray
        self.color = Colors.DarkGray
        self.image = RESOURCES_DIR + "/gear.svg"
        self.heartBeatDelay = 1.0

        self.actionExport = self._menu.addAction("Export")
        self.actionExport.triggered.connect(self.onExport)
        self.actionImport = self._menu.addAction("Import")
        self.actionImport.triggered.connect(self.onImport)

    def onExport(self):
        savePath, selectedFilter = QFileDialog.getSaveFileName(filter="Subgraph data (*.json)")
        if savePath != "":
            with open(savePath, 'w') as f:
                json.dump(self._rawNode.rawGraph.serialize(), f)
            logger.info("{0} data successfully exported!".format(self.getName()))

    def onImport(self):
        openPath, selectedFilter = QFileDialog.getOpenFileName(filter="Subgraph data (*.json)")
        if openPath != "":
            with open(openPath, 'r') as f:
                data = json.load(f)
                data["nodes"] = self.canvasRef().makeSerializedNodesUnique(data["nodes"])
                self._rawNode.rawGraph.populateFromJson(data)
                self.canvasRef().createWrappersForGraph(self._rawNode.rawGraph)

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
