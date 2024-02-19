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


import json
from collections import defaultdict

from qtpy.QtWidgets import *

from PyFlow.ConfigManager import ConfigManager
from PyFlow.Input import InputManager
from PyFlow.UI.Widgets.PropertiesFramework import (
    CollapsibleFormWidget,
    PropertiesWidget,
)
from PyFlow.UI.Widgets.PreferencesWindow import CategoryWidgetBase
from PyFlow.UI.Widgets.InputActionWidget import InputActionWidget
from PyFlow.UI.Canvas.UICommon import clearLayout


class InputPreferences(CategoryWidgetBase):
    """docstring for InputPreferences."""

    def __init__(self, parent=None):
        super(InputPreferences, self).__init__(parent)
        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        self.setWidget(self.content)

    def serialize(self, settings):
        data = InputManager().serialize()
        with open(ConfigManager().INPUT_CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)

    def onShow(self, settings):
        clearLayout(self.layout)
        properties = PropertiesWidget()
        properties.setLockCheckBoxVisible(False)
        properties.setTearOffCopyVisible(False)

        groupActions = defaultdict(list)
        for actionName, variants in InputManager().getData().items():
            for action in variants:
                groupActions[action.group].append(action)

        for groupName, variants in groupActions.items():
            category = CollapsibleFormWidget(headName=groupName)
            for inputActionVariant in variants:
                actionWidget = InputActionWidget(inputActionRef=inputActionVariant)
                actionWidget.setAction(inputActionVariant)
                category.addWidget(
                    label=inputActionVariant.getName(),
                    widget=actionWidget,
                    maxLabelWidth=150,
                )
            properties.addWidget(category)
            category.setCollapsed(True)
        self.layout.addWidget(properties)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)
