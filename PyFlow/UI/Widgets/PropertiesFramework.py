from nine import str
from PyFlow.UI import RESOURCES_DIR
from PyFlow.UI.Canvas.UICommon import clearLayout

from Qt import QtWidgets
from Qt import QtCore, QtGui


# Framework
class HeadButton(QtWidgets.QPushButton):
    """docstring for HeadButton."""
    def __init__(self, parent=None, maxHeight=25):
        super(HeadButton, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setDefault(True)
        self.setMaximumHeight(maxHeight)


class CollapsibleWidget(QtWidgets.QWidget):
    """Has content widget and button on top to hide or show content"""

    def __init__(self, parent=None, headName="Collapse", noSpacer=True, collapsed=False):
        super(CollapsibleWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setupUi()
        self.connectUi()
        self.setButtonName(headName)
        if noSpacer:
            self.removeSpacer()
        self.setCollapsed(collapsed)

    def filterContent(self, pattern):
        pass

    def title(self):
        return self.pbHead.text()

    def setReadOnly(self, bReadOnly=True):
        self.ContentWidget.setEnabled(not bReadOnly)

    def connectUi(self):
        self.pbHead.clicked.connect(self.toggleCollapsed)

    def setupUi(self):
        self.resize(400, 300)
        self.mainVLayout = QtWidgets.QVBoxLayout(self)
        self.mainVLayout.setSpacing(2)
        self.mainVLayout.setContentsMargins(2, 2, 2, 2)
        self.mainVLayout.setObjectName("mainVLayout")
        self.mainVLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.pbHead = HeadButton(self)
        self.mainVLayout.addWidget(self.pbHead)
        self.setMinimumHeight(30)
        self.ContentWidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContentWidget.sizePolicy().hasHeightForWidth())
        self.ContentWidget.setSizePolicy(sizePolicy)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred))
        self.ContentWidget.setObjectName("ContentWidget")
        self.ContentWidget.setContentsMargins(10, 0, 0, 0)
        self.mainVLayout.addWidget(self.ContentWidget)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainVLayout.addItem(self.spacerItem)
        self.setWindowTitle(self.objectName())
        self.pbHead.setStyleSheet(self.pbHead.styleSheet() + "\nText-align:left;")
        self.contentHiddenIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_TitleBarUnshadeButton)
        self.contentVisibleIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_TitleBarShadeButton)
        self.updateIcon()

    def addWidget(self, widget):
        self.mainVLayout.addWidget(widget)

    def removeSpacer(self):
        if self.spacerItem is not None:
            self.mainVLayout.removeItem(self.spacerItem)
            del self.spacerItem
            self.spacerItem = None

    def setContentHiddenIcon(self, icon):
        self.contentHiddenIcon = icon

    def setContentVisibleIcon(self, icon):
        self.contentVisibleIcon = icon

    def toggleCollapsed(self):
        if self.ContentWidget.isVisible():
            self.setCollapsed(True)
        else:
            self.setCollapsed(False)

    def setButtonName(self, name):
        self.pbHead.setText(name)

    def isCollapsed(self):
        return self.ContentWidget.isHidden()

    def updateIcon(self):
        if self.isCollapsed():
            self.pbHead.setIcon(self.contentHiddenIcon)
        else:
            self.pbHead.setIcon(self.contentVisibleIcon)

    def setCollapsed(self, bCollapsed=False):
        self.ContentWidget.setVisible(not bCollapsed)
        self.updateIcon()


class PropertyEntry(QtWidgets.QWidget):
    """docstring for PropertyEntry."""
    def __init__(self, label, widget, parent=None, hideLabel=False):
        super(PropertyEntry, self).__init__(parent)
        self.label = label
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        if not hideLabel:
            label = QtWidgets.QLabel(label)
            label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred))
            self.layout.addWidget(label)
        self.layout.addWidget(widget)

    def getLabel(self):
        return self.label


class CollapsibleFormWidget(CollapsibleWidget):
    def __init__(self, parent=None, headName="Collapse", noSpacer=True, collapsed=False, hideLabels=False):
        super(CollapsibleFormWidget, self).__init__(parent, headName=headName, noSpacer=noSpacer, collapsed=collapsed)
        self.hideLabels = hideLabels
        self.Layout = QtWidgets.QVBoxLayout(self.ContentWidget)
        self.Layout.setObjectName("CollapseWidgetFormLayout")
        self.Layout.setSpacing(2)
        self.Layout.setContentsMargins(0, 0, 0, 5)
        self.updateIcon()

    def isAllWidgetsHidden(self):
        count = self.Layout.count()
        hidden = 0
        for i in range(count):
            widget = self.Layout.itemAt(i).widget()
            if widget.isHidden():
                hidden += 1
        return count == hidden

    def filterContent(self, pattern):
        count = self.Layout.count()
        for i in range(count):
            widget = self.Layout.itemAt(i).widget()
            if widget:
                widget.setVisible(pattern.lower() in widget.getLabel().lower())

    def insertWidget(self, index=0, label=None, widget=None):
        if widget is None or isinstance(widget, CollapsibleWidget):
            return False
        self.Layout.insertWidget(index, PropertyEntry(str(label), widget))
        return True

    def addWidget(self, label=None, widget=None):
        if widget is None or isinstance(widget, CollapsibleWidget):
            return False
        self.Layout.addWidget(PropertyEntry(str(label), widget, hideLabel=self.hideLabels))
        return True


