from nine import str
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.UI.Widgets.EditPropertiesWidget import EditPropertiesTreeWidget
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
    def __init__(self, label, widget, parent=None, hideLabel=False, maxLabelWidth=None):
        super(PropertyEntry, self).__init__(parent)
        self.label = label
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(1, 1, 1, 1)
        if not hideLabel:
            label = QtWidgets.QLabel(label + ":")
            label.setStyleSheet("font: bold")
            if not maxLabelWidth:
                label.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred))
            else:
                label.setMaximumWidth(maxLabelWidth)
            self.layout.addWidget(label)
        self.layout.addWidget(widget)
        self.index = -1

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
        self.propertyNames = {}
        self.entryNames = {}
        self.updateIcon()
        self.groups = {}

    def setSpacing(self, spacing=2):
        self.Layout.setSpacing(spacing)

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
        for key,value in self.entryNames.items():
            if isinstance(value,PropertyEntry):
                value.setVisible(pattern.lower() in value.getLabel().lower())
        for key,value in self.groups.items():
            if isinstance(value,CollapSibleGoupBox):
                if value.isAllWidgetsHidden():
                    value.hide()
                else:
                    value.show()
                    value.setCollapsed(False)                    

    def insertWidget(self, index=0, label=None, widget=None, maxLabelWidth=None, group=None):
        if widget is None or isinstance(widget, CollapsibleWidget):
            return False
        if group is not None and group != "":
            if group in self.groups:
                groupW = self.groups[group]
            else:
                groupW = CollapSibleGoupBox(group)
                self.groups[group] = groupW
        entry = PropertyEntry(str(label), widget, hideLabel=self.hideLabels, maxLabelWidth=maxLabelWidth)
        self.propertyNames[label] = widget
        self.entryNames[label] = entry
        if group is None or group == "":
            self.Layout.insertWidget(index, entry)
        else:
            groupW.insertWidget(index,entry)
            self.Layout.addWidget(groupW)             
        return True

    def addWidget(self, label=None, widget=None, maxLabelWidth=None,group=None):
        if widget is None or isinstance(widget, CollapsibleWidget):
            return False
        if group is not None and group != "":
            if group in self.groups:
                groupW = self.groups[group]
            else:
                groupW = CollapSibleGoupBox(group)
                self.groups[group] = groupW
        self.propertyNames[label] = widget
        entry = PropertyEntry(str(label), widget, hideLabel=self.hideLabels, maxLabelWidth=maxLabelWidth)
        self.entryNames[label] = entry
        if group is None or group == "":
            self.Layout.addWidget(entry)
        else:
            groupW.addWidget(entry)
            self.Layout.addWidget(groupW)
        return True

    def getWidgetByName(self, name):
        if name in self.propertyNames:
            return self.propertyNames[name]
        else:
            return None

