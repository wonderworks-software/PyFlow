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


from types import MethodType
import subprocess
import os
import uuid
import logging

from Qt.QtWidgets import QAction
from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QInputDialog
from Qt import QtCore

from PyFlow import GET_PACKAGES
from PyFlow import GET_PACKAGE_PATH
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.ConfigManager import ConfigManager

logger = logging.getLogger(None)


INITIAL_CODE = """

from PyFlow.Core.Common import *

def prepareNode(node):
    node.createInputPin(pinName="inExec", dataType="ExecPin", foo=node.processNode)
    node.createOutputPin(pinName="outExec", dataType="ExecPin")
    node.createInputPin(pinName="a", dataType="IntPin", defaultValue=0, foo=None, structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group="")
    node.createInputPin(pinName="b", dataType="IntPin", defaultValue=0, foo=None, structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group="")
    node.createOutputPin(pinName="c", dataType="IntPin", defaultValue=0, structure=StructureType.Single, constraint=None, structConstraint=None, supportedPinDataTypes=[], group="")


def compute(node):
    a = node.getData("a")
    b = node.getData("b")
    node.setData("c", a ** b)
    node["outExec"].call()

"""


class UIPythonNode(UINodeBase):
    # watcher = QtCore.QFileSystemWatcher()
    watcher = None

    def __init__(self, raw_node):
        super(UIPythonNode, self).__init__(raw_node)

        self.actionEdit = self._menu.addAction("Edit")
        self.actionEdit.triggered.connect(self.onEdit)
        self._filePath = ''

        self.fileHandle = None
        self.currentEditorProcess = None
        self.actionExport = self._menu.addAction("Export")
        self.actionExport.triggered.connect(self.onExport)
        self.actionExport = self._menu.addAction("Export to package")
        self.actionExport.triggered.connect(self.onExportToPackage)
        self.actionImport = self._menu.addAction("Import")
        self.actionImport.triggered.connect(self.onImport)

    def onExportToPackage(self):
        packageNames = list(GET_PACKAGES().keys())
        selectedPackageName, accepted = QInputDialog.getItem(None, "Select", "Select package", packageNames, editable=False)
        if accepted:
            packagePath = GET_PACKAGE_PATH(selectedPackageName)
            pyNodesDir = os.path.join(packagePath, "PyNodes")
            if not os.path.isdir(pyNodesDir):
                os.mkdir(pyNodesDir)
            self.onExport(root=pyNodesDir)
            # refresh node boxes
            app = self.canvasRef().getApp()
            nodeBoxes = app.getRegisteredTools(classNameFilters=["NodeBoxTool"])
            for nodeBox in nodeBoxes:
                nodeBox.refresh()

    def onExport(self, root=None):
        try:
            savePath, selectedFilter = QFileDialog.getSaveFileName(filter="Python node data (*.pynode)", dir=root)
        except:
            savePath, selectedFilter = QFileDialog.getSaveFileName(filter="Python node data (*.pynode)")
        if savePath != "":
            with open(savePath, 'w') as f:
                f.write(self.nodeData)
            logger.info("{0} data successfully exported!".format(self.getName()))

    def onImport(self):
        openPath, selectedFilter = QFileDialog.getOpenFileName(filter="Python node data (*.pynode)")
        if openPath != "":
            with open(openPath, 'r') as f:
                dataString = f.read()
                self.tryApplyNodeData(dataString)
            EditorHistory().saveState("Import python node data", modify=True)

    def mouseDoubleClickEvent(self, event):
        super(UIPythonNode, self).mouseDoubleClickEvent(event)
        self.onEdit()

    @property
    def compute(self, *args, **kwargs):
        return self._rawNode.compute

    @compute.setter
    def compute(self, value):
        self._rawNode.compute = value

    @property
    def nodeData(self):
        return self._rawNode.nodeData

    def rebuild(self):
        if len(self._rawNode._nodeData) > 0:
            self.tryApplyNodeData(self._rawNode._nodeData)

    def eventDropOnCanvas(self):
        self.rebuild()

    def postCreate(self, jsonTemplate=None):
        super(UIPythonNode, self).postCreate(jsonTemplate)
        self.setHeaderHtml(self.getName())

    @nodeData.setter
    def nodeData(self, value):
        self._rawNode.nodeData = value

    def onFileChanged(self, path):
        uidStr = str(self.uid).replace("-", "")
        if uidStr not in path:
            return

        if not os.path.exists(path):
            self._filePath = ''
            if self.fileHandle is not None:
                self.fileHandle.close()
                self.fileHandle = None
            return
        else:
            # open file handle if needed
            if self.fileHandle is None:
                self.fileHandle = open(path, 'r')

            # read code string
            self.fileHandle.seek(0)
            codeString = self.fileHandle.read()

            self.tryApplyNodeData(codeString)

    def tryApplyNodeData(self, dataString):
        try:
            self.nodeData = dataString
            # create wrappers
            for pin in self._rawNode.getOrderedPins():
                self._createUIPinWrapper(pin)
            self.updateNodeShape()
            self.updateNodeHeaderColor()
            self.setHeaderHtml(self.getName())
        except Exception as e:
            logger.warning(e)

    def shoutDown(self):
        if self.fileHandle is not None:
            self.fileHandle.close()

    def kill(self, *args, **kwargs):
        try:
            if self.fileHandle is not None:
                self.fileHandle.close()
            os.remove(self._filePath)
        except:
            pass
        super(UIPythonNode, self).kill()

    def onEdit(self):
        editCmd = ConfigManager().getPrefsValue("PREFS", "General/EditorCmd")
        tempFilesDir = self.canvasRef().getApp().getTempDirectory()

        if self._filePath == "":
            # if no file assotiated - create one
            uidStr = str(self.uid).replace("-", "")
            self._filePath = os.path.join(tempFilesDir, "{}.py".format(uidStr))

        if not os.path.exists(self._filePath):
            f = open(self._filePath, 'w')
            if self.nodeData == "":
                f.write(INITIAL_CODE)
            else:
                f.write(self.nodeData)
            f.close()

        filePathString = '"{}"'.format(self._filePath)
        editCmd = editCmd.replace("@FILE", filePathString)

        # create file watcher
        if UIPythonNode.watcher is None:
            UIPythonNode.watcher = QtCore.QFileSystemWatcher()
        if self._filePath not in UIPythonNode.watcher.files():
            UIPythonNode.watcher.addPath(self._filePath)

        try:
            UIPythonNode.watcher.fileChanged.disconnect(self.onFileChanged)
        except:
            pass

        result = UIPythonNode.watcher.fileChanged.connect(self.onFileChanged)
        self.currentEditorProcess = subprocess.Popen(editCmd)
        self.fileHandle = open(self._filePath, 'r')