lockUnlockCheckboxStyle = """
QCheckBox {{
    spacing: 5px;
}}
QCheckBox::indicator {{
    width: 20px;
    height: 20px;
}}
QCheckBox::indicator:unchecked {{
    image: url({0});
}}
QCheckBox::indicator:checked {{
    image: url({1});
}}
""".format(RESOURCES_DIR + "/unlocked.png", RESOURCES_DIR + "/locked.png")


class PropertiesWidget(QtWidgets.QWidget):
    """docstring for PropertiesWidget."""
    spawnDuplicate = QtCore.Signal()

    def __init__(self, parent=None, searchByHeaders=False):
        super(PropertiesWidget, self).__init__(parent)
        self.setWindowTitle("Properties view")
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setObjectName("propertiesMainLayout")
        self.mainLayout.setContentsMargins(2, 2, 2, 2)
        self.searchBox = QtWidgets.QLineEdit(self)
        self.searchBox.setObjectName("lineEdit")
        self.searchBox.setPlaceholderText(str("search..."))
        self.searchBox.textChanged.connect(self.filterByHeaders if searchByHeaders else self.filterByHeadersAndFields)
        self.searchBoxWidget = QtWidgets.QWidget()
        self.searchBoxLayout = QtWidgets.QHBoxLayout(self.searchBoxWidget)
        self.searchBoxLayout.setContentsMargins(1, 1, 1, 1)
        self.searchBoxLayout.addWidget(self.searchBox)
        self.lockCheckBox = QtWidgets.QCheckBox()
        self.lockCheckBox.setStyleSheet(lockUnlockCheckboxStyle)
        self.searchBoxLayout.addWidget(self.lockCheckBox)
        self.tearOffCopy = QtWidgets.QPushButton()
        self.tearOffCopy.setStyleSheet("")
        self.tearOffCopy.setFlat(True)
        self.tearOffCopy.setIcon(QtGui.QIcon(RESOURCES_DIR + "/tear_off_copy.png"))
        self.tearOffCopy.clicked.connect(self.spawnDuplicate.emit)
        self.searchBoxLayout.addWidget(self.tearOffCopy)
        self.mainLayout.addWidget(self.searchBoxWidget)
        self.searchBoxWidget.hide()
        self.contentLayout = QtWidgets.QVBoxLayout()
        self.contentLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.mainLayout.addLayout(self.contentLayout)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.mainLayout.addItem(self.spacerItem)
        self.mainLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    def filterByHeaders(self, text):
        count = self.contentLayout.count()
        for i in range(count):
            item = self.contentLayout.itemAt(i)
            w = item.widget()
            if w:
                if text.lower() in w.title().lower():
                    w.show()
                else:
                    w.hide()

    def filterByHeadersAndFields(self, text):
        count = self.contentLayout.count()
        for i in range(count):
            item = self.contentLayout.itemAt(i)
            w = item.widget()
            if w:
                w.filterContent(text)
                if w.isAllWidgetsHidden():
                    w.hide()
                else:
                    w.show()

    def isLocked(self):
        return self.lockCheckBox.checkState() == QtCore.Qt.Checked

    def clear(self):
        if not self.isLocked():
            clearLayout(self.contentLayout)
            self.searchBoxWidget.hide()
            self.lockCheckBox.setChecked(False)

    def addWidget(self, collapsibleWidget):
        if not self.isLocked():
            if isinstance(collapsibleWidget, CollapsibleFormWidget):
                self.searchBoxWidget.show()
                self.contentLayout.insertWidget(-1, collapsibleWidget)
                return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    s = QtWidgets.QScrollArea()

    pw = PropertiesWidget()

    rootWidget = CollapsibleFormWidget(headName="Settings", noSpacer=True)
    rootWidget.addWidget("test", QtWidgets.QPushButton("ss"))
    rootWidget.addWidget("foo", QtWidgets.QPushButton(""))
    rootWidget.addWidget("bar", QtWidgets.QPushButton(""))

    rootWidget2 = CollapsibleFormWidget(headName="Test", noSpacer=True)
    rootWidget2.addWidget("test2", QtWidgets.QPushButton("aa"))

    pw.addWidget(rootWidget)
    pw.addWidget(rootWidget2)
    s.setWidget(pw)
    s.show()

    pw.clear()

    sys.exit(app.exec_())
