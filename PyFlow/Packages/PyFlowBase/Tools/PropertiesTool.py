## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


from nine import str
from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from PyFlow.Packages.PyFlowBase.Tools import RESOURCES_DIR
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

        self.propertiesWidget.searchBoxLayout.removeWidget(self.propertiesWidget.lockCheckBox)
        self.addButton(self.propertiesWidget.lockCheckBox)
        self.propertiesWidget.searchBoxLayout.removeWidget(self.propertiesWidget.tearOffCopy)
        self.addButton(self.propertiesWidget.tearOffCopy)
        # self.addButton(self.propertiesWidget.settingsButton)

        self.setWindowTitle(self.uniqueName())
        self.fillDelegate = None
        self.propertiesWidget.spawnDuplicate.connect(self.onTearOffCopy)

    def onTearOffCopy(self, *args, **kwargs):
        instance = self.pyFlowInstance.invokeDockToolByName("PyFlowBase", self.name())
        if self.fillDelegate is not None:
            instance.assignPropertiesWidget(self.fillDelegate)
        instance.setFloating(True)
        instance.resize(self.size())

    def clear(self):
        self.propertiesWidget.clear()

    def assignPropertiesWidget(self, propertiesFillDelegate):
        self.fillDelegate = propertiesFillDelegate
        propertiesFillDelegate(self.propertiesWidget)

    @staticmethod
    def isSingleton():
        return False

    @staticmethod
    def toolTip():
        return "Properties editing and displaying"

    @staticmethod
    def name():
        return str("Properties")
