import os
import sys
import subprocess
import json
from time import clock
import pkgutil
import uuid

from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QStyleFactory
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QTextEdit
from Qt.QtWidgets import QMessageBox
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QMenu
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QUndoView
from Qt.QtWidgets import QToolButton
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QSpacerItem
from Qt.QtWidgets import QFileDialog
from Qt.QtWidgets import QDockWidget

from PyFlow import Packages
from PyFlow.UI.Canvas.Canvas import Canvas
from PyFlow.Core.Common import Direction
from PyFlow.UI.Canvas.UICommon import clearLayout
from PyFlow.Core.GraphBase import GraphBase
from PyFlow.Core.GraphManager import GraphManager
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.UI.Widgets import GraphEditor_ui
from PyFlow.UI.Utils.StyleSheetEditor import StyleSheetEditor
from PyFlow.UI.Tool.Tool import ShelfTool, DockTool
from PyFlow.Packages.PyflowBase.Tools.PropertiesTool import PropertiesTool
from PyFlow.UI.Tool import GET_TOOLS
from PyFlow import INITIALIZE
from PyFlow.UI.ContextMenuGenerator import ContextMenuGenerator


FILE_DIR = os.path.abspath(os.path.dirname(__file__))
SETTINGS_PATH = os.path.join(FILE_DIR, "appConfig.ini")
STYLE_PATH = os.path.join(FILE_DIR, "style.css")
EDITOR_TARGET_FPS = 120


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


class PluginType:
    pNode = 0
    pCommand = 1
    pFunctionLibrary = 2
    pPin = 3


def _implementPlugin(name, pluginType):
    pass


def getOrCreateMenu(menuBar, title):
    for child in menuBar.findChildren(QMenu):
        if child.title() == title:
            return child
    menu = QMenu(menuBar)
    menu.setObjectName(title)
    menu.setTitle(title)
    return menu


