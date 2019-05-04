from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from PyFlow.Packages.PyflowBase.Tools import RESOURCES_DIR
from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget


class PropertiesTool(DockTool):
    """docstring for Properties tool."""
    def __init__(self):
        super(PropertiesTool, self).__init__()
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.setWidget(self.scrollArea)
        self.propertiesWidget = PropertiesWidget()
        self.scrollArea.setWidget(self.propertiesWidget)
        self.setWindowTitle(self.uniqueName())

    def clear(self):
        self.propertiesWidget.clear()

    def assignPropertiesWidget(self, propertiesFillDelegate):
        propertiesFillDelegate(self.propertiesWidget)

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "/property_icon.png")

    @staticmethod
    def isSingleton():
        return False

    @staticmethod
    def toolTip():
        return "Properties editing and displaying"

    @staticmethod
    def name():
        return str("Properties")
