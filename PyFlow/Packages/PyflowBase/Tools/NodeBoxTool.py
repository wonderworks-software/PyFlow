from nine import str
from Qt import QtCore
from Qt import QtGui

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Views.NodeBox import NodesBox


class NodeBoxTool(DockTool):
    """docstring for NodeBox tool."""
    def __init__(self):
        super(NodeBoxTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":node_box_icon.png")

    def onShow(self):
        super(NodeBoxTool, self).onShow()
        self.setMinimumSize(QtCore.QSize(200, 50))
        self.content = NodesBox(self, False)
        self.content.setObjectName("NodeBoxToolContent")
        self.setWidget(self.content)

    @staticmethod
    def isSingleton():
        return True

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def toolTip():
        return "Available nodes"

    @staticmethod
    def name():
        return str("NodeBox")
