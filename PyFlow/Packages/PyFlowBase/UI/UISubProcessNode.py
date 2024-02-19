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


from PyFlow.UI.Canvas.UICommon import DEFAULT_IN_EXEC_NAME
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.UI.Canvas.UICommon import NodeActionButtonInfo
from PyFlow.UI.Utils.stylesheet import Colors
from qtpy import QtCore
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QInputDialog


class UISubProcess(UINodeBase):
    pinCreated = QtCore.Signal(object)
    
    def __init__(self, raw_node):
        super(UISubProcess, self).__init__(raw_node)
        actionAddOut = self._menu.addAction("Add option")
        actionAddOut.setToolTip("Add command option")
        actionAddOut.setData(NodeActionButtonInfo(RESOURCES_DIR + "/pin.svg"))
        actionAddOut.triggered.connect(self.onAddInPin)
        self.computeFlagLabel = QLabel("  idle  ")
        self._rawNode.computing.connect(self.onComputing)
        self._rawNode.computed.connect(self.onComputed)
        self.addWidget(self.computeFlagLabel)

    def postCreate(self, jsonTemplate=None):
        super(UISubProcess, self).postCreate(jsonTemplate=jsonTemplate)
        inExecPin = self.getPinSG(DEFAULT_IN_EXEC_NAME)
        inExecPin.bLabelHidden = True

    def onAddInPin(self):
        name, confirmed = QInputDialog.getText(
            None, "Rename", "Enter new pin name")
        if confirmed and name != self.name and name != "":
            name = self._rawNode.getUniqPinName(name)
            rawPin = self._rawNode.addInPin(name, "StringPin")
            uiPin = self._createUIPinWrapper(rawPin)
            self.pinCreated.emit(uiPin)
            self.updateNodeShape()
    
    def postCreate(self, jsonTemplate):
        UINodeBase.postCreate(self, jsonTemplate)
        for uiPin in self.UIPins.values():
            pass

    
    def onComputing(self,*args, **kwargs):
        self.computeFlagLabel.setText("  working  ")
        # self.setComputing(*args, **kwargs)
        
    def onComputed(self,*args, **kwargs):
        self.computeFlagLabel.setText("  idle  ")
        # self.setClean(*args, **kwargs)
        
            