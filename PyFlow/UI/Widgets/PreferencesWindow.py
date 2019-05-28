from Qt.QtWidgets import *
from Qt import QtCore, QtGui
from PyFlow.ConfigManager import ConfigManager


class CategoryButton(QPushButton):
    """docstring for CategoryButton."""
    def __init__(self, icon=None, text="test", parent=None):
        super(CategoryButton, self).__init__(text, parent)
        self.setMinimumHeight(30)


class CategoryWidgetBase(QWidget):
    """docstring for CategoryWidgetBase."""
    def __init__(self, parent=None):
        super(CategoryWidgetBase, self).__init__(parent)

    def serialize(self, settings):
        pass

    def deserialize(self, settings):
        pass


class InputPreferences(CategoryWidgetBase):
    """docstring for InputPreferences."""
    def __init__(self, parent=None):
        super(InputPreferences, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)

        self.layout.addWidget(QLabel("Mouse button"))

        self.cb = QComboBox()
        self.cb.addItems(["Hello", "World"])
        self.layout.addWidget(self.cb)

        spacerItem = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)

    def serialize(self, settings):
        settings.setValue("myComboBoxValue", self.cb.currentText())

    def deserialize(self, settings):
        self.cb.setCurrentIndex(self.cb.findText(settings.value("myComboBoxValue")))


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
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.categoriesVerticalLayout = QVBoxLayout()
        self.categoriesVerticalLayout.setObjectName("categoriesLayout")
        spacer = QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.categoriesVerticalLayout.addItem(spacer)
        self.verticalLayout_3.addLayout(self.categoriesVerticalLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setMinimumWidth(200)
        self.stackedWidget = QStackedWidget(self.splitter)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralWidget)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self._indexes = {}
        self.addCategory("Input", InputPreferences())
        pbSavePrefs = QPushButton("Save")
        pbSavePrefs.clicked.connect(self.savePreferences)
        self.categoriesVerticalLayout.addWidget(pbSavePrefs)

    def showEvent(self, event):
        settings = QtCore.QSettings(ConfigManager().PREFERENCES_CONFIG_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup("Preferences")
        for name, indexWidget in self._indexes.items():
            index, widget = indexWidget
            settings.beginGroup(name)
            widget.deserialize(settings)
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
        index = self.stackedWidget.addWidget(widget)
        self._indexes[name] = (index, widget)
        categoryButton.clicked.connect(lambda idx=index: self.stackedWidget.setCurrentIndex(idx))


if __name__ == "__main__":
    import sys
    a = QApplication(sys.argv)

    w = PreferencesWindow()
    w.show()

    sys.exit(a.exec_())
