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


from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.UI.ContextMenuDataBuilder import ContextMenuDataBuilder

from qtpy import QtGui
from qtpy.QtWidgets import *


class CompileTool(ShelfTool):
    """docstring for CompileTool."""

    def __init__(self):
        super(CompileTool, self).__init__()

    def onSetFormat(self, fmt):
        self.format = fmt

    @staticmethod
    def toolTip():
        return "Ensures everything is ok!"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "compile.png")

    @staticmethod
    def name():
        return str("CompileTool")

    def do(self):
        for node in self.pyFlowInstance.graphManager.get().getAllNodes():
            node.checkForErrors()
