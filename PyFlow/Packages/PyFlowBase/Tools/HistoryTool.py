from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.EditorHistory import EditorHistory


class HistoryEntry(QListWidgetItem):
    """docstring for HistoryEntry"""
    enabledBrush = QtGui.QColor(80, 80, 80, 255)
    disabledBrush = enabledBrush.darker(150)

    def __init__(self, state, icon=None):
        super(HistoryEntry, self).__init__(state.text)
        self.state = state
        if icon:
            self.setIcon(icon)
        self.bEnabled = True
        self.setFont(QtGui.QFont("Consolas"))

    def setEnabled(self, bEnabled):
        color = self.enabledBrush if bEnabled else self.disabledBrush
        self.setBackground(color)
        self.setForeground(color.lighter(150))
        self.bEnabled = bEnabled


class HistoryWidget(QListWidget):
    """docstring for HistoryWidget"""
    def __init__(self, parent=None):
        super(HistoryWidget, self).__init__(parent)
        self.currentRowChanged.connect(self.onRowChanged)
        EditorHistory().statePushed.connect(self.addEntry)
        EditorHistory().stateRemoved.connect(self.onRemoveState)
        EditorHistory().stateSelected.connect(self.selectEntry)
        self._data = {}

    def onRemoveState(self, state):
        item = self._data.pop(state)
        row = self.row(item)
        self.takeItem(row)

    def addEntry(self, state):
        item = HistoryEntry(state)
        self._data[state] = item
        self.addItem(item)
        self.selectEntry(state)

    def selectEntry(self, state):
        item = self._data[state]
        row = self.row(item)
        self.setCurrentRow(row, QtCore.QItemSelectionModel.ClearAndSelect)

    def mouseReleaseEvent(self, event):
        super(HistoryWidget, self).mouseReleaseEvent(event)
        item = self.currentItem()
        if item is not None:
            EditorHistory().selectState(item.state)

    def onRowChanged(self, row):
        for i in range(self.count()):
            item = self.item(i)
            itemRow = self.row(item)
            item.setEnabled(itemRow <= row)


class HistoryTool(DockTool):
    """docstring for History tool."""
    def __init__(self):
        super(HistoryTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.content = QWidget()
        self.content.setObjectName("historyToolContent")
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.undoStackWidget = HistoryWidget(self)
        self.undoStackWidget.setObjectName("undoStackWidget")
        self.verticalLayout.addWidget(self.undoStackWidget)
        self.pbClearHistory = QPushButton("Clear history")
        self.pbClearHistory.clicked.connect(self.onClear)
        self.verticalLayout.addWidget(self.pbClearHistory)
        self.setWidget(self.content)

    def onShow(self):
        super(HistoryTool, self).onShow()
        if self.undoStackWidget.count() != EditorHistory().count():
            stack = EditorHistory().getStack()
            for state in stack:
                self.undoStackWidget.addEntry(state)
            self.undoStackWidget.selectEntry(EditorHistory().activeState)

    def onClear(self):
        EditorHistory().clear()
        self.undoStackWidget.clear()

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":history.png")

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Undo stack"

    @staticmethod
    def name():
        return str("History")
