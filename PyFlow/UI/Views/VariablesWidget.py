"""@file VariablesWidget.py

Variables input widget. Container for [UIVariable](@ref PyFlow.Core.Variable.UIVariable)
"""
import json
from types import MethodType
import uuid

from Qt import QtCore, QtGui
from Qt.QtWidgets import QListWidget, QListWidgetItem, QWidget

from PyFlow.UI.Graph.UIVariable import UIVariable
from PyFlow.UI.Views.VariablesWidget_ui import Ui_Form
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

    def __init__(self, app, parent=None):
        super(VariablesWidget, self).__init__(parent)
        self.setupUi(self)
        self.app = app
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
        rawVariable = self.graph.createVariable(
            dataType=dataType, accessLevel=accessLevel, uid=uid)
        uiVariable = UIVariable(rawVariable, self.graph)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, uiVariable)
        return uiVariable
