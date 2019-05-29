from Qt.QtWidgets import *
from Qt import QtCore, QtGui

from PyFlow.ConfigManager import ConfigManager
from PyFlow.Input import InputAction, InputManager
from PyFlow.UI.Widgets.MouseButtonCapture import MouseButtonCaptureWidget
from PyFlow.UI.Widgets.KeyboardModifiersCapture import KeyboardModifiersCaptureWidget
from PyFlow.UI.Widgets.KeyCapture import KeyCaptureWidget
from PyFlow.UI.Widgets.InputActionWidget import InputActionWidget
from PyFlow.UI.Widgets.PropertiesFramework import CollapsibleFormWidget
from PyFlow.UI.Canvas.UICommon import clearLayout


class CategoryButton(QPushButton):
    """docstring for CategoryButton."""
    def __init__(self, icon=None, text="test", parent=None):
        super(CategoryButton, self).__init__(text, parent)
        self.setMinimumHeight(30)


class CategoryWidgetBase(QWidget):
    """docstring for CategoryWidgetBase."""
    def __init__(self, parent=None):
        super(CategoryWidgetBase, self).__init__(parent)

    def initDefaults(self):
        pass

    def serialize(self, settings):
        pass

    def onShow(self, settings):
        pass


class InputPreferences(CategoryWidgetBase):
    """docstring for InputPreferences."""
    def __init__(self, parent=None):
        super(InputPreferences, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)

    def serialize(self, settings):
        pass

    def onShow(self, settings):
        clearLayout(self.layout)
        for actionName, variants in InputManager().getData().items():
            category = CollapsibleFormWidget(headName=actionName, hideLabels=True)
            for inputActionVariant in variants:
                actionWidget = InputActionWidget(inputActionRef=inputActionVariant)
                actionWidget.setAction(inputActionVariant)
                category.addWidget(widget=actionWidget)
            self.layout.addWidget(category)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)


class GeneralPreferences(CategoryWidgetBase):
    """docstring for GeneralPreferences."""
    def __init__(self, parent=None):
        super(GeneralPreferences, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(2)
        w = CollapsibleFormWidget(headName="Python node")
        le = QLineEdit("notepad.exe @FILE")
        w.addWidget("Editor cmd:", le)
        self.layout.addWidget(w)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def serialize(self, settings):
        pass


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
        pbSavePrefs = QPushButton("Save")
        pbSavePrefs.clicked.connect(self.savePreferences)
        self.categoriesVerticalLayout.addWidget(pbSavePrefs)

        self.addCategory("Input", InputPreferences())
        self.addCategory("General", GeneralPreferences())
        self.selectByName("General")

    def selectByName(self, name):
        if name in self._indexes:
            self.stackedWidget.setCurrentIndex(self._indexes[name][0])

    def showEvent(self, event):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup("Preferences")
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            widget.onShow(settings)
            settings.endGroup()
        settings.endGroup()

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
        categoryButton.clicked.connect(lambda checked=False, idx=index: self.switchCategoryContent(idx))

    def switchCategoryContent(self, index):
        self.stackedWidget.setCurrentIndex(index)
