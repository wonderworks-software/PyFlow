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
        self.scrollArea = None

    def createContent(self, propertiesWidget):
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.setWidget(self.scrollArea)
        self.scrollArea.setWidget(propertiesWidget)

    def clear(self):
        # clear active properties widget signals?
        currentPropertiesWidget = self.widget()
        if currentPropertiesWidget:
            currentPropertiesWidget.deleteLater()

    def assignPropertiesWidget(self, propertiesWidget):
        if isinstance(propertiesWidget, PropertiesWidget):
            self.clear()
            self.createContent(propertiesWidget)

    @staticmethod
    def getIcon():
        return QtGui.QIcon(RESOURCES_DIR + "/property_icon.png")

    @staticmethod
    def isSingleton():
        return True

    def onShow(self):
        super(PropertiesTool, self).onShow()

    @staticmethod
    def toolTip():
        return "Properties editing and displaying"

    @staticmethod
    def name():
        return str("Properties")
