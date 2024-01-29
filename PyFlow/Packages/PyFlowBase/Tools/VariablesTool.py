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
from qtpy import QtGui
from qtpy.QtWidgets import QUndoView
from qtpy.QtWidgets import QWidget
from qtpy.QtWidgets import QVBoxLayout

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.VariablesWidget import VariablesWidget


class VariablesTool(DockTool):
    """docstring for Variables tool."""

    def __init__(self):
        super(VariablesTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.varsWidget = None
        self.content = QWidget()
        self.content.setObjectName("VariablesToolContent")
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setWidget(self.content)

    @staticmethod
    def isSingleton():
        return True

    def onShow(self):
        super(VariablesTool, self).onShow()
        self.varsWidget = VariablesWidget(self.pyFlowInstance)
        self.pyFlowInstance.fileBeenLoaded.connect(self.varsWidget.actualize)
        self.verticalLayout.addWidget(self.varsWidget)
        self.varsWidget.actualize()

    def showEvent(self, event):
        super(VariablesTool, self).showEvent(event)
        if self.varsWidget is not None:
            self.varsWidget.actualize()

    @staticmethod
    def toolTip():
        return "Variables editing/creation"

    @staticmethod
    def name():
        return "Variables"
