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
import json
from types import MethodType
import uuid

from qtpy import QtCore, QtGui
from qtpy.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QAbstractItemView
)

from PyFlow.PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.PyFlow.UI.Canvas.UIVariable import UIVariable
from PyFlow.PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
from PyFlow.PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.PyFlow.Core.Common import *

VARIABLE_TAG = "VAR"
VARIABLE_DATA_TAG = "VAR_DATA"


class VariablesListWidget(QListWidget):
    """docstring for VariablesListWidget."""
    def __init__(self, parent=None):
        super(VariablesListWidget, self).__init__(parent)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionRectVisible(True)

    def mousePressEvent(self, event):
        super(VariablesListWidget, self).mousePressEvent(event)
        w = self.itemWidget(self.currentItem())
        if w:
            drag = QtGui.QDrag(self)
            mime_data = QtCore.QMimeData()
            varJson = w.serialize()
            dataJson = {VARIABLE_TAG: True, VARIABLE_DATA_TAG: varJson}
            mime_data.setText(json.dumps(dataJson))
            drag.setMimeData(mime_data)
            drag.exec_()


class VariablesWidget(QWidget, Ui_Form):
    """docstring for VariablesWidget"""

    def __init__(self, pyFlowInstance, parent=None):
        super(VariablesWidget, self).__init__()
        self.setupUi(self)
        self.pyFlowInstance = pyFlowInstance
        self.pyFlowInstance.graphManager.get().graphChanged.connect(self.onGraphChanged)
        self.pbNewVar.clicked.connect(self.createVariable)
        self.listWidget = VariablesListWidget()
        self.lytListWidget.addWidget(self.listWidget)
        self.pyFlowInstance.newFileExecuted.connect(self.actualize)

    def actualize(self):
        self.clear()
        # populate current graph
        graph = self.pyFlowInstance.graphManager.get().activeGraph()
        if graph:
            for var in graph.getVarList():
                self.createVariableWrapperAndAddToList(var)

    def onGraphChanged(self, *args, **kwargs):
        self.actualize()

    def clear(self):
        """Does not removes any variable. UI only
        """
        self.listWidget.clear()

    def killVar(self, uiVariableWidget):
        variableGraph = uiVariableWidget._rawVariable.graph
        variableGraph.killVariable(uiVariableWidget._rawVariable)
        self.actualize()

        self.clearProperties()
        EditorHistory().saveState("Kill variable", modify=True)

    def createVariableWrapperAndAddToList(self, rawVariable):
        uiVariable = UIVariable(rawVariable, self)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 20))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable

    def createVariable(self, dataType=str('BoolPin'), accessLevel=AccessLevel.public, uid=None):
        rawVariable = self.pyFlowInstance.graphManager.get().activeGraph().createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)
        uiVariable = self.createVariableWrapperAndAddToList(rawVariable)
        EditorHistory().saveState("Create variable", modify=True)
        return uiVariable

    def clearProperties(self):
        self.pyFlowInstance.onRequestClearProperties()

    def onUpdatePropertyView(self, uiVariable):
        self.pyFlowInstance.onRequestFillProperties(uiVariable.createPropertiesWidget)
