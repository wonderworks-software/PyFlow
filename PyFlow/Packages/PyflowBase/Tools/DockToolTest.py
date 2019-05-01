from nine import str
from PyFlow.UI.Tool.Tool import DockTool


class DockToolTest(DockTool):
    """docstring for AlignBottomTool."""
    def __init__(self, parent=None):
        super(DockToolTest, self).__init__(parent)

    @staticmethod
    def toolTip():
        return "Test dock tool tooltip"

    @staticmethod
    def name():
        return str("Test dock tool")
