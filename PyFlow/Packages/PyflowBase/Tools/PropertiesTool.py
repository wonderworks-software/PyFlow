from nine import str
from Qt import QtCore
from Qt import QtWidgets

from PyFlow.UI.Tool.Tool import DockTool
from PyFlow.UI.Widgets.PropertiesFramework import PropertiesWidget


class PropertiesTool(DockTool):
    """docstring for Properties tool."""
    def __init__(self):
        super(PropertiesTool, self).__init__()
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.setWidget(self.scrollArea)

    def clear(self):
        # clear active properties widget signals?
        currentPropertiesWidget = self.scrollArea.takeWidget()
        if currentPropertiesWidget:
            currentPropertiesWidget.deleteLater()

    def assignPropertiesWidget(self, propertiesWidget):
        if isinstance(propertiesWidget, PropertiesWidget):
            self.clear()
            self.scrollArea.setWidget(propertiesWidget)

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
