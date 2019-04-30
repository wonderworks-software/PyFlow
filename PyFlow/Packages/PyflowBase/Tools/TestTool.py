from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR

from Qt import QtGui


class TestTool(ShelfTool):
    """docstring for TestTool."""
    def __init__(self):
        super(TestTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "py.png")

    @staticmethod
    def name():
        return str("TestTool")

    def do(self):
        super(TestTool, self).do()
