"""@file VariablesWidget.py

Variables input widget. Container for [UIVariable](@ref PyFlow.Core.Variable.UIVariable)
"""
import json
from types import MethodType
import uuid

from Qt import QtCore, QtGui
from Qt.QtWidgets import QListWidget, QListWidgetItem, QWidget

from PyFlow.UI.UIVariable import UIVariable
from PyFlow.UI.Widgets.VariablesWidget_ui import Ui_Form

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
    def __init__(self, app, graph, parent=None):
        super(VariablesWidget, self).__init__(parent)
        self.setupUi(self)
        self.graph = graph
        self.app = app
        self.pbNewVar.clicked.connect(self.createVariable)
        self.pbKillVar.clicked.connect(self.killVar)
        self.listWidget.mousePressEvent = MethodType(lwMousePressEvent, self.listWidget)
        self.listWidget.setDragDropMode(self.listWidget.InternalMove)
        self.notVisVars = []

    # TODO: this will be removed when scopes will be done
    def setGraph(self, graph):
        self.graph = graph
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            w = self.listWidget.itemWidget(item)
            if w.uid not in self.graph.vars:
                item.setHidden(True)
            else:
                item.setHidden(False)

    def killAll(self):
        self.listWidget.clear()
        self.graph.vars.clear()
        self.graph._clearPropertiesView()

    def killVar(self):
        for i in self.listWidget.selectedItems():
            w = self.listWidget.itemWidget(i)
            if w.uid in self.graph.vars:
                var = self.graph.vars.pop(w.uid)
                row = self.listWidget.row(i)
                self.listWidget.takeItem(row)
                var.killed.emit()
        self.graph._clearPropertiesView()

    def createVariable(self, uid=None):
        rawVariable = self.graph.createVariable()
        # when graph is opened we need to restore guids
        if isinstance(uid, uuid.UUID):
            rawVariable.uid = uid
        uiVariable = UIVariable(rawVariable, self.graph)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable
