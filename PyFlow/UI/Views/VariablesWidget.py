"""@file VariablesWidget.py

Variables input widget. Container for [UIVariable](@ref PyFlow.Core.Variable.UIVariable)
"""
import json
from types import MethodType
import uuid

from Qt import QtCore, QtGui
from Qt.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QWidget,
    QLineEdit,
    QComboBox,
    QAbstractItemView
)

from PyFlow.UI.Canvas.UIVariable import UIVariable, VarTypeComboBox
from PyFlow.UI.Widgets.InputWidgets import createInputWidget
from PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.UI.Widgets.CollapsibleWidget import CollapsibleFormWidget
from PyFlow import getPinDefaultValueByType
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
        self.pbKillVar.clicked.connect(self.killVar)
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

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None):
        rawVariable = self.canvas.graphManager.activeGraph().createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)
        uiVariable = self.createVariableWrapperAndAddToList(rawVariable)
        return uiVariable

    def clearProperties(self):
        formLayout = self.canvas.parent.formLayout
        clearLayout(formLayout)

    @staticmethod
    def createPropertiesWidgetForVariable(rawVariable):
        # TODO: construct properties view here and return
        return None

    def onUpdatePropertyView(self, uiVariable):
        propertiesLayout = self.canvas.parent.propertiesLayout
        clearLayout(propertiesLayout)
        rawVariable = uiVariable._rawVariable

        baseCategory = CollapsibleFormWidget(headName="Base")

        # name
        le_name = QLineEdit(rawVariable.name)
        le_name.returnPressed.connect(lambda: uiVariable.setName(le_name.text()))
        baseCategory.addWidget("Name", le_name)

        # data type
        cbTypes = VarTypeComboBox(uiVariable)
        baseCategory.addWidget("Type", cbTypes)

        valueCategory = CollapsibleFormWidget(headName="Value")

        # current value
        def valSetter(x):
            rawVariable.value = x
        w = createInputWidget(rawVariable.dataType, valSetter, getPinDefaultValueByType(rawVariable.dataType), None)
        if w:
            w.setWidgetValue(rawVariable.value)
            w.setObjectName(rawVariable.name)
            valueCategory.addWidget(rawVariable.name, w)

        # access level
        cb = QComboBox()
        cb.addItem('public', 0)
        cb.addItem('private', 1)
        cb.addItem('protected', 2)

        def accessLevelChanged(x):
            rawVariable.accessLevel = AccessLevel[x]
        cb.currentTextChanged.connect(accessLevelChanged)
        cb.setCurrentIndex(rawVariable.accessLevel)
        valueCategory.addWidget('Access level', cb)
        propertiesLayout.addWidget(baseCategory)
        propertiesLayout.addWidget(valueCategory)
