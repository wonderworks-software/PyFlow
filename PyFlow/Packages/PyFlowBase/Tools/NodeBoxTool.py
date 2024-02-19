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


from qtpy import QtCore

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.NodeBox import NodesBox


class NodeBoxTool(DockTool):
    """docstring for NodeBox tool."""

    def __init__(self):
        super(NodeBoxTool, self).__init__()
        self.content = None

    def onShow(self):
        super(NodeBoxTool, self).onShow()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.content = NodesBox(
            self, self.pyFlowInstance.getCanvas(), False, False, bUseDragAndDrop=True
        )
        self.content.setObjectName("NodeBoxToolContent")
        self.setWidget(self.content)

    def refresh(self):
        self.content.treeWidget.refresh()

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def name():
        return "NodeBox"
