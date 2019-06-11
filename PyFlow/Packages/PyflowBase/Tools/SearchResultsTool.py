from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt.QtWidgets import *

from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Widgets.PropertiesFramework import *


class SearchResultsTool(DockTool):
    """docstring for NodeBox tool."""
    def __init__(self):
        super(SearchResultsTool, self).__init__()
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)

        self.content = PropertiesWidget()
        self.content.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.actionClear = QAction("Clear")
        self.actionClear.triggered.connect(self.content.clear)
        self.content.addAction(self.actionClear)

        self.content.setSearchBoxVisible(False)
        self.content.setLockCheckBoxVisible(False)
        self.content.setTearOffCopyVisible(False)

        self.content.setObjectName("SearchResultstent")
        self.scrollArea.setWidget(self.content)
        self.setWindowTitle(self.uniqueName())
        self.setWidget(self.scrollArea)

    def onShowNodesResults(self, uiNodesList):
        self.content.clear()
        category = CollapsibleFormWidget(headName="Results")
        category.setSpacing(0)
        for node in uiNodesList:
            locationString = ">".join(node.location())
            btn = QPushButton(locationString)
            btn.clicked.connect(lambda checked=False, n=node: self.pyFlowInstance.getCanvas().jumpToNode(n))
            category.addWidget(node.getName(), btn)
        self.content.addWidget(category)

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.BottomDockWidgetArea

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":searching-magnifying-glass.png")

    def onShow(self):
        super(SearchResultsTool, self).onShow()
        self.pyFlowInstance.getCanvas().requestShowSearchResults.connect(self.onShowNodesResults)

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def name():
        return str("Search results")
