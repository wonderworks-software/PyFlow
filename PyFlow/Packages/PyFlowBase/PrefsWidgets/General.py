## Copyright 2015-2019 Ilgar Lunin, Pedro Cabrera
## Copyright 2022 Stephan Helma

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

from Qt import QtCore
from Qt.QtWidgets import *

from PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.UI.Widgets.PreferencesWindow import CategoryWidgetBase


class GeneralPreferences(CategoryWidgetBase):
    """docstring for GeneralPreferences."""
    def __init__(self, parent=None):
        super(GeneralPreferences, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)

        commonCategory = CollapsibleFormWidget(headName="Common")
        defaultTempFolder = os.path.join(os.path.expanduser('~'), "PyFlowTemp")
        defaultTempFolder = os.path.normpath(defaultTempFolder)
        self.tempFilesDir = QLineEdit(defaultTempFolder)
        commonCategory.addWidget("TempFilesDir", self.tempFilesDir)
        self.additionalPackagePaths = QLineEdit("")
        commonCategory.addWidget("Additional package locations", self.additionalPackagePaths)
        self.layout.addWidget(commonCategory)

        self.lePythonEditor = QLineEdit("sublime_text.exe @FILE")
        commonCategory.addWidget("External text editor", self.lePythonEditor)

        self.historyDepth = QSpinBox()
        self.historyDepth.setRange(10, 100)

        def setHistoryCapacity(val):
            EditorHistory().capacity = val
        self.historyDepth.editingFinished.connect(setHistoryCapacity)
        commonCategory.addWidget("History depth", self.historyDepth)

        self.autoZoom = QCheckBox(self)
        self.autoZoom.stateChanged.connect(self.setZoom)
        commonCategory.addWidget("Automatic zoom", self.autoZoom)

        self.adjAutoZoom = QDoubleSpinBox()
        self.adjAutoZoom.setMinimum(0)
        self.adjAutoZoom.setSingleStep(0.1)
        self.adjAutoZoom.valueChanged.connect(self.setZoom)
        commonCategory.addWidget("Adjust automatic zoom", self.adjAutoZoom)

        self.initialZoom = QDoubleSpinBox()
        self.initialZoom.setMinimum(0)
        self.initialZoom.setSingleStep(0.1)
        self.initialZoom.valueChanged.connect(self.setZoom)
        commonCategory.addWidget("Initial zoom factor", self.initialZoom)

        self.redirectOutput = QCheckBox(self)
        commonCategory.addWidget("Redirect output", self.redirectOutput)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def setZoom(self):
        pyflow = self.parent().parent().parent().parent().parent()
        if self.autoZoom.checkState() == QtCore.Qt.Checked:
            # Auto zoom
            zoom = self.adjAutoZoom.value()
            pyflow.canvasWidget.canvas.setAutoZoom(zoom)
        else:
            # Manual zoom
            zoom = self.initialZoom.value()
            pyflow.canvasWidget.canvas.setZoom(zoom)

    def initDefaults(self, settings):
        settings.setValue("EditorCmd", "sublime_text.exe @FILE")
        settings.setValue("TempFilesDir", os.path.expanduser('~/PyFlowTemp'))
        settings.setValue("HistoryDepth", 50)
        settings.setValue("AutoZoom", True)
        settings.setValue("AdjAutoZoom", 1)
        settings.setValue("InitialZoom", 1)
        settings.setValue("RedirectOutput", True)

    def serialize(self, settings):
        settings.setValue("EditorCmd", self.lePythonEditor.text())
        settings.setValue("TempFilesDir", self.tempFilesDir.text())
        settings.setValue("ExtraPackageDirs", self.additionalPackagePaths.text())
        settings.setValue("HistoryDepth", self.historyDepth.value())
        settings.setValue("AutoZoom", self.autoZoom.checkState() == QtCore.Qt.Checked)
        settings.setValue("AdjAutoZoom", self.adjAutoZoom.value())
        settings.setValue("InitialZoom", self.initialZoom.value())
        settings.setValue("RedirectOutput", self.redirectOutput.checkState() == QtCore.Qt.Checked)

    def onShow(self, settings):
        self.lePythonEditor.setText(settings.value("EditorCmd"))
        path = settings.value("TempFilesDir")
        path = os.path.normpath(path)
        self.tempFilesDir.setText(path)
        self.additionalPackagePaths.setText(settings.value("ExtraPackageDirs"))

        try:
            self.historyDepth.setValue(int(settings.value("HistoryDepth")))
        except:
            pass

        self.autoZoom.setChecked(settings.value("AutoZoom") != "false")
        try:
            self.adjAutoZoom.setValue(float(settings.value("AdjAutoZoom")))
        except:
            self.adjAutoZoom.setValue(1)

        try:
            self.initialZoom.setValue(float(settings.value("InitialZoom")))
        except:
            self.initialZoom.setValue(1)

        try:
            self.redirectOutput.setChecked(settings.value("RedirectOutput") == "true")
        except:
            pass
