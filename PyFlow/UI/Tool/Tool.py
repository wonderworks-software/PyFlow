from nine import str
import uuid
from Qt import QtWidgets
from Qt import QtGui, QtCore


class ToolBase(object):
    """docstring for ToolBase."""
    def __init__(self):
        super(ToolBase, self).__init__()
        self.uid = uuid.uuid4()
        self.canvas = None

    def saveState(self, settings):
        settings.setValue("uid", str(self.uid))
        settings.setValue("name", self.name())

    def restoreState(self, settings):
        uidStr = settings.value("uid")
        if uidStr is not None:
            self.uid = uuid.UUID(uidStr)
        else:
            self.uid = uuid.uuid4()

    def setCanvas(self, canvas):
        if self.canvas is None:
            self.canvas = canvas

    @staticmethod
    def toolTip():
        return "Default tooltip"

    def uniqueName(self):
        return "{0}::{1}".format(self.name(), str(self.uid))

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


class DockTool(QtWidgets.QDockWidget, ToolBase):
    """docstring for DockTool."""
    def __init__(self):
        ToolBase.__init__(self)
        QtWidgets.QDockWidget.__init__(self)
        self.setToolTip(self.toolTip())
        self.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.setMinimumSize(QtCore.QSize(80, 80))
        self.setObjectName(self.uniqueName())

    def restoreState(self, settings):
        super(DockTool, self).restoreState(settings)
        self.setObjectName(self.uniqueName())
        self.setWindowTitle(settings.value("name"))

    def onShow(self):
        print(self.name(), "invoked")

    def onDestroy(self):
        print(self.name(), "destroyed")

    @staticmethod
    def showOnStartup():
        return False

    def closeEvent(self, event):
        self.onDestroy()
        self.parent().unregisterToolInstance(self)
        event.accept()
