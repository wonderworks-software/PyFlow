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
import os

from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QMessageBox

from PyFlow import GET_PACKAGE_PATH, GET_PACKAGES
from PyFlow.UI.Canvas.UICommon import validateGraphDataPackages
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Utils.stylesheet import Colors
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.Core.Common import *
from PyFlow.UI.EditorHistory import EditorHistory


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
        self.actionExport = self._menu.addAction("Export to package")
        self.actionExport.triggered.connect(self.onExportToPackage)
        self.actionImport = self._menu.addAction("Import")
        self.actionImport.triggered.connect(self.onImport)

    def rebuild(self):
        if self._rawNode._rawGraphJson is not None:
            self.assignData(self._rawNode._rawGraphJson)

    def onExport(self, root=None):
        try:
            savePath, selectedFilter = QFileDialog.getSaveFileName(filter="Subgraph data (*.compound)", dir=root)
        except:
            savePath, selectedFilter = QFileDialog.getSaveFileName(filter="Subgraph data (*.compound)")
        if savePath != "":
            with open(savePath, 'w') as f:
                json.dump(self._rawNode.rawGraph.serialize(), f, indent=4)
            logger.info("{0} data successfully exported!".format(self.getName()))

    def onExportToPackage(self):
        # check if category is not empty
        if self._rawNode._rawGraph.category == '':
            QMessageBox.information(None, "Warning", "Category is not set! Please step into compound and type category name.")
            return

        packageNames = list(GET_PACKAGES().keys())
        selectedPackageName, accepted = QInputDialog.getItem(None, "Select", "Select package", packageNames, editable=False)
        if accepted:
            packagePath = GET_PACKAGE_PATH(selectedPackageName)
            compoundsDir = os.path.join(packagePath, "Compounds")
            if not os.path.isdir(compoundsDir):
                os.mkdir(compoundsDir)
            self.onExport(root=compoundsDir)
            # refresh node box
            app = self.canvasRef().getApp()
            nodeBoxes = app.getRegisteredTools(classNameFilters=["NodeBoxTool"])
            for nodeBox in nodeBoxes:
                nodeBox.refresh()

    def onImport(self):
        openPath, selectedFilter = QFileDialog.getOpenFileName(filter="Subgraph data (*.compound)")
        if openPath != "":
            with open(openPath, 'r') as f:
                data = json.load(f)
                self.assignData(data)

    def assignData(self, data):
        data["isRoot"] = False
        data["parentGraphName"] = self._rawNode.rawGraph.parentGraph.name
        missedPackages = set()
        if validateGraphDataPackages(data, missedPackages):
            data["nodes"] = self.canvasRef().makeSerializedNodesUnique(data["nodes"])
            self._rawNode.rawGraph.populateFromJson(data)
            self.canvasRef().createWrappersForGraph(self._rawNode.rawGraph)
            EditorHistory().saveState("Import compound", modify=True)
        else:
            logger.error("Missing dependencies! {0}".format(",".join(missedPackages)))

    def getGraph(self):
        return self._rawNode.rawGraph

    def stepIn(self):
        self._rawNode.graph().graphManager.selectGraph(self._rawNode.rawGraph)

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
                        wrapper.createInputWidgets(inputsCategory, group="{} inputs".format(node.name), pins=False)
