import json
from collections import defaultdict
import inspect
import os
from Qt.QtWidgets import *
from Qt import QtCore, QtGui
from nine import str

from PyFlow.ConfigManager import ConfigManager
from PyFlow.Input import InputAction, InputManager
from PyFlow.UI.Widgets.MouseButtonCapture import MouseButtonCaptureWidget
from PyFlow.UI.Widgets.KeyboardModifiersCapture import KeyboardModifiersCaptureWidget
from PyFlow.UI.Widgets.KeyCapture import KeyCaptureWidget
from PyFlow.UI.Widgets.InputActionWidget import InputActionWidget
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget, PropertiesWidget
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.UI.Widgets.QtSliders import pyf_ColorSlider, pyf_Slider
from PyFlow.UI.Utils.stylesheet import editableStyleSheet

FILE_DIR = os.path.dirname(__file__)
THEMES_PATH = os.path.join(os.path.dirname(FILE_DIR), "Themes")


class CategoryButton(QPushButton):
    """docstring for CategoryButton."""
    def __init__(self, icon=None, text="test", parent=None):
        super(CategoryButton, self).__init__(text, parent)
        self.setMinimumHeight(30)
        self.setCheckable(True)
        self.setAutoExclusive(True)


class CategoryWidgetBase(QScrollArea):
    """docstring for CategoryWidgetBase."""
    def __init__(self, parent=None):
        super(CategoryWidgetBase, self).__init__(parent)
        self.setWidgetResizable(True)

    def initDefaults(self, settings):
        pass

    def serialize(self, settings):
        pass

    def onShow(self, settings):
        pass


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
                category.addWidget(label=inputActionVariant.getName(), widget=actionWidget,maxLabelWidth=150)
            properties.addWidget(category)
            category.setCollapsed(True)
        self.layout.addWidget(properties)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)


class GeneralPreferences(CategoryWidgetBase):
    """docstring for GeneralPreferences."""
    def __init__(self, parent=None):
        super(GeneralPreferences, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)

        commonCategory = CollapsibleFormWidget(headName="Common")
        self.tempFilesDir = QLineEdit(os.path.expanduser('~/PyFlowTemp'))
        commonCategory.addWidget("TempFilesDir", self.tempFilesDir)
        self.layout.addWidget(commonCategory)

        pythonNodeCategory = CollapsibleFormWidget(headName="Python node")
        self.lePythonEditor = QLineEdit("notepad.exe @FILE")
        pythonNodeCategory.addWidget("Editor cmd", self.lePythonEditor)
        self.layout.addWidget(pythonNodeCategory)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def initDefaults(self, settings):
        settings.setValue("EditorCmd", "notepad.exe @FILE")
        settings.setValue("TempFilesDir", os.path.expanduser('~/PyFlowTemp'))

    def serialize(self, settings):
        settings.setValue("EditorCmd", self.lePythonEditor.text())
        settings.setValue("TempFilesDir", self.tempFilesDir.text())

    def onShow(self, settings):
        self.lePythonEditor.setText(settings.value("EditorCmd"))
        self.tempFilesDir.setText(settings.value("TempFilesDir"))


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
                elif name in ["InputFieldColor", "BgColor", "BgColorDarker", "BgColorBright", "BorderColor"]:
                    bg.addWidget(name, inp)
                elif name in ["CanvasBgColor", "CanvastextColor", "CanvasGridColor", "CanvasGridColorDarker"]:
                    canvas.addWidget(name, inp)
            elif isinstance(obj, list):
                if name in ["GridSizeFine", "GridSizeHuge"]:
                    inp = pyf_Slider(self)
                    inp.setValue(obj[0])
                    inp.valueChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color,update) )
                elif name in ["DrawNumbers"]:
                    inp = QCheckBox()
                    inp.setChecked(obj[0])
                    inp.stateChanged.connect(lambda color, name=name, update=True: editableStyleSheet().setColor(name, color,update) )
                canvas.addWidget(name, inp)
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


class PreferencesWindow(QMainWindow):
    """docstring for PreferencesWindow."""
    def __init__(self, parent=None):
        super(PreferencesWindow, self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle("Preferences")
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QSplitter(self.centralWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.scrollArea = QScrollArea(self.splitter)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 497, 596))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setSpacing(2)
        self.categoriesVerticalLayout = QVBoxLayout()
        self.categoriesVerticalLayout.setObjectName("categoriesLayout")
        spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.categoriesVerticalLayout.addItem(spacer)
        self.verticalLayout_3.addLayout(self.categoriesVerticalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setMinimumWidth(200)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralWidget)
        self.splitter.setSizes([150, 450])
        self._indexes = {}
        self.categoryButtons = {}
        self.buttonsLay = QHBoxLayout()
        pbSavePrefs = QPushButton("SaveAsDefault")
        pbSavePrefs.clicked.connect(self.savePreferences)
        pbSaveAndClosePrefs = QPushButton("SaveAndClose")
        pbSaveAndClosePrefs.clicked.connect(self.saveAndClosePrefs)        
        self.buttonsLay.addWidget(pbSavePrefs)
        self.buttonsLay.addWidget(pbSaveAndClosePrefs)
        self.categoriesVerticalLayout.addLayout(self.buttonsLay)

        self.addCategory("Input", InputPreferences())
        self.addCategory("General", GeneralPreferences())
        self.addCategory("Theme", ThemePreferences())
        self.selectByName("General")
        self.categoryButtons[1].toggle()
        self.tryCreateDefaults()

    def selectByName(self, name):
        if name in self._indexes:
            self.stackedWidget.setCurrentIndex(self._indexes[name][0])

    def tryCreateDefaults(self):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup("Preferences")
        groups = settings.childGroups()
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            bInitDefaults = False
            if name not in groups:
                bInitDefaults = True
            settings.beginGroup(name)
            if bInitDefaults:
                widget.initDefaults(settings)
            settings.endGroup()
        settings.endGroup()
        settings.sync()

    def showEvent(self, event):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup("Preferences")
        groups = settings.childGroups()
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            widget.onShow(settings)
            settings.endGroup()
        settings.endGroup()

    def saveAndClosePrefs(self):
        self.savePreferences()
        self.close()

    def savePreferences(self):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup("Preferences")
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            widget.serialize(settings)
            settings.endGroup()
        settings.endGroup()
        settings.sync()

    def addCategory(self, name, widget):
        categoryButton = CategoryButton(text=name)
        self.categoriesVerticalLayout.insertWidget(0, categoryButton)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        index = self.stackedWidget.addWidget(widget)
        self._indexes[name] = (index, widget)
        self.categoryButtons[index] = categoryButton
        categoryButton.clicked.connect(lambda checked=False, idx=index: self.switchCategoryContent(idx))

    def switchCategoryContent(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.categoryButtons[index].toggle()
