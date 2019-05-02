from nine import str
from Qt import QtCore
from Qt.QtWidgets import QUndoView
from Qt.QtWidgets import QWidget
from Qt.QtWidgets import QVBoxLayout

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.VariablesWidget import VariablesWidget


class VariablesTool(DockTool):
    """docstring for History tool."""
    def __init__(self):
        super(VariablesTool, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.content = QWidget()
        self.content.setObjectName("VariablesToolContent")
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.setWidget(self.content)

    @staticmethod
    def isSingleton():
        return True

    def onShow(self):
        super(VariablesTool, self).onShow()
        self.verticalLayout.addWidget(VariablesWidget(self.canvas))

    @staticmethod
    def toolTip():
        return "Variables editing/creation"

    @staticmethod
    def name():
        return str("Variables")
