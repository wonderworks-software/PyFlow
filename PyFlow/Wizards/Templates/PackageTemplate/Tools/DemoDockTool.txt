from qtpy import QtGui

from PyFlow.UI.Tool.Tool import DockTool


class DemoDockTool(DockTool):
    """docstring for History tool."""
    def __init__(self):
        super(DemoDockTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":brick.png")

    @staticmethod
    def toolTip():
        return "My awesome dock tool!"

    @staticmethod
    def name():
        return "DemoDockTool"
