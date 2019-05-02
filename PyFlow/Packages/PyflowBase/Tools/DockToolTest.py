from nine import str
from Qt import QtCore

from PyFlow.UI.Tool.Tool import DockTool


class DockToolTest(DockTool):
    """docstring for AlignBottomTool."""
    def __init__(self):
        super(DockToolTest, self).__init__()
        self.setMinimumSize(QtCore.QSize(200, 50))

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.TopDockWidgetArea

    @staticmethod
    def showOnStartup():
        return True

    @staticmethod
    def toolTip():
        return "Test dock tool tooltip"

    @staticmethod
    def name():
        return str("TestDockTool")
