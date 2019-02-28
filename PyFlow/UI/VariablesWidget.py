"""@file VariablesWidget.py

Variables input widget. Container for [VariableBase](@ref PyFlow.Core.Variable.VariableBase)
"""
from types import MethodType
import json

from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem

from PyFlow.UI.Widgets.VariablesWidget_ui import Ui_Form
from Variable import VariableBase

VARIABLE_TAG = "VAR"
VARIABLE_NODE_UID_TAG = "UID"


def lwMousePressEvent(self, event):
    QListWidget.mousePressEvent(self, event)
    w = self.itemWidget(self.currentItem())
    if w:
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        dataJson = {VARIABLE_TAG: True, VARIABLE_NODE_UID_TAG: str(w.uid), "Package": None, "PressedText": None}
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
        var = VariableBase(self.graph.getUniqVarName('NewVar'), False, self.graph, self, 'BoolPin', uid=uid)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, var)
        return var
