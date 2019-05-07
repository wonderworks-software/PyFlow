"""@file GetVarNode.py

Builtin node to set variable value.
"""
from Qt.QtWidgets import QStyle
from Qt.QtWidgets import QGraphicsItem
from Qt.QtWidgets import QLineEdit
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Utils.Settings import *
from PyFlow.UI.Canvas.UINodeBase import UINodeBase
from PyFlow.Commands.RemoveNodes import RemoveNodes
from PyFlow.UI.Widgets.InputWidgets import createInputWidget


# Variable setter node
class UISetVarNode(UINodeBase):
    """docstring for UISetVarNode"""

    def __init__(self, raw_node):
        super(UISetVarNode, self).__init__(raw_node)
        self.UIIn = None
        self.UIOut = None

    @property
    def var(self):
        return self._rawNode.var

    def serialize(self):
        template = UINodeBase.serialize(self)
        template['meta']['var'] = self.var.serialize()
        return template

    def onUpdatePropertyView(self, formLayout):
        # var name
        leName = QLineEdit(self.var.name)
        leName.setReadOnly(True)
        formLayout.addRow("Name", leName)

        # var type
        leType = QLineEdit(self.var.dataType)
        leType.setReadOnly(True)
        formLayout.addRow("Type", leType)

        # exec input
        inExecWidget = createInputWidget(
            self._rawNode.inExec.dataType, self._rawNode.inExec.call)
        if inExecWidget:
            inExecWidget.setObjectName(self._rawNode.inExec.getName())
            formLayout.addRow(self._rawNode.inExec.name, inExecWidget)
            if self._rawNode.inExec.hasConnections():
                inExecWidget.setEnabled(False)

        # input value
        w = createInputWidget(self._rawNode.inp.dataType,
                              self._rawNode.inp.setData, self.var.value)
        if w:
            w.blockWidgetSignals(True)
            w.setWidgetValue(self._rawNode.inp.currentData())
            w.blockWidgetSignals(False)
            w.setObjectName(self._rawNode.inp.getName())
            formLayout.addRow(self._rawNode.inp.name, w)
            if self._rawNode.inp.hasConnections():
                w.setEnabled(False)

    def onVarDataTypeChanged(self, dataType):
        cmd = RemoveNodes([self], self.graph())
        self.graph().undoStack.push(cmd)

    def postCreate(self, template):
        super(UISetVarNode, self).postCreate(template)
        self.var.nameChanged.connect(self.onVarNameChanged)
        self.var.dataTypeChanged.connect(self.onVarDataTypeChanged)

        # hide all execs labels
        for uiPin in self.UIPins.values():
            if uiPin.isExec():
                uiPin.setDisplayName("")

        self.onVarNameChanged(self.var.name)

    def onVarNameChanged(self, newName):
        self.displayName = 'Set {}'.format(newName)
        self.label().setPlainText(self.displayName)
        self.setName(newName)
        self.updateNodeShape(label=self.displayName)

    @staticmethod
    def category():
        return 'Variables'
