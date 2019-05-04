"""@file VariablesWidget.py

Variables input widget. Container for [UIVariable](@ref PyFlow.Core.Variable.UIVariable)
"""
from nine import str
import json
from types import MethodType
import uuid

from Qt import QtCore, QtGui
from Qt.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QAbstractItemView
)

from PyFlow.UI.Canvas.UIVariable import UIVariable
from PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.Core.Common import *

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

    def __init__(self, canvas, parent=None):
        super(VariablesWidget, self).__init__(parent)
        self.setupUi(self)
        self.canvas = canvas
        self.canvas.graphManager.graphChanged.connect(self.onGraphChanged)
        self.pbNewVar.clicked.connect(self.createVariable)
        self.listWidget = VariablesListWidget()
        self.lytListWidget.addWidget(self.listWidget)

    def actualize(self):
        self.clear()
        # populate current graph
        graph = self.canvas.graphManager.activeGraph()
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

        # TODO: rewrite properties system
        self.clearProperties()

    def createVariableWrapperAndAddToList(self, rawVariable):
        uiVariable = UIVariable(rawVariable, self)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable

    def createVariable(self, dataType=str('AnyPin'), accessLevel=AccessLevel.public, uid=None):
        rawVariable = self.canvas.graphManager.activeGraph().createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)
        uiVariable = self.createVariableWrapperAndAddToList(rawVariable)
        return uiVariable

    def clearProperties(self):
        propertiesLayout = self.canvas.parent.propertiesLayout
        clearLayout(propertiesLayout)

    def onUpdatePropertyView(self, uiVariable):
        properties = uiVariable.createPropertiesWidget()
        self.canvas.requestFillProperties.emit(properties)
