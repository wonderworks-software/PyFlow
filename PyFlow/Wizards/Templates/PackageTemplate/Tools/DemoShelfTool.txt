from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Core.Common import Direction

from qtpy import QtGui


class DemoShelfTool(ShelfTool):
    """docstring for DemoShelfTool."""
    def __init__(self):
        super(DemoShelfTool, self).__init__()

    @staticmethod
    def toolTip():
        return "This is my new awesome shelf button"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(":brick.png")

    @staticmethod
    def name():
        return "DemoShelfTool"

    def do(self):
        print("Greet!")
