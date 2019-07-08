import os

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

        def setHistoryCapacity():
            EditorHistory().capacity = self.historyDepth.value()
        self.historyDepth.editingFinished.connect(setHistoryCapacity)
        commonCategory.addWidget("History depth", self.historyDepth)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def initDefaults(self, settings):
        settings.setValue("EditorCmd", "sublime_text.exe @FILE")
        settings.setValue("TempFilesDir", os.path.expanduser('~/PyFlowTemp'))

    def serialize(self, settings):
        settings.setValue("EditorCmd", self.lePythonEditor.text())
        settings.setValue("TempFilesDir", self.tempFilesDir.text())
        settings.setValue("ExtraPackageDirs", self.additionalPackagePaths.text())
        settings.setValue("HistoryDepth", self.historyDepth.value())

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