## App itself
class PyFlow(QMainWindow, GraphEditor_ui.Ui_MainWindow):
    newFileExecuted = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super(PyFlow, self).__init__(parent=parent)
        self.setupUi(self)
        self._tools = set()

        self.styleSheetEditor = StyleSheetEditor()
        self.graphManager = GraphManager()
        self.canvasWidget = Canvas(self.graphManager, self)
        self.canvasWidget.requestFillProperties.connect(self.onRequestFillProperties)
        self.canvasWidget.requestClearProperties.connect(self.onRequestClearProperties)
        self.graphManager.graphChanged.connect(self.updateGraphTreeLocation)
        self.updateGraphTreeLocation()
        self.SceneLayout.addWidget(self.canvasWidget)

        rxLettersAndNumbers = QtCore.QRegExp('^[a-zA-Z0-9]*$')
        nameValidator = QtGui.QRegExpValidator(rxLettersAndNumbers, self.leCompoundName)
        self.leCompoundName.setValidator(nameValidator)
        self.leCompoundName.returnPressed.connect(self.onActiveCompoundNameAccepted)

        rxLetters = QtCore.QRegExp('^[a-zA-Z]*$')
        categoryValidator = QtGui.QRegExpValidator(rxLetters, self.leCompoundCategory)
        self.leCompoundCategory.setValidator(categoryValidator)
        self.leCompoundCategory.returnPressed.connect(self.onActiveCompoundCategoryAccepted)

        self.setMouseTracking(True)

        self._lastClock = 0.0
        self.fps = EDITOR_TARGET_FPS
        self.tick_timer = QtCore.QTimer()
        self._current_file_name = 'Untitled'
        self.populateMenu()
        self.dockWidgetNodeView.setVisible(True)

    def populateMenu(self):
        fileMenu = self.menuBar.addMenu("File")
        newFileAction = fileMenu.addAction("New file")
        newFileAction.triggered.connect(self.newFile)

        loadAction = fileMenu.addAction("Load")
        loadAction.triggered.connect(self.load)

        saveAction = fileMenu.addAction("Save")
        saveAction.triggered.connect(self.save)

        saveAsAction = fileMenu.addAction("Save as")
        saveAsAction.triggered.connect(lambda: self.save(True))

        editMenu = self.menuBar.addMenu("Edit")
        preferencesAction = editMenu.addAction("Preferences")

        helpMenu = self.menuBar.addMenu("Help")
        shortcutsAction = helpMenu.addAction("Shortcuts")
        shortcutsAction.triggered.connect(self.shortcuts_info)

    def registerToolInstance(self, instance):
        """Registers tool instance reference

        This needed to prevent classes from being garbage collected and to save widgets state

        Args:

            instance (ToolBase): Tool to be registered
        """
        self._tools.add(instance)

    def unregisterToolInstance(self, instance):
        if instance in self._tools:
            self._tools.remove(instance)

    def onRequestFillProperties(self, propertiesWidget):
        for toolInstance in self._tools:
            if isinstance(toolInstance, PropertiesTool):
                toolInstance.assignPropertiesWidget(propertiesWidget)

    def onRequestClearProperties(self):
        for toolInstance in self._tools:
            if isinstance(toolInstance, PropertiesTool):
                toolInstance.clear()

    def getToolbar(self):
        return self.toolBar

    def getCanvas(self):
        return self.canvasWidget

    def setCompoundPropertiesWidgetVisible(self, bVisible):
        if bVisible:
            self.CompoundPropertiesWidget.show()
            self.leCompoundName.setText(self.graphManager.activeGraph().name)
            self.leCompoundCategory.setText(self.graphManager.activeGraph().category)
        else:
            self.CompoundPropertiesWidget.hide()

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        if all([event.key() == QtCore.Qt.Key_N, modifiers == QtCore.Qt.ControlModifier]):
            self.newFile()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier]):
            self.save()
        if all([event.key() == QtCore.Qt.Key_O, modifiers == QtCore.Qt.ControlModifier]):
            self.load()
        if all([event.key() == QtCore.Qt.Key_S, modifiers == QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier]):
            self.save_as()

    def loadFromData(self, data, fpath=""):
        self.newFile(keepRoot=False)
        # load raw data
        self.graphManager.deserialize(data)
        # create ui nodes
        for graph in self.graphManager.getAllGraphs():
            self.canvasWidget.createWrappersForGraph(graph)
        self.graphManager.selectRootGraph()
        self.variablesWidget.actualize()

    def load(self):
        name_filter = "Graph files (*.json)"
        savepath = QFileDialog.getOpenFileName(filter=name_filter)
        if type(savepath) in [tuple, list]:
            fpath = savepath[0]
        else:
            fpath = savepath
        if not fpath == '':
            with open(fpath, 'r') as f:
                data = json.load(f)
                self.loadFromData(data, fpath)

    def save(self, save_as=False):
        if save_as:
            name_filter = "Graph files (*.json)"
            savepath = QFileDialog.getSaveFileName(filter=name_filter)
            if type(savepath) in [tuple, list]:
                pth = savepath[0]
            else:
                pth = savepath
            if not pth == '':
                self._current_file_name = pth
            else:
                self._current_file_name = "Untitled"
        else:
            if not os.path.isfile(self._current_file_name):
                name_filter = "Graph files (*.json)"
                savepath = QFileDialog.getSaveFileName(filter=name_filter)
                if type(savepath) in [tuple, list]:
                    pth = savepath[0]
                else:
                    pth = savepath
                if not pth == '':
                    self._current_file_name = pth
                else:
                    self._current_file_name = "Untitled"

        if self._current_file_name in ["", "Untitled"]:
            return

        if not self._current_file_name == '':
            with open(self._current_file_name, 'w') as f:
                saveData = self.graphManager.serialize()
                json.dump(saveData, f, indent=4)

            print(str("// saved: '{0}'".format(self._current_file_name)))

    def newFile(self, keepRoot=True):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()

        # broadcast
        self.graphManager.clear(keepRoot=keepRoot)
        self.newFileExecuted.emit(keepRoot)
        self._current_file_name = 'Untitled'
        self.clearPropertiesView()
        self.variablesWidget.actualize()

        self.startMainLoop()

    def updateGraphTreeLocation(self, *args, **kwargs):
        location = self.canvasWidget.location()
        clearLayout(self.layoutGraphPath)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutGraphPath.addItem(spacerItem)
        for folderName in location:
            index = self.layoutGraphPath.count() - 1
            btn = QPushButton(folderName)

            def onClicked(checked, name=None):
                self.canvasWidget.stepToCompound(name)

            btn.clicked.connect(lambda chk=False, name=folderName: onClicked(chk, name))
            self.layoutGraphPath.insertWidget(index, btn)

        self.setCompoundPropertiesWidgetVisible(self.graphManager.activeGraph().depth() > 1)

    def onActiveCompoundNameAccepted(self):
        newName = self.graphManager.getUniqName(self.leCompoundName.text())
        self.graphManager.activeGraph().name = newName
        self.leCompoundName.blockSignals(True)
        self.leCompoundName.setText(newName)
        self.leCompoundName.blockSignals(False)
        self.updateGraphTreeLocation()

    def onActiveCompoundCategoryAccepted(self):
        newCategoryName = self.leCompoundCategory.text()
        self.graphManager.activeGraph().category = newCategoryName

    def startMainLoop(self):
        self.tick_timer.timeout.connect(self.mainLoop)
        self.tick_timer.start(1000 / EDITOR_TARGET_FPS)

    def stopMainLoop(self):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()

    def mainLoop(self):
        deltaTime = clock() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)

        # Tick all graphs
        # each graph will tick owning raw nodes
        # each raw node will tick it's ui wrapper if it exists
        self.graphManager.Tick(deltaTime)

        # Tick canvas. Update ui only stuff such animation etc.
        self.canvasWidget.Tick(deltaTime)

        self._lastClock = clock()

    def createPopupMenu(self):
        pass

    def toggleHistory(self):
        self.dockWidgetUndoStack.setVisible(
            not self.dockWidgetUndoStack.isVisible())

    def newPlugin(self, pluginType):
        name, result = QInputDialog.getText(
            self, 'Plugin name', 'Enter plugin name')
        if result:
            _implementPlugin(name, pluginType)

    def getToolClassByName(self, packageName, toolName, toolClass=DockTool):
        registeredTools = GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass
        return None

    def createToolInstanceByClass(self, packageName, toolName, toolClass=DockTool):
        registeredTools = GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass()
        return None

    def invokeDockToolByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name, DockTool)
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        # Highlight window
                        print("highlight", tool.uniqueName())
                return
        ToolInstance = self.createToolInstanceByClass(packageName, name, DockTool)
        if ToolInstance:
            self.registerToolInstance(ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            else:
                self.addDockWidget(ToolInstance.defaultDockArea(), ToolInstance)
            ToolInstance.setCanvas(self.canvasWidget)
            ToolInstance.onShow()
        return ToolInstance

    def closeEvent(self, event):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()
        self.canvasWidget.shoutDown()
        # save editor config
        settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat, self)
        # clear file each time to capture opened dock tools
        settings.clear()
        settings.sync()

        settings.beginGroup('Editor')
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())
        settings.endGroup()

        # save tools state
        settings.beginGroup('Tools')
        for tool in self._tools:
            if isinstance(tool, ShelfTool):
                settings.beginGroup("ShelfTools")
                settings.beginGroup(tool.uniqueName())
                tool.saveState(settings)
                settings.endGroup()
                settings.endGroup()
            if isinstance(tool, DockTool):
                settings.beginGroup("DockTools")
                settings.beginGroup(tool.uniqueName())
                tool.saveState(settings)
                settings.endGroup()
                settings.endGroup()
            tool.onDestroy()
        settings.endGroup()
        settings.sync()
        QMainWindow.closeEvent(self, event)

    def editTheme(self):
        self.styleSheetEditor.show()

    def updateStyle(self):
        pass
        # if self.styleSheetEditor:
        #    self.setStyleSheet(self.styleSheetEditor.getStyleSheet())

    def togglePropertyView(self):
        if self.dockWidgetNodeView.isVisible():
            self.dockWidgetNodeView.setVisible(False)
        else:
            self.dockWidgetNodeView.setVisible(True)

    def toggleVariables(self):
        if self.dockWidgetVariables.isVisible():
            self.dockWidgetVariables.hide()
        else:
            self.dockWidgetVariables.show()

    def shortcuts_info(self):

        data = "Tab - togle node box\n"
        data += "Ctrl+N - new file\n"
        data += "Ctrl+S - save\n"
        data += "Ctrl+Shift+S - save as\n"
        data += "Ctrl+O - open file\n"
        data += "F - frame selected\n"
        data += "H - frame all\n"
        data += "C - comment selected nodes\n"
        data += "Delete - kill selected nodes\n"
        data += "Ctrl+C - Copy\n"
        data += "Ctrl+V - Paste\n"
        data += "Alt+Drag - Duplicate\n"
        data += "Ctrl+Z - Undo\n"
        data += "Ctrl+Y - Redo\n"
        data += "Alt+Click - Disconnect Pin\n"
        data += "Ctrl+Shift+ArrowLeft - Align left\n"
        data += "Ctrl+Shift+ArrowUp - Align Up\n"
        data += "Ctrl+Shift+ArrowRight - Align right\n"
        data += "Ctrl+Shift+ArrowBottom - Align Bottom\n"

        QMessageBox.information(self, "Shortcuts", data)

    @staticmethod
    def instance(parent=None):
        instance = PyFlow(parent)
        instance.startMainLoop()
        INITIALIZE()

        # populate tools
        canvas = instance.getCanvas()
        toolbar = instance.getToolbar()
        settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)
        instance.restoreGeometry(settings.value('Editor/geometry'))
        instance.restoreState(settings.value('Editor/state'))
        settings.beginGroup("Tools")
        for packageName, registeredToolSet in GET_TOOLS().items():
            for ToolClass in registeredToolSet:
                if issubclass(ToolClass, ShelfTool):
                    ToolInstance = ToolClass()
                    # prevent to be garbage collected
                    instance.registerToolInstance(ToolInstance)
                    ToolInstance.setCanvas(canvas)
                    action = QAction(instance)
                    action.setIcon(ToolInstance.getIcon())
                    action.setText(ToolInstance.name())
                    action.setToolTip(ToolInstance.toolTip())
                    action.setObjectName(ToolInstance.name())
                    action.triggered.connect(ToolInstance.do)
                    # check if context menu data available
                    menuBuilder = ToolInstance.contextMenuBuilder()
                    if menuBuilder:
                        menuGenerator = ContextMenuGenerator(menuBuilder)
                        menu = menuGenerator.generate()
                        action.setMenu(menu)
                    toolbar.addAction(action)

                    # step to ShelfTools/ToolName group and pass settings inside
                    settings.beginGroup("ShelfTools")
                    settings.beginGroup(ToolClass.name())
                    ToolInstance.restoreState(settings)
                    settings.endGroup()
                    settings.endGroup()

                if issubclass(ToolClass, DockTool):
                    menus = instance.menuBar.findChildren(QMenu)
                    helpMenuAction = [m for m in menus if m.title() == "Help"][0].menuAction()
                    toolsMenu = getOrCreateMenu(instance.menuBar, "Tools")
                    instance.menuBar.insertMenu(helpMenuAction, toolsMenu)
                    packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
                    toolsMenu.addMenu(packageSubMenu)
                    showToolAction = packageSubMenu.addAction(ToolClass.name())
                    showToolAction.triggered.connect(lambda pkgName=packageName, toolName=ToolClass.name(): instance.invokeDockToolByName(pkgName, toolName))

                    settings.beginGroup("DockTools")
                    childGroups = settings.childGroups()
                    for dockToolGroupName in childGroups:
                        # This dock tool data been saved on last shutdown
                        settings.beginGroup(dockToolGroupName)
                        if dockToolGroupName in [t.uniqueName() for t in instance._tools]:
                            continue
                        toolName = dockToolGroupName.split("::")[0]
                        ToolInstance = instance.invokeDockToolByName(packageName, toolName, settings)
                        settings.endGroup()
                    settings.endGroup()
        return instance
