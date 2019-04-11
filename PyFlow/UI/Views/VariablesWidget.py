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
    QComboBox
)

from PyFlow.UI.Canvas.UIVariable import UIVariable, VarTypeComboBox
from PyFlow.UI.Widgets.InputWidgets import createInputWidget
from PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
from PyFlow import getPinDefaultValueByType
from PyFlow.Core.Common import *

VARIABLE_TAG = "VAR"
VARIABLE_DATA_TAG = "VAR_DATA"


def lwMousePressEvent(self, event):
    QListWidget.mousePressEvent(self, event)
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
        self.pbNewVar.clicked.connect(self.createVariable)
        self.pbKillVar.clicked.connect(self.killVar)
        self.listWidget.mousePressEvent = MethodType(
            lwMousePressEvent, self.listWidget)
        self.listWidget.setDragDropMode(self.listWidget.InternalMove)
        self.notVisVars = []

    def killAll(self):
        self.listWidget.clear()

    def killVar(self):
        # remove variable from owning graph
        # send events
        pass

    def createVariable(self, dataType='AnyPin', accessLevel=AccessLevel.public, uid=None):
        rawVariable = self.canvas.graphManager.activeGraph().createVariable(dataType=dataType, accessLevel=accessLevel, uid=uid)
        uiVariable = UIVariable(rawVariable, self)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable

    def onUpdatePropertyView(self, uiVariable):
        formLayout = self.canvas.parent.formLayout
        rawVariable = uiVariable._rawVariable

        # name
        le_name = QLineEdit(rawVariable.name)
        le_name.returnPressed.connect(lambda: var.setName(le_name.text()))
        formLayout.addRow("Name", le_name)

        # data type
        cbTypes = VarTypeComboBox(uiVariable)
        formLayout.addRow("Type", cbTypes)

        # current value
        def valSetter(x):
            rawVariable.value = x
        w = createInputWidget(rawVariable.dataType, valSetter, getPinDefaultValueByType(rawVariable.dataType), None)
        if w:
            w.setWidgetValue(rawVariable.value)
            w.setObjectName(rawVariable.name)
            formLayout.addRow(rawVariable.name, w)
        # access level
        cb = QComboBox()
        cb.addItem('public', 0)
        cb.addItem('private', 1)
        cb.addItem('protected', 2)

        def accessLevelChanged(x):
            rawVariable.accessLevel = AccessLevel[x]
        cb.currentTextChanged.connect(accessLevelChanged)
        cb.setCurrentIndex(rawVariable.accessLevel)
        formLayout.addRow('Access level', cb)
