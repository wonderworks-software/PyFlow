from nine import str

from Qt.QtWidgets import *
from Qt import QtCore, QtGui

from PyFlow.ConfigManager import ConfigManager
from PyFlow.Core.Common import SingletonDecorator


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


@SingletonDecorator
class PreferencesWindow(QMainWindow):
    """docstring for PreferencesWindow."""
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
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

        self.tryCreateDefaults()

    def selectByName(self, name):
        if name in self._indexes:
            index = self._indexes[name][0]
            self.stackedWidget.setCurrentIndex(index)
            self.categoryButtons[index].setChecked(True)

    def tryCreateDefaults(self):
        settings = ConfigManager().getSettings("PREFS")
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
        settings.sync()

    def showEvent(self, event):
        settings = ConfigManager().getSettings("PREFS")
        groups = settings.childGroups()
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            if name not in groups:
                widget.initDefaults(settings)
            widget.onShow(settings)
            settings.endGroup()

    def saveAndClosePrefs(self):
        self.savePreferences()
        self.close()

    def savePreferences(self):
        settings = ConfigManager().getSettings("PREFS")
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            widget.serialize(settings)
            settings.endGroup()
        settings.sync()

    def addCategory(self, name, widget):
        categoryButton = CategoryButton(text=name)
        self.categoriesVerticalLayout.insertWidget(self.categoriesVerticalLayout.count() - 2, categoryButton)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        index = self.stackedWidget.addWidget(widget)
        self._indexes[name] = (index, widget)
        self.categoryButtons[index] = categoryButton
        categoryButton.clicked.connect(lambda checked=False, idx=index: self.switchCategoryContent(idx))

    def switchCategoryContent(self, index):
        self.stackedWidget.setCurrentIndex(index)
        self.categoryButtons[index].toggle()
