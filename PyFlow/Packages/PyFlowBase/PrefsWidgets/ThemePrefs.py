import os
import inspect
import json
from collections import defaultdict

from Qt.QtWidgets import *
from Qt import QtGui

from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget, PropertiesWidget
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.UI.Widgets.QtSliders import pyf_ColorSlider, pyf_Slider
from PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.UI.Widgets.PreferencesWindow import *
import PyFlow.UI as UIModule


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
        editableStyleSheet().loadPresests(THEMES_PATH)
        properties = PropertiesWidget()
        properties.setLockCheckBoxVisible(False)
        properties.setTearOffCopyVisible(False)
        general = CollapsibleFormWidget(headName="General")
        bg = CollapsibleFormWidget(headName="BackGround")
        canvas = CollapsibleFormWidget(headName="Canvas")
        options = inspect.getmembers(editableStyleSheet())
        for name, obj in options:
            if isinstance(obj, QtGui.QColor):
                inp = pyf_ColorSlider(type="int", alpha=len(list(obj.getRgbF())) == 4, startColor=list(obj.getRgbF()))
                inp.valueChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color, update))
                if name in ["TextColor", "MainColor", "TextSelectedColor", "ButtonsColor"]:
                    general.addWidget(name, inp)
                elif name in ["InputFieldColor", "BgColor", "BgColorDarker", "BgColorBright", "BorderColor","LoggerBgColor"]:
                    bg.addWidget(name, inp)
                elif name in ["CanvasBgColor", "CanvastextColor", "CanvasGridColor", "CanvasGridColorDarker"]:
                    canvas.addWidget(name, inp)
            elif isinstance(obj, list):
                if name in ["GridSizeFine", "GridSizeHuge"]:
                    inp = pyf_Slider(self)
                    inp.setValue(obj[0])
                    inp.valueChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color,update) )
                elif name in ["DrawNumbers","SetAppStyleSheet"]:
                    inp = QCheckBox()
                    inp.setChecked(obj[0])
                    inp.stateChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color,update) )
                if name != "SetAppStyleSheet":
                    canvas.addWidget(name, inp)
                else:
                    general.insertWidget(0,name,inp)

        self.selector = QComboBox()
        for name in editableStyleSheet().presests.keys():
            self.selector.addItem(name)
        if self.currTheme is not None:
            self.selector.setCurrentIndex(self.currTheme)
        else:
            if isinstance(settings, str):
                if settings in editableStyleSheet().presests:
                    self.selector.setCurrentIndex(list(editableStyleSheet().presests.keys()).index(settings))
            elif settings and settings.value('Theme_Name'):
                if settings.value('Theme_Name') in editableStyleSheet().presests:
                    self.selector.setCurrentIndex(list(editableStyleSheet().presests.keys()).index(settings.value('Theme_Name')))
            self.currTheme = self.selector.currentIndex()

        self.layout.addWidget(self.selector)
        self.selector.activated.connect(self.setPreset)
        general.setCollapsed(True)
        bg.setCollapsed(True)
        canvas.setCollapsed(True)
        properties.addWidget(general)
        properties.addWidget(bg)
        properties.addWidget(canvas)
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
        data = editableStyleSheet().presests[self.selector.currentText()]
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
