from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QListWidget
from Qt.QtWidgets import QListWidgetItem
import VariablesWidget_ui
from Variable import VariableBase
from types import MethodType
from AbstractGraph import *


def lwMousePressEvent(self, event):
    QListWidget.mousePressEvent(self, event)
    w = self.itemWidget(self.currentItem())
    if w:
        drag = QtGui.QDrag(self)
        mime_data = QtCore.QMimeData()
        mime_data.setText("Var|" + str(w.uid))
        drag.setMimeData(mime_data)
        drag.exec_()


class VariablesWidget(QWidget, VariablesWidget_ui.Ui_Form):
    """docstring for VariablesWidget"""
    def __init__(self, app, graph, parent=None):
        super(VariablesWidget, self).__init__(parent)
        self.setupUi(self)
        self.graph = graph
        self.app = app
        self.pbNewVar.clicked.connect(self.createVariable)
        self.pbKillVar.clicked.connect(self.killVar)
        self.listWidget.mousePressEvent = MethodType(lwMousePressEvent, self.listWidget, QListWidget)

    def killVar(self):
        for i in self.listWidget.selectedItems():
            w = self.listWidget.itemWidget(i)
            if w.uid in self.graph.vars:
                var = self.graph.vars.pop(w.uid)
                row = self.listWidget.row(i)
                self.listWidget.takeItem(row)
                var.killed.emit()
        self.graph._clearPropertiesView()

    def createVariable(self):
        var = VariableBase(self.graph.getUniqVarName('NewVar'), False, self.graph, self, DataTypes.Bool)
        item = QListWidgetItem(self.listWidget)
        item.setSizeHint(QtCore.QSize(60, 38))
        self.listWidget.setItemWidget(item, var)
