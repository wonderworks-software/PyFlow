from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.UI.ContextMenuDataBuilder import ContextMenuDataBuilder

from Qt import QtGui
from Qt.QtWidgets import *


class CompileTool(ShelfTool):
    """docstring for CompileTool."""
    def __init__(self):
        super(CompileTool, self).__init__()

    def onSetFormat(self, fmt):
        self.format = fmt

    @staticmethod
    def toolTip():
        return "Ensures everything is ok!"

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "compile.png")

    @staticmethod
    def name():
        return str("CompileTool")

    def do(self):
        QMessageBox.information(self.pyFlowInstance, "Info", "Smart code goes here")
