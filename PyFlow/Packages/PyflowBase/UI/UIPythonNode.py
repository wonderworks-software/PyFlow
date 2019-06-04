from types import MethodType
import subprocess
import os

from Qt.QtWidgets import QAction
from Qt import QtGui, QtCore

from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Views.CodeEditor import CodeEditor
from PyFlow.ConfigManager import ConfigManager


INITIAL_CODE = """

from PyFlow.Core.Common import *

def definePins(node):
    node.createInputPin(pinName="inExec", dataType="ExecPin", foo=node.processNode)
    node.createOutputPin(pinName="outExec", dataType="ExecPin")
    node.createInputPin(pinName="a", dataType="IntPin", defaultValue=0, foo=None, structure=PinStructure.Single, constraint=None, structConstraint=None, allowedPins=[], group="")
    node.createInputPin(pinName="b", dataType="IntPin", defaultValue=0, foo=None, structure=PinStructure.Single, constraint=None, structConstraint=None, allowedPins=[], group="")
    node.createOutputPin(pinName="c", dataType="IntPin", defaultValue=0, structure=PinStructure.Single, constraint=None, structConstraint=None, allowedPins=[], group="")


def compute(node):
    a = node.getData("a")
    b = node.getData("b")
    node.setData("c", a ** b)
    node["outExec"].call()

"""


class UIPythonNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIPythonNode, self).__init__(raw_node)

        self.actionEdit = self._menu.addAction("Edit")
        self.actionEdit.triggered.connect(self.onEdit)
        self._filePath = ''
        self.watcher = QtCore.QFileSystemWatcher()
        self.fileHandle = None

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

    @nodeData.setter
    def nodeData(self, value):
        self._rawNode.nodeData = value

    def onFileChanged(self, path):
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

            self._rawNode.nodeData = codeString

            # create wrappers
            for pin in self._rawNode.getOrderedPins():
                self._createUIPinWrapper(pin)
            self.updateNodeShape()
            self.updateNodeHeaderColor()

    def onEdit(self):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat)
        editCmd = settings.value("Preferences/General/EditorCmd")

        appUserFolder = os.path.expanduser('~/PyFlow')
        if self._filePath == "":
            # if no file assotiated - create one
            self._filePath = os.path.join(appUserFolder, "{0}.py".format(self.getName()))
        if not os.path.exists(self._filePath):
            f = open(self._filePath, 'w')
            f.write(INITIAL_CODE)
            f.close()

        filePathString = '"{}"'.format(self._filePath)
        editCmd = editCmd.replace("@FILE", filePathString)

        # create file watcher
        if self._filePath not in self.watcher.files():
            self.watcher.addPath(self._filePath)

        try:
            self.watcher.fileChanged.disconnect(self.onFileChanged)
        except:
            pass

        self.watcher.fileChanged.connect(self.onFileChanged)
        subprocess.Popen(editCmd)
