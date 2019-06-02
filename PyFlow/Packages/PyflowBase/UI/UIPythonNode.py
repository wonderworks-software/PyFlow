import subprocess
import os

from Qt.QtWidgets import QAction
from Qt import QtGui, QtCore


from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Views.CodeEditor import CodeEditor
from PyFlow.ConfigManager import ConfigManager


class UIPythonNode(UINodeBase):
    def __init__(self, raw_node):
        super(UIPythonNode, self).__init__(raw_node)

        self.actionEdit = self._menu.addAction("Edit")
        self.actionEdit.triggered.connect(self.onEdit)
        self._filePath = ''
        self.watcher = QtCore.QFileSystemWatcher()
        self.connection = None

    @property
    def compute(self, *args, **kwargs):
        return self._rawNode.compute

    @compute.setter
    def compute(self, value):
        self._rawNode.compute = value

    @property
    def currentComputeCode(self):
        return self._rawNode.currentComputeCode

    @currentComputeCode.setter
    def currentComputeCode(self, value):
        self._rawNode.currentComputeCode = value

    def onFileChanged(self, path):
        if not os.path.exists(path):
            print(path, "removed")
            return
        else:
            print(path, "changed")

    def onEdit(self):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat)
        editCmd = settings.value("Preferences/General/EditorCmd")

        appUserFolder = os.path.expanduser('~/PyFlow')
        if self._filePath == "":
            # if no file assotiated - create one
            self._filePath = os.path.join(appUserFolder, "{0}.py".format(self.getName()))
        if not os.path.exists(self._filePath):
            f = open(self._filePath, 'w')
            f.write("")
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
