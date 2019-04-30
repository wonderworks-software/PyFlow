from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from Qt import QtGui
from Qt.QtWidgets import QFileDialog


class AlignBottomTool(ShelfTool):
    """docstring for AlignBottomTool."""
    def __init__(self):
        super(AlignBottomTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "alignbottom.png")

    @staticmethod
    def name():
        return str("AlignBottomTool")

    def do(self):
        self.canvas.alignSelectedNodes(Direction.Down)
