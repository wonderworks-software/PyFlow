from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from Qt import QtGui
from Qt.QtWidgets import QFileDialog


class AlignLeftTool(ShelfTool):
    """docstring for AlignLeftTool."""
    def __init__(self):
        super(AlignLeftTool, self).__init__()

    @staticmethod
    def toolTip():
        return "Aligns selected nodes by left most node"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignleft.png")

    @staticmethod
    def name():
        return str("AlignLeftTool")

    def do(self):
        self.canvas.alignSelectedNodes(Direction.Left)
