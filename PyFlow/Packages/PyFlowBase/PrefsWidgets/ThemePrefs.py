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


import os
import inspect
import json
from collections import defaultdict

from qtpy.QtWidgets import *
from qtpy import QtGui

from PyFlow.PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget, PropertiesWidget
from PyFlow.PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.PyFlow.UI.Widgets.QtSliders import pyf_ColorSlider, pyf_Slider
from PyFlow.PyFlow.UI.Utils.stylesheet import editableStyleSheet, ConnectionTypes
from PyFlow.PyFlow.UI.Widgets.PreferencesWindow import *
import PyFlow.PyFlow.UI as UIModule


THEMES_PATH = os.path.join(UIModule.__path__[0], "Themes")


class ThemePreferences(CategoryWidgetBase):
    """docstring for ThemePreferences."""
    def __init__(self, parent=None):
        super(ThemePreferences, self).__init__(parent)
        self.content = QWidget()
        self.layout = QVBoxLayout(self.content)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        self.setWidget(self.content)
        self.currTheme = None

    def onShow(self, settings):
        clearLayout(self.layout)
        editableStyleSheet().loadPresets(THEMES_PATH)
        properties = PropertiesWidget()
        properties.setLockCheckBoxVisible(False)
        properties.setTearOffCopyVisible(False)
        general = CollapsibleFormWidget(headName="General")
        bg = CollapsibleFormWidget(headName="BackGround")
        canvas = CollapsibleFormWidget(headName="Canvas")
        connections = CollapsibleFormWidget(headName="Connections")
        lods = CollapsibleFormWidget(headName="LODS")
        lodMax = None
        lodWidgets = []
        options = inspect.getmembers(editableStyleSheet())
        for name, obj in options:
            if isinstance(obj, QtGui.QColor):
                inp = pyf_ColorSlider(type="int", alpha=len(list(obj.toTuple())) == 4, startColor=list(obj.toTuple()))
                inp.valueChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color, update))
                if name in ["TextColor", "MainColor", "TextSelectedColor", "ButtonsColor"]:
                    general.addWidget(name, inp)
                elif name in ["InputFieldColor", "BgColor", "BgColorDarker", "BgColorBright", "BorderColor", "LoggerBgColor"]:
                    bg.addWidget(name, inp)
                elif name in ["CanvasBgColor", "CanvastextColor", "CanvasGridColor", "CanvasGridColorDarker"]:
                    canvas.addWidget(name, inp)
            elif isinstance(obj, list):
                if name in ["GridSizeFine", "GridSizeHuge", "ConnectionRoundness", "ConnectionOffset"]:
                    inp = pyf_Slider(self)
                    inp.setValue(obj[0])
                    inp.setMinimum(0)
                    inp.setMaximum(1000.0)
                    inp.valueChanged.connect(lambda color, name=name, update=False: editableStyleSheet().setColor(name, color, update))
                elif name in ["DrawNumbers", "SetAppStyleSheet","DrawGrid"]:
                    inp = QCheckBox()
                    inp.setChecked(obj[0])
                    inp.stateChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color, update))
                elif name == "ConnectionMode":
                    inp = QComboBox()
                    for i in ConnectionTypes:
                        inp.addItem(i.name)
                    inp.setCurrentIndex(obj[0])
                    inp.currentIndexChanged.connect(lambda value, name=name, update=False: editableStyleSheet().setColor(name, value, update))
                elif name in ["LOD_Number", "NodeSwitch", "ConnectionSwitch", "PinSwitch", "CanvasSwitch"]:
                    inp = pyf_Slider(self, type="int")
                    inp.setValue(obj[0])
                    if name != "LOD_Number":
                        inp.setMinimum(0)
                        inp.setMaximum(editableStyleSheet().LOD_Number[0])
                        lodWidgets.append(inp)
                    else:
                        lodMax = inp
                        inp.setMinimum(0)
                    inp.valueChanged.connect(lambda color, name=name, update=False: editableStyleSheet().setColor(name, color, update))

                if name in ["ConnectionMode", "ConnectionRoundness","ConnectionOffset"]:
                    connections.addWidget(name, inp)
                elif name == "SetAppStyleSheet":
                    general.insertWidget(0, name, inp)
                elif name in ["NodeSwitch", "ConnectionSwitch", "PinSwitch", "CanvasSwitch"]:
                    lods.addWidget(name, inp)
                elif name == "LOD_Number":
                    lods.insertWidget(0, name, inp)
                else:
                    canvas.addWidget(name, inp)

        for lod in lodWidgets:
            lodMax.valueChanged.connect(lod.setMaximum)

        self.selector = QComboBox()
        for name in editableStyleSheet().presets.keys():
            self.selector.addItem(name)
        if self.currTheme is not None:
            self.selector.setCurrentIndex(self.currTheme)
        else:
            if isinstance(settings, str):
                if settings in editableStyleSheet().presets:
                    self.selector.setCurrentIndex(list(editableStyleSheet().presets.keys()).index(settings))
            elif settings and settings.value('Theme_Name'):
                if settings.value('Theme_Name') in editableStyleSheet().presets:
                    self.selector.setCurrentIndex(list(editableStyleSheet().presets.keys()).index(settings.value('Theme_Name')))
            self.currTheme = self.selector.currentIndex()

        self.layout.addWidget(self.selector)
        self.selector.activated.connect(self.setPreset)

        general.setCollapsed(True)
        bg.setCollapsed(True)
        canvas.setCollapsed(True)
        connections.setCollapsed(True)
        lods.setCollapsed(True)
        properties.addWidget(general)
        properties.addWidget(bg)
        properties.addWidget(canvas)
        properties.addWidget(connections)
        properties.addWidget(lods)
        self.layout.addWidget(properties)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

        lay = QHBoxLayout()
        pbSaveTheme = QPushButton("SaveTheme")
        pbSaveTheme.clicked.connect(self.saveTheme)
        pbSaveThemeAs = QPushButton("SaveThemeAs")
        pbSaveThemeAs.clicked.connect(self.saveThemeAs)
        pbDeleteTheme = QPushButton("RemoveTheme")
        pbDeleteTheme.clicked.connect(self.deleteTheme)
        lay.addWidget(pbSaveTheme)
        lay.addWidget(pbSaveThemeAs)
        lay.addWidget(pbDeleteTheme)
        self.layout.addLayout(lay)

    def setPreset(self, index):
        data = editableStyleSheet().presets[self.selector.currentText()]
        editableStyleSheet().loadFromData(data)
        self.currTheme = self.selector.currentIndex()
        self.onShow(self.selector.currentText())

    def deleteTheme(self):
        if os.path.exists(os.path.join(THEMES_PATH, self.selector.currentText() + ".json")):
            os.remove(os.path.join(THEMES_PATH, self.selector.currentText() + ".json"))
            self.selector.removeItem(self.selector.currentIndex())
            self.onShow(self.selector.currentText())
            self.setPreset(0)

    def saveTheme(self):
        self.saveThemeAs(self.selector.currentText())

    def saveThemeAs(self, fileName=None):
        okPressed = True
        if not fileName:
            fileName, okPressed = QInputDialog.getText(self, "Get text", "Your name:", QLineEdit.Normal, "")
        if okPressed and fileName != '':
            data = editableStyleSheet().serialize()
            with open(os.path.join(THEMES_PATH, fileName + ".json"), "w") as f:
                json.dump(data, f, separators=(',', ':'))
            self.onShow(fileName)

    def serialize(self, settings):
        settings.setValue("Theme_Name", self.selector.currentText())
