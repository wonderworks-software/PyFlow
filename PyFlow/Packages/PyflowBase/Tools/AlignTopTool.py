from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.Core.Common import Direction

from Qt import QtGui
from Qt.QtWidgets import QFileDialog


class AlignTopTool(ShelfTool):
    """docstring for AlignTopTool."""
    def __init__(self):
        super(AlignTopTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "aligntop.png")

    @staticmethod
    def name():
        return str("AlignTopTool")

    def do(self):
        self.canvas.alignSelectedNodes(Direction.Up)
