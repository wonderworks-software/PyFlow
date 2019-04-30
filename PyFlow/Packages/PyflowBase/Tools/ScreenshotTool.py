from nine import str
from PyFlow.UI.Tool.Tool import ShelfTool
from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR

from Qt import QtGui
from Qt.QtWidgets import QFileDialog


class ScreenshotTool(ShelfTool):
    """docstring for ScreenshotTool."""
    def __init__(self):
        super(ScreenshotTool, self).__init__()

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "screenshot_icon.png")

    @staticmethod
    def name():
        return str("ScreenshotTool")

    def do(self):
        name_filter = "Image (*.png)"
        fName = QFileDialog.getSaveFileName(filter=name_filter)
        if not fName[0] == '':
            print("save screen to {0}".format(fName[0]))
            img = self.canvas.grab()
            img.save(fName[0], quality=100)
