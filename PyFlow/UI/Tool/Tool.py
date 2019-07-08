from nine import str
import uuid
from Qt import QtWidgets
from Qt import QtGui, QtCore

from PyFlow.UI.Utils.stylesheet import editableStyleSheet

class ToolBase(object):
    """docstring for ToolBase."""
    packageName = ""

    def __init__(self):
        super(ToolBase, self).__init__()
        self.uid = uuid.uuid4()
        self.pyFlowInstance = None

    def onShow(self):
        print(self.name(), "invoked")

    def onDestroy(self):
        print(self.name(), "destroyed")

    def saveState(self, settings):
        settings.setValue("uid", str(self.uid))

    def restoreState(self, settings):
        uidStr = settings.value("uid")
        if uidStr is not None:
            self.uid = uuid.UUID(uidStr)
        else:
            self.uid = uuid.uuid4()

    def setAppInstance(self, pyFlowInstance):
        if self.pyFlowInstance is None:
            self.pyFlowInstance = pyFlowInstance

    @staticmethod
    def toolTip():
        return "Default tooltip"

    def uniqueName(self):
        return "{0}::{1}".format(self.name(), str(self.uid))

    @staticmethod
    def name():
        return "ToolBase"


class ShelfTool(ToolBase):
    """docstring for ShelfTool."""
    def __init__(self):
        super(ShelfTool, self).__init__()

    def contextMenuBuilder(self):
        return None

    @staticmethod
    def getIcon():
        return QtGui.QIcon.fromTheme("go-home")

    def do(self):
        print(self.name(), "called!", self.canvas)


class DockTool(QtWidgets.QDockWidget, ToolBase):
    """docstring for DockTool."""
    def __init__(self):
        ToolBase.__init__(self)
        QtWidgets.QDockWidget.__init__(self)
        self.setToolTip(self.toolTip())
        self.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.setObjectName(self.uniqueName())
        self.setTitleBarWidget(DockTitleBar(self))
        self.setFloating(False)

    @staticmethod
    def defaultDockArea():
        return QtCore.Qt.LeftDockWidgetArea

    @staticmethod
    def isSingleton():
        return False

    def onShow(self):
        super(DockTool, self).onShow()
        self.setWindowTitle(self.name())

    @staticmethod
    def getIcon():
        return None

    def restoreState(self, settings):
        super(DockTool, self).restoreState(settings)
        self.setObjectName(self.uniqueName())

    @staticmethod
    def showOnStartup():
        return False

    def closeEvent(self, event):
        self.onDestroy()
        self.parent().unregisterToolInstance(self)
        event.accept()

    def addButton(self,button):
        self.titleBarWidget().addButton(button)

class DockTitleBar(QtWidgets.QWidget):
    def __init__(self, dockWidget,renamable=False):
        super(DockTitleBar, self).__init__(dockWidget)
        self.renamable = renamable
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,1)
        self.buttonsLay = QtWidgets.QHBoxLayout()
        self.buttonsLay.setSpacing(1)
        self.buttonsLay.setMargin(1)
        self.box = QtWidgets.QGroupBox("")
        self.box.setLayout(self.buttonsLay)
        self.box.setObjectName("Docked")
        self.layout().addWidget(self.box)

        self.box.mouseDoubleClickEvent = self.mouseDoubleClickEvent
        self.box.mousePressEvent = self.mousePressEvent        
        self.box.mouseMoveEvent = self.mouseMoveEvent 
        self.box.mouseReleaseEvent = self.mouseReleaseEvent

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setStyleSheet("background:transparent")
        self.titleEdit = QtWidgets.QLineEdit(self)
        self.titleEdit.hide()
        self.titleEdit.editingFinished.connect(self.finishEdit)

        self.buttonSize = QtCore.QSize(14, 14)

        self.dockButton = QtWidgets.QToolButton(self)
        self.dockButton.setIcon(QtGui.QIcon(':/split_window.png'))
        self.dockButton.setMaximumSize(self.buttonSize)
        self.dockButton.setAutoRaise(True)
        self.dockButton.clicked.connect(self.toggleFloating)

        self.closeButton = QtWidgets.QToolButton(self)
        self.closeButton.setMaximumSize(self.buttonSize)
        self.closeButton.setAutoRaise(True)
        self.closeButton.setIcon(QtGui.QIcon(':/close_window.png'))
        self.closeButton.clicked.connect(self.closeParent)

        self.buttonsLay.addSpacing(2)
        self.buttonsLay.addWidget(self.titleLabel)
        self.buttonsLay.addWidget(self.titleEdit)
        self.buttonsLay.addStretch()
        self.buttonsLay.addSpacing(5)
        self.buttonsLay.addWidget(self.dockButton)
        self.buttonsLay.addWidget(self.closeButton)

        dockWidget.featuresChanged.connect(self.onFeaturesChanged)

        self.onFeaturesChanged(dockWidget.features())
        self.setTitle(dockWidget.windowTitle())
        dockWidget.installEventFilter(self)
        dockWidget.topLevelChanged.connect(self.ChangeFloatingStyle)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.WindowTitleChange:
            self.setTitle(source.windowTitle())
        return super(DockTitleBar, self).eventFilter(source, event)

    def startEdit(self):
        self.titleLabel.hide()
        self.titleEdit.show()
        self.titleEdit.setFocus()

    def finishEdit(self):
        self.titleEdit.hide()
        self.titleLabel.show()
        self.parent().setWindowTitle(self.titleEdit.text())

    def onFeaturesChanged(self, features):
        if not features & QtWidgets.QDockWidget.DockWidgetVerticalTitleBar:
            self.closeButton.setVisible(
                features & QtWidgets.QDockWidget.DockWidgetClosable)
            self.dockButton.setVisible(
                features & QtWidgets.QDockWidget.DockWidgetFloatable)
        else:
            raise ValueError('vertical title bar not supported')

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleEdit.setText(title)

    def ChangeFloatingStyle(self,state):
        if not state:
            self.box.setStyleSheet(editableStyleSheet().getStyleSheet())
        else:
            self.box.setStyleSheet("""QGroupBox{
                                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 %s,
                                stop: 0.6 %s,
                                stop: 1.0 %s);}"""%("rgba%s" % str(editableStyleSheet().ButtonsColor.getRgb()),
                                                    "rgba%s" % str(editableStyleSheet().BgColorBright.getRgb()),
                                                    "rgba%s" % str(editableStyleSheet().BgColorBright.getRgb())))
        
        
    def update(self,*args,**kwargs):
        self.ChangeFloatingStyle(self.parent().isFloating())
        super(DockTitleBar, self).update(*args,**kwargs)

    def toggleFloating(self):
        self.parent().setFloating(not self.parent().isFloating())

    def closeParent(self):
        self.parent().toggleViewAction().setChecked(False)
        self.parent().close()

    def mouseDoubleClickEvent(self, event):
        if event.pos().x() <= self.titleLabel.width() and self.renamable:
            self.startEdit()
        else:
            # this keeps the normal double-click behaviour
            super(DockTitleBar, self).mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, event):
        event.ignore()

    def addButton(self,button):
        button.setAutoRaise(True)
        button.setMaximumSize(self.buttonSize)
        self.buttonsLay.insertWidget(5,button)