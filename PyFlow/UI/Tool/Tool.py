from nine import str
from Qt import QtWidgets
from Qt import QtGui, QtCore


class ToolBase(object):
    """docstring for ToolBase."""
    def __init__(self):
        super(ToolBase, self).__init__()
        self.canvas = None

    def setCanvas(self, canvas):
        if self.canvas is None:
            self.canvas = canvas

    @staticmethod
    def toolTip():
        return "Default tooltip"

    @staticmethod
    def name():
        return "ToolBase"


class ShelfTool(ToolBase):
    """docstring for ShelfTool."""
    def __init__(self):
        super(ShelfTool, self).__init__()

    def contextMenuBuilder(self):
        return None

    @staticmethod
    def getIcon():
        return QtGui.QIcon.fromTheme("go-home")

    def do(self):
        print(self.name(), "called!", self.canvas)