class CollapSibleGoupBox(QtWidgets.QWidget):

    def __init__(self,name):
        super(CollapSibleGoupBox, self).__init__()

        # widgets
        self.controlGroup = QtWidgets.QGroupBox()
        self.controlGroup.setTitle(name)
        self.controlGroup.setCheckable(True)
        self.controlGroup.setChecked(True)

        # groupbox layout
        self.groupLayout = QtWidgets.QVBoxLayout(self.controlGroup)

        self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())

        # signals
        self.controlGroup.toggled.connect(
            lambda: self.toggleCollapsed())

        # layout
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.mainLayout.addWidget(self.controlGroup)

    def isAllWidgetsHidden(self):
        count = self.groupLayout.count()
        hidden = 0
        for i in range(count):
            widget = self.groupLayout.itemAt(i).widget()
            if widget.isHidden():
                hidden += 1
        return count == hidden

    def insertWidget(self,index,widget):
        self.groupLayout.insertWidget(index,widget)
        self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())

    def addWidget(self,widget):
        self.groupLayout.addWidget(widget)
        self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())

    def toggleCollapsed(self):
        state = self.controlGroup.isChecked()
        if state:
            self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())
        else:
            self.controlGroup.setFixedHeight(30)

    def setCollapsed(self, bCollapsed=False):
        self.controlGroup.setChecked(not bCollapsed)
        if not bCollapsed:
            self.controlGroup.setFixedHeight(self.controlGroup.sizeHint().height())
        else:
            self.controlGroup.setFixedHeight(30)

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

        self.settingsButton = QtWidgets.QToolButton()
        self.settingsButton.setIcon(QtGui.QIcon(":/settings.png"))
        self.settingsMenu = QtWidgets.QMenu()
        self.editPropertiesAction = QtWidgets.QAction("Edit Parameter Interface",None)
        self.settingsMenu.addAction(self.editPropertiesAction)
        self.settingsButton.setMenu(self.settingsMenu)
        self.editPropertiesAction.triggered.connect(self.showPropertyEditor)
        #self.settingsButton.clicked.connect(self.spawnDuplicate.emit)
        self.settingsButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)

        self.lockCheckBox = QtWidgets.QToolButton()
        self.lockCheckBox.setCheckable(True)
        self.lockCheckBox.setIcon(QtGui.QIcon(':/unlocked.png'))
        self.lockCheckBox.toggled.connect(self.changeLockIcon)
        self.searchBoxLayout.addWidget(self.lockCheckBox)
        self.tearOffCopy = QtWidgets.QToolButton()
        self.tearOffCopy.setIcon(QtGui.QIcon(":/tear_off_copy_bw.png"))
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

    def changeLockIcon(self,checked):
        if checked:
            self.lockCheckBox.setIcon(QtGui.QIcon(':/locked.png'))
        else:
            self.lockCheckBox.setIcon(QtGui.QIcon(':/unlocked.png'))

    def setLockCheckBoxVisible(self, bVisible):
        self.lockCheckBox.setVisible(bVisible)

    def setTearOffCopyVisible(self, bVisible):
        self.tearOffCopy.setVisible(bVisible)

    def setSearchBoxVisible(self, bVisible):
        self.searchBox.setVisible(bVisible)

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
                    w.setCollapsed(False)

    def isLocked(self):
        return self.lockCheckBox.isChecked() == True

    def clear(self):
        if not self.isLocked():
            clearLayout(self.contentLayout)
            self.searchBoxWidget.hide()
            self.lockCheckBox.setChecked(False)

    def insertWidget(self, collapsibleWidget,index):
        if not self.isLocked():
            if isinstance(collapsibleWidget, CollapsibleFormWidget):
                self.searchBoxWidget.show()
                self.contentLayout.insertWidget(index, collapsibleWidget)
                return True

    def addWidget(self, collapsibleWidget):
        if not self.isLocked():
            if isinstance(collapsibleWidget, CollapsibleFormWidget):
                self.searchBoxWidget.show()
                self.contentLayout.insertWidget(-1, collapsibleWidget)
                return True

    def showPropertyEditor(self):
        tree = EditPropertiesTreeWidget()
        count = self.contentLayout.count()
        folders = {}
        for i in range(count):
            item = self.contentLayout.itemAt(i)
            w = item.widget()        
            if w:
                if w.title() in  ["Inputs"]:
                    for key,group in w.groups.items():
                        if key not in folders:
                            folders[key] = {}
                        #for e in range(group.groupLayout.count()):
                        #    w = group.groupLayout.itemAt(e).widget()
                        #    folders[key][w.getLabel()] = group.groupLayout.itemAt(e).widget()

        for fold in folders:
            folder = tree.addFolder(fold)
            #for widg in folders[fold]:
            #    child = tree.addNormal(widg,folder)

        d = QtWidgets.QDialog()
        d.setLayout(QtWidgets.QHBoxLayout())
        d.layout().addWidget(tree)
        d.exec_()
        newOrder = tree.model_to_dict()


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
