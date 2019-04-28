# from PyFlow.UI.Canvas.UICommon import clearLayout

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

    def mousePressEvent(self, event):
        modifires = event.modifiers()
        button = event.button()
        self.parent().bCollapseWithChildren = modifires == QtCore.Qt.ShiftModifier and button == QtCore.Qt.LeftButton
        super(HeadButton, self).mousePressEvent(event)


class CollapsibleWidget(QtWidgets.QWidget):
    """Has content widget and button on top to hide or show content"""

    def __init__(self, parent=None, headName="Collapse", noSpacer=True, collapsed=False):
        super(CollapsibleWidget, self).__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setupUi()
        self.connectUi()
        self.setButtonName(headName)
        self.parentCollapseWidget = None
        self.childrenCollapseWidgets = set()
        self.bCollapseWithChildren = False
        if noSpacer:
            self.removeSpacer()
        self.setCollapsed(collapsed)

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
        self.contentHiddenIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_ArrowRight)
        self.contentVisibleIcon = self.pbHead.style().standardIcon(QtWidgets.QStyle.SP_ArrowDown)
        self.updateIcon()

    def addWidget(self, *args, **kwargs):
        pass

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
        return self.ContentWidget.isVisible()

    def updateIcon(self):
        if self.isCollapsed():
            self.pbHead.setIcon(self.contentVisibleIcon)
        else:
            self.pbHead.setIcon(self.contentHiddenIcon)

    def setCollapsed(self, bCollapsed=False):
        if self.bCollapseWithChildren:
            for child in self.childrenCollapseWidgets:
                child.bCollapseWithChildren = self.bCollapseWithChildren
                child.setCollapsed(bCollapsed)
        if bCollapsed:
            self.ContentWidget.hide()
        else:
            self.ContentWidget.show()
        self.updateIcon()


class PropertiesWidget(QtWidgets.QWidget):
    """docstring for PropertiesWidget."""
    def __init__(self, parent=None):
        super(PropertiesWidget, self).__init__(parent)
        self.lyt = QtWidgets.QVBoxLayout(self)
        self.lyt.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    def clear(self):
        clearLayout(self.lyt)

    def addWidget(self, widget):
        self.lyt.addWidget(widget)


# Example widget
class CollapsibleFormWidget(CollapsibleWidget):
    def __init__(self, parent=None, headName="Collapse", noSpacer=True, collapsed=False):
        super(CollapsibleFormWidget, self).__init__(parent, headName=headName, noSpacer=noSpacer, collapsed=collapsed)
        self.Layout = QtWidgets.QFormLayout(self.ContentWidget)
        self.Layout.setSpacing(2)
        self.Layout.setContentsMargins(0, 0, 0, 5)

    def addWidget(self, label=None, widget=None):
        if widget is None:
            return False
        if isinstance(widget, CollapsibleWidget):
            widget.removeSpacer()
            widget.parentCollapseWidget = self
            self.childrenCollapseWidgets.add(widget)
        if label:
            self.Layout.addRow(str(label), widget)
        else:
            self.Layout.addRow(widget)
        return True


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    s = QtWidgets.QScrollArea()

    pw = PropertiesWidget()

    rootWidget = CollapsibleFormWidget(headName="Settings", noSpacer=False)
    w1 = CollapsibleFormWidget(headName="pins")
    w1.setReadOnly(True)
    w2 = CollapsibleFormWidget(headName="appearance")
    w3 = CollapsibleFormWidget(headName="Appearance|base")

    # Can be nested!!
    rootWidget.addWidget(widget=w1)
    rootWidget.addWidget(widget=w2)
    w2.addWidget(widget=w3)

    w1.addWidget("First", QtWidgets.QPushButton())
    w1.addWidget("Label", QtWidgets.QPushButton())
    w1.addWidget("Sec", QtWidgets.QPushButton())
    w1.addWidget(widget=QtWidgets.QPushButton("separator"))
    w1.addWidget("A", QtWidgets.QPushButton())

    w2.addWidget("First2", QtWidgets.QPushButton())
    w2.addWidget("Label2", QtWidgets.QPushButton())
    w2.addWidget("Sec2", QtWidgets.QPushButton())

    w3.addWidget("Sec3", QtWidgets.QPushButton())

    pw.addWidget(rootWidget)
    s.setWidget(pw)
    s.show()

    sys.exit(app.exec_())
