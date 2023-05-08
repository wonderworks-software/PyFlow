## Copyright 2023 David Lario

## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at

##     http://www.apache.org/licenses/LICENSE-2.0

## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import os
import sys
import subprocess
import json
from time import process_time
import pkgutil
import uuid
import shutil
from string import ascii_letters
import random

from PySide6.QtCore import QCoreApplication
#import mdi_rc
from qtpy import QtGui
from qtpy import QtCore
from qtpy.QtWidgets import *

from PyFlow.PyFlow import GET_PACKAGES
from PyFlow.PyFlow.Core.Common import SingletonDecorator
from PyFlow.PyFlow.Core.PathsRegistry import PathsRegistry
from PyFlow.PyFlow.Core.version import *
from PyFlow.PyFlow.Core.GraphBase import GraphBase
from PyFlow.PyFlow.Core.GraphManager import GraphManagerSingleton
from PyFlow.PyFlow.ConfigManager import ConfigManager
from PyFlow.PyFlow.UI.Canvas.UICommon import *
from PyFlow.PyFlow.UI.Widgets.BlueprintCanvas import BlueprintCanvasWidget
from PyFlow.PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.PyFlow.UI.Canvas.UINodeBase import getUINodeInstance
from PyFlow.PyFlow.UI.Tool.Tool import ShelfTool, DockTool, FormTool
from PyFlow.PyFlow.UI.EditorHistory import EditorHistory
from PyFlow.PyFlow.UI.Tool import GET_TOOLS
from PyFlow.PyFlow.UI.Tool import REGISTER_TOOL
from PyFlow.PyFlow.UI.Utils.stylesheet import editableStyleSheet
from PyFlow.PyFlow.UI.ContextMenuGenerator import ContextMenuGenerator
from PyFlow.PyFlow.UI.Widgets.PreferencesWindow import PreferencesWindow
try:
    from PyFlow.PyFlow.Packages.PyFlowBase.Tools.PropertiesTool import PropertiesTool
except:
    pass
from PyFlow.PyFlow.UI.Forms.PackageBuilder import PackageBuilder
from PyFlow.PyFlow import INITIALIZE
from PyFlow.PyFlow.Input import InputAction, InputActionType
from PyFlow.PyFlow.Input import InputManager
from PyFlow.PyFlow.ConfigManager import ConfigManager
from PyFlow.PyFlow.UI.Canvas.CanvasBase import CanvasBase

import PyFlow.PyFlow.UI.resources

EDITOR_TARGET_FPS = 60

from qtpy.QtCore import (QSignalMapper, QRect, QSize, Qt, QFile, QFileInfo, QTextStream, QPoint, QSettings)
from qtpy.QtGui import (QIcon, QKeySequence, QUndoStack)
from qtpy.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMdiSubWindow, QMessageBox, QWidget, QMenuBar)

'''from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QWidget, QMenuBar)'''

def generateRandomString(numSymbolds=5):
    result = ""
    for i in range(numSymbolds):
        letter = random.choice(ascii_letters)
        result += letter
    return result

def getOrCreateMenu(menuBar, title):
    for child in menuBar.findChildren(QMenu):
        if child.title() == title:
            return child
    menu = QMenu(menuBar)
    menu.setObjectName(title)
    menu.setTitle(title)
    return menu


def winTitle():
    return "PyFlow v{0}".format(currentVersion().__str__())

class pyflowChild(QMdiSubWindow):
    sequenceNumber = 1
    newFileExecuted = QtCore.Signal(bool)
    fileBeenLoaded = QtCore.Signal()

    def __init__(self, parent):
        super(pyflowChild, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.isUntitled = True
        self.guid = uuid.uuid4()
        self.parent = parent
        self.graphManager = GraphManagerSingleton()
        self.canvasWidget = BlueprintCanvasWidget(self.graphManager.get(), self)
        self.canvasWidget.setObjectName("canvasWidget")
        self._currentFileName = ""

        self.setWidget(self.canvasWidget)
        self._tools = set()

        self._lastClock = 0.0
        self.fps = EDITOR_TARGET_FPS
        self.tick_timer = QtCore.QTimer(self)

        self.isModified = False
        self._modified = False

        #self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

        self.currentSoftware = ""
        self.edHistory = EditorHistory(self)
        self.edHistory.statePushed.connect(self.historyStatePushed)

        self.readSettings()
        self.currentTempDir = ""

        self.preferencesWindow = PreferencesWindow(self)
        self.populateToolBar()
        self.createActions()

        '''self.instanceDict[None] = self

        self.instanceDict = {}
        self.instanceDict[None] = self'''

        self.startMainLoop()

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QtCore.QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def historyStatePushed(self, state):
        if state.modifiesData():
            self.modified = True
            self.updateLabel()
        # print(state, state.modifiesData())

    @property
    def modified(self):
        return self._modified

    @modified.setter
    def modified(self, value):
        self._modified = value
        self.updateLabel()

    def updateLabel(self):
        label = self._currentFileName
        if self.currentFileName is not None:
            if os.path.isfile(self.currentFileName):
                label = os.path.basename(self.currentFileName)
        if self.modified:
            label += "*"
        self.setWindowTitle("{0}".format(label))

    def getTempDirectory(self):
        """Returns unique temp directory for application instance.

        This folder and all it's content will be removed from disc on application shutdown.
        """
        if self.currentTempDir == "":
            # create app folder in documents
            # random string used for cases when multiple instances of app are running in the same time
            tempDirPath = ConfigManager().getPrefsValue("PREFS", "General/TempFilesDir")
            if tempDirPath[-1:] in ('/', '\\'):
                tempDirPath = tempDirPath[:-1]
            self.currentTempDir = "{0}_{1}".format(tempDirPath, generateRandomString())

            if not os.path.exists(self.currentTempDir):
                os.makedirs(self.currentTempDir)
        return self.currentTempDir


    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
            self.cut()

    def copy(self):
            self.copy()

    def paste(self):
            self.paste()

    def createActions(self):
        self.newAct = QAction(QIcon(':/images/new.png'), "&New", self,
                              shortcut=QKeySequence.New, statusTip="Create a new file",
                              triggered=self.parent.newFile)

        self.openAct = QAction(QIcon(':/images/open.png'), "&Open...", self,
                               shortcut=QKeySequence.Open, statusTip="Open an existing file",
                               triggered=self.parent.open)

        self.saveAct = QAction(QIcon(':/images/save.png'), "&Save", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                                 shortcut=QKeySequence.SaveAs,
                                 statusTip="Save the document under a new name",
                                 triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
                               statusTip="Exit the application",
                               triggered=QApplication.instance().closeAllWindows)

        self.cutAct = QAction(QIcon(':/images/cut.png'), "Cu&t", self,
                              shortcut=QKeySequence.Cut,
                              statusTip="Cut the current selection's contents to the clipboard",
                              triggered=self.cut)

        self.copyAct = QAction(QIcon(':/images/copy.png'), "&Copy", self,
                               shortcut=QKeySequence.Copy,
                               statusTip="Copy the current selection's contents to the clipboard",
                               triggered=self.copy)

        self.pasteAct = QAction(QIcon(':/images/paste.png'), "&Paste", self,
                                shortcut=QKeySequence.Paste,
                                statusTip="Paste the clipboard's contents into the current selection",
                                triggered=self.paste)

        self.closeAct = QAction("Cl&ose", self,
                                statusTip="Close the active window",
                                triggered=self.parent.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,
                                   statusTip="Close all the windows",
                                   triggered=self.parent.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows",
                               triggered=self.parent.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self,
                                  statusTip="Cascade the windows",
                                  triggered=self.parent.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.parent.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                                   shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.parent.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.parent.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

    def getMenuBar(self):
        return self.menuBar

    def getToolBarLayout(self):

        toolBarDict = {}
        pyFlowToolBar = []
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "NewFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "NewFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "OpenFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "SaveFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "AlignLeft",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "AlignRight",
                              "Active": True})

        toolBarDict["File"] = pyFlowToolBar

        return toolBarDict

    def showPreferencesWindow(self):
        self.preferencesWindow.show()

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

    def populateToolBar(self):
        settings = ConfigManager().getSettings("APP_STATE")
        toolbar = QToolBar(self)

        newFileAction = toolbar.addAction("New file")
        newFileAction.setIcon(QtGui.QIcon(":/new_file_icon.png"))
        newFileAction.setToolTip("")
        newFileAction.triggered.connect(self.parent.newFile)

        loadAction = toolbar.addAction("Load")
        loadAction.setIcon(QtGui.QIcon(":/folder_open_icon.png"))
        loadAction.setToolTip("")
        loadAction.triggered.connect(self.parent.load)

        self.parent.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)

        self.parent.toolBarDict[self.guid] = toolbar

        software = "standalone"

        try:
            extraPackagePaths = []
            extraPathsString = ConfigManager().getPrefsValue("PREFS", "General/ExtraPackageDirs")
            if extraPathsString is not None:
                extraPathsString = extraPathsString.rstrip(";")
                extraPathsRaw = extraPathsString.split(";")
                for rawPath in extraPathsRaw:
                    if os.path.exists(rawPath):
                        extraPackagePaths.append(os.path.normpath(rawPath))
            INITIALIZE(additionalPackageLocations=extraPackagePaths, software=software)
        except Exception as e:
            QMessageBox.critical(None, "Fatal error", str(e))
            return

        geo = settings.value('Editor/geometry')
        if geo is not None:
            self.restoreGeometry(geo)
        state = settings.value('Editor/state')
        if state is not None:
            self.parent.restoreState(state)

        settings.beginGroup("Tools")

        for packageName, registeredToolSet in GET_TOOLS().items():
            for ToolClass in registeredToolSet:
                if issubclass(ToolClass, ShelfTool):
                    ToolInstance = ToolClass()
                    # prevent to be garbage collected
                    self.registerToolInstance(ToolInstance)
                    ToolInstance.setAppInstance(self)
                    action = QAction(self)
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

                if issubclass(ToolClass, FormTool):
                    ToolInstance = ToolClass()
                    # prevent to be garbage collected
                    self.registerToolInstance(ToolInstance)
                    ToolInstance.setAppInstance(self.parent)
                    action = QAction(self)
                    action.setIcon(ToolInstance.getIcon())
                    action.setText(ToolInstance.name())
                    action.setToolTip(ToolInstance.toolTip())
                    action.setObjectName(ToolInstance.name())
                    action.triggered.connect(ToolInstance.do)

                    menus = self.parent.menuBar.findChildren(QMenu)
                    pluginsMenuAction = [m for m in menus if m.title() == "Tools"][0].menuAction()
                    toolsMenu = getOrCreateMenu(self.parent.menuBar, "Tools")
                    self.parent.menuBar.insertMenu(pluginsMenuAction, toolsMenu)
                    packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
                    toolsMenu.addMenu(packageSubMenu)
                    showToolAction = packageSubMenu.addAction(action)

                    settings.beginGroup("DockTools")
                    childGroups = settings.childGroups()
                    for dockToolGroupName in childGroups:
                        # This dock tool data been saved on last shutdown
                        settings.beginGroup(dockToolGroupName)
                        if dockToolGroupName in [t.uniqueName() for t in self._tools]:
                            settings.endGroup()
                            continue
                        toolName = dockToolGroupName.split("::")[0]
                        self.invokeDockToolByName(packageName, toolName, settings)
                        settings.endGroup()
                    settings.endGroup()

                if issubclass(ToolClass, DockTool):
                    menus = self.parent.menuBar.findChildren(QMenu)
                    pluginsMenuAction = [m for m in menus if m.title() == "Tools"][0].menuAction()
                    toolsMenu = getOrCreateMenu(self.parent.menuBar, "Tools")
                    self.parent.menuBar.insertMenu(pluginsMenuAction, toolsMenu)
                    packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
                    toolsMenu.addMenu(packageSubMenu)
                    showToolAction = packageSubMenu.addAction(ToolClass.name())
                    icon = ToolClass.getIcon()
                    if icon:
                        showToolAction.setIcon(icon)
                    showToolAction.triggered.connect(
                        lambda pkgName=packageName, toolName=ToolClass.name(): self.invokeDockToolByName(pkgName,
                                                                                                             toolName))
                    settings.beginGroup("DockTools")
                    childGroups = settings.childGroups()
                    for dockToolGroupName in childGroups:
                        # This dock tool data been saved on last shutdown
                        settings.beginGroup(dockToolGroupName)
                        if dockToolGroupName in [t.uniqueName() for t in self._tools]:
                            settings.endGroup()
                            continue
                        toolName = dockToolGroupName.split("::")[0]
                        self.invokeDockToolByName(packageName, toolName, settings)
                        settings.endGroup()
                    settings.endGroup()

        EditorHistory().saveState("New file")

        for name, package in GET_PACKAGES().items():
            prefsWidgets = package.PrefsWidgets()
            if prefsWidgets is not None:
                for categoryName, widgetClass in prefsWidgets.items():
                    PreferencesWindow().addCategory(categoryName, widgetClass())
                PreferencesWindow().selectByName("General")
        return toolbar
    def getToolBar(self):
        return self.toolBarDict

    def getCanvas(self):
        return self.canvasWidget.canvas

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        currentInputAction = InputAction(name="temp", actionType=InputActionType.Keyboard, key=event.key(), modifiers=modifiers)

        actionSaveVariants = InputManager()["App.Save"]
        actionNewFileVariants = InputManager()["App.NewFile"]
        actionLoadVariants = InputManager()["App.Load"]
        actionSaveAsVariants = InputManager()["App.SaveAs"]

        if currentInputAction in actionNewFileVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return

            EditorHistory().clear()
            historyTools = self.getRegisteredTools(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()
            self.newFile()
            EditorHistory().saveState("New file")
            self.currentFileName = None
            self.modified = False
            self.updateLabel()
        if currentInputAction in actionSaveVariants:
            self.save()
        if currentInputAction in actionLoadVariants:
            shouldSave = self.shouldSave()
            if shouldSave == QMessageBox.Yes:
                self.save()
            elif shouldSave == QMessageBox.Discard:
                return
            self.load()
        if currentInputAction in actionSaveAsVariants:
            self.save(True)

    def loadFromFileChecked(self, filePath):
        shouldSave = self.shouldSave()
        if shouldSave == QMessageBox.Yes:
            self.save()
        elif shouldSave == QMessageBox.Discard:
            return
        self.loadFromFile(filePath)
        self.modified = False
        self.updateLabel()


    def loadFromData(self, data, clearHistory=False):

        # check first if all packages we are trying to load are legal
        missedPackages = set()
        if not validateGraphDataPackages(data, missedPackages):
            msg = "This graph can not be loaded. Following packages not found:\n\n"
            index = 1
            for missedPackageName in missedPackages:
                msg += "{0}. {1}\n".format(index, missedPackageName)
                index += 1
            QMessageBox.critical(self, "Missing dependencies", msg)
            return

        if clearHistory:
            EditorHistory().clear()
            historyTools = self.getRegisteredTools(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()

        self.newFile(keepRoot=False)
        # load raw data
        self.graphManager.get().deserialize(data)
        self.fileBeenLoaded.emit()
        self.graphManager.get().selectGraphByName(data["activeGraph"])
        self.updateLabel()
        PathsRegistry().rebuild()

    @property
    def currentFileName(self):
        return self._currentFileName

    @currentFileName.setter
    def currentFileName(self, value):
        self._currentFileName = value
        self.updateLabel()

    def createPopupMenu(self):
        pass

    def getToolClassByName(self, packageName, toolName, toolClass=DockTool):
        registeredTools = GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            if issubclass(ToolClass, toolClass):
                pass
            if ToolClass.name() == toolName:
                return ToolClass
        return None

    def createToolInstanceByClass(self, packageName, toolName, toolClass=DockTool):
        registeredTools = GET_TOOLS()
        for ToolClass in registeredTools[packageName]:
            supportedSoftwares = ToolClass.supportedSoftwares()
            if "any" not in supportedSoftwares:
                if self.currentSoftware not in supportedSoftwares:
                    continue

            if issubclass(ToolClass, toolClass):
                pass

            if ToolClass.name() == toolName:
                return ToolClass()
        return None

    def getRegisteredTools(self, classNameFilters=[]):
        if len(classNameFilters) == 0:
            return self._tools
        else:
            result = []
            for tool in self._tools:
                if tool.__class__.__name__ in classNameFilters:
                    result.append(tool)
            return result

    def invokeFormByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name, FormTool)
        if toolClass is None:
            return
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        tool.show()
                        tool.onShow()
                        # Highlight window
                        print("highlight", tool.uniqueName())
                return
        ToolInstance = self.createToolInstanceByClass(packageName, name, FormTool)
        if ToolInstance:
            self.registerToolInstance(ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.parent.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            ToolInstance.setAppInstance(self.parent)
            ToolInstance.onShow()
        return ToolInstance

    def invokeDockToolByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name, DockTool)
        if toolClass is None:
            return
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        tool.show()
                        tool.onShow()
                        # Highlight window
                        print("highlight", tool.uniqueName())
                return
        ToolInstance = self.createToolInstanceByClass(packageName, name, DockTool)
        if ToolInstance:
            self.registerToolInstance(ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.parent.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            else:
                self.parent.addDockWidget(ToolInstance.defaultDockArea(), ToolInstance)
            ToolInstance.setAppInstance(self)
            ToolInstance.onShow()
        return ToolInstance

    def newFile(self):
        self.isUntitled = True
        self.curFile = f"document{pyflowChild.sequenceNumber}.pygraph"
        self._currentFileName = f"document{pyflowChild.sequenceNumber}.pygraph"
        pyflowChild.sequenceNumber += 1
        self.setWindowTitle(self.curFile + '[*]')

        #self.document().contentsChanged.connect(self.documentWasModified)

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return False

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)

        #self.contentsChanged.connect(self.documentWasModified)

        return True

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save As", self.curFile)
        if not fileName:
            return False

        return self.saveFile(fileName)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        return True

    def userFriendlyCurrentFile(self):
        return self.strippedName(self.curFile)

    def currentFile(self):
        return self.curFile

    def closeEvent(self, event):
        if self.maybeSave():
            event.accept()
        else:
            event.ignore()

        self.parent.toolBarDict[self.guid].setVisible(False)
        del self.parent.toolBarDict[self.guid]


    def documentWasModified(self):
        self.setWindowModified(self.isModified)

    def maybeSave(self):
        if self.isModified:
            ret = QMessageBox.warning(self, "MDI",
                    "'%s' has been modified.\nDo you want to save your "
                    "changes?" % self.userFriendlyCurrentFile(),
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        #self.document().setModified(False)
        self.setWindowModified(False)
        self.setWindowTitle(self.userFriendlyCurrentFile() + "[*]")

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()

    def onRequestFillProperties(self, propertiesFillDelegate):
        for toolInstance in self._tools:
            if isinstance(toolInstance, PropertiesTool):
                toolInstance.clear()
                toolInstance.assignPropertiesWidget(propertiesFillDelegate)

    def onRequestClearProperties(self):
        for toolInstance in self._tools:
            if isinstance(toolInstance, PropertiesTool):
                toolInstance.clear()

    def startMainLoop(self):
        self.tick_timer.timeout.connect(self.mainLoop)
        self.tick_timer.start(1000 / EDITOR_TARGET_FPS)
        QCoreApplication.processEvents()

    def stopMainLoop(self):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()

    def mainLoop(self):
        deltaTime = process_time() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)

        # Tick all graphs
        # each graph will tick owning raw nodes
        # each raw node will tick its ui wrapper if it exists
        self.graphManager.get().Tick(deltaTime)

        # Tick canvas. Update ui only stuff such animation etc.
        self.canvasWidget.Tick(deltaTime)

        self._lastClock = process_time()

class MDIMain(QMainWindow):
    appInstance = None
    def __init__(self, parent=None):
        super(MDIMain, self).__init__(parent=parent)

        self.mdiArea = QMdiArea()

        '''self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)'''
        self.setCentralWidget(self.mdiArea)
        self.mdiArea.subWindowActivated.connect(self.updateMenus)
        self.windowMapper = QSignalMapper(self)
        self.guid = uuid.uuid4()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.currentSoftware = ""
        self.undoStack = QUndoStack(self)
        self.setContentsMargins(1, 1, 1, 1)
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QTabWidget.North)
        self.setDockOptions(QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks)
        self.menuBar = QMenuBar(None) #self
        self.menuBar.setGeometry(QRect(0, 0, 863, 21))
        self.menuBar.setObjectName("menuBar")
        self.setMenuBar(self.menuBar)
        self.windowMapper = QSignalMapper(self)
        self._tools = set()
        self.setWindowTitle(winTitle())
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setWindowIcon(QtGui.QIcon(":/LogoBpApp.png"))
        self.undoStack = QUndoStack(self)
        self.setMouseTracking(True)

        self.toolBarDict = {}
        self.populateToolBar()
        self.refreshToolBar(self)
        self.createStatusBar()
        #self.updateMenus()
        self.populateMenu()

        self.preferencesWindow = PreferencesWindow(self)

        self.createActions()

    def populateMenu(self):
        fileMenu = self.menuBar.addMenu("&File")
        newFileAction = fileMenu.addAction("New file")
        newFileAction.setIcon(QtGui.QIcon(":/new_file_icon.png"))
        newFileAction.triggered.connect(self.newFile)

        loadAction = fileMenu.addAction("Load")
        loadAction.setIcon(QtGui.QIcon(":/folder_open_icon.png"))
        loadAction.triggered.connect(self.load)

        saveAction = fileMenu.addAction("Save")
        saveAction.setIcon(QtGui.QIcon(":/save_icon.png"))
        saveAction.triggered.connect(self.save)

        saveAsAction = fileMenu.addAction("Save as")
        saveAsAction.setIcon(QtGui.QIcon(":/save_as_icon.png"))
        saveAsAction.triggered.connect(lambda: self.save(True))

        IOMenu = fileMenu.addMenu("Custom IO")
        for packageName, package in GET_PACKAGES().items():
            # exporters
            exporters = None
            try:
                exporters = package.GetExporters()
            except:
                continue
            pkgMenu = IOMenu.addMenu(packageName)
            for exporterName, exporterClass in exporters.items():
                fileFormatMenu = pkgMenu.addMenu(exporterClass.displayName())
                fileFormatMenu.setToolTip(exporterClass.toolTip())
                if exporterClass.createExporterMenu():
                    exportAction = fileFormatMenu.addAction("Export")
                    exportAction.triggered.connect(lambda checked=False, app=self, exporter=exporterClass: exporter.doExport(app))
                if exporterClass.createImporterMenu():
                    importAction = fileFormatMenu.addAction("Import")
                    importAction.triggered.connect(lambda checked=False, app=self, exporter=exporterClass: exporter.doImport(app))

        editMenu = self.menuBar.addMenu("Edit")
        preferencesAction = editMenu.addAction("Preferences")
        preferencesAction.setIcon(QtGui.QIcon(":/options_icon.png"))
        preferencesAction.triggered.connect(self.showPreferencesWindow)

        pluginsMenu = self.menuBar.addMenu("Tools")
        packagePlugin = pluginsMenu.addAction("Create package...")
        packagePlugin.triggered.connect(self.createPackagebBuilder)

        self.windowMenu = self.menuBar.addMenu("&Window")
        self.updateWindowMenu
        self.windowMenu.aboutToShow.connect(self.updateWindowMenu)

        helpMenu = self.menuBar.addMenu("Help")
        helpMenu.addAction("Homepage").triggered.connect(lambda _=False, url="https://wonderworks-software.github.io/PyFlow/": QtGui.QDesktopServices.openUrl(url))
        helpMenu.addAction("Docs").triggered.connect(lambda _=False, url="https://pyflow.readthedocs.io/en/latest/": QtGui.QDesktopServices.openUrl(url))

    def populateToolBar(self):
        settings = ConfigManager().getSettings("APP_STATE")
        toolbar = QToolBar(self)

        newFileAction = toolbar.addAction("New file")
        newFileAction.setIcon(QtGui.QIcon(":/new_file_icon.png"))
        newFileAction.setToolTip("")
        newFileAction.triggered.connect(self.newFile)

        loadAction = toolbar.addAction("Load")
        loadAction.setIcon(QtGui.QIcon(":/folder_open_icon.png"))
        loadAction.setToolTip("")
        loadAction.triggered.connect(self.load)

        self.addToolBar(QtCore.Qt.TopToolBarArea, toolbar)

        self.toolBarDict[self.guid] = toolbar

        geo = settings.value('Editor/geometry')
        if geo is not None:
            self.restoreGeometry(geo)
        state = settings.value('Editor/state')
        if state is not None:
            self.restoreState(state)
        settings.beginGroup("Tools")

        for packageName, registeredToolSet in GET_TOOLS().items():
            for ToolClass in registeredToolSet:
                if issubclass(ToolClass, ShelfTool) or issubclass(ToolClass, FormTool):
                    ToolInstance = ToolClass()
                    # prevent to be garbage collected
                    self.registerToolInstance(ToolInstance)
                    ToolInstance.setAppInstance(self)
                    action = QAction(self)
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
                    menus = self.menuBar.findChildren(QMenu)
                    pluginsMenuAction = [m for m in menus if m.title() == "Tools"][0].menuAction()
                    toolsMenu = getOrCreateMenu(self.menuBar, "Tools")
                    self.menuBar.insertMenu(pluginsMenuAction, toolsMenu)
                    packageSubMenu = getOrCreateMenu(toolsMenu, packageName)
                    toolsMenu.addMenu(packageSubMenu)
                    showToolAction = packageSubMenu.addAction(ToolClass.name())
                    icon = ToolClass.getIcon()
                    if icon:
                        showToolAction.setIcon(icon)
                    showToolAction.triggered.connect(
                        lambda pkgName=packageName, toolName=ToolClass.name(): self.invokeDockToolByName(pkgName,
                                                                                                             toolName))

                    settings.beginGroup("DockTools")
                    childGroups = settings.childGroups()
                    for dockToolGroupName in childGroups:
                        # This dock tool data been saved on last shutdown
                        settings.beginGroup(dockToolGroupName)
                        if dockToolGroupName in [t.uniqueName() for t in self._tools]:
                            settings.endGroup()
                            continue
                        toolName = dockToolGroupName.split("::")[0]
                        self.invokeDockToolByName(packageName, toolName, settings)
                        settings.endGroup()
                    settings.endGroup()

            EditorHistory(self).saveState("New file")

            for name, package in GET_PACKAGES().items():
                prefsWidgets = package.PrefsWidgets()
                if prefsWidgets is not None:
                    for categoryName, widgetClass in prefsWidgets.items():
                        PreferencesWindow().addCategory(categoryName, widgetClass())
                    PreferencesWindow().selectByName("General")
            return toolbar
    def getToolBar(self):
        return self.toolBarDict

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
            supportedSoftwares = ToolClass.supportedSoftwares()
            if "any" not in supportedSoftwares:
                if self.currentSoftware not in supportedSoftwares:
                    continue

            if issubclass(ToolClass, toolClass):
                if ToolClass.name() == toolName:
                    return ToolClass()
        return None

    def invokeDockToolByName(self, packageName, name, settings=None):
        # invokeDockToolByName Invokes dock tool by tool name and package name
        # If settings provided QMainWindow::restoreDockWidget will be called instead QMainWindow::addDockWidget
        toolClass = self.getToolClassByName(packageName, name, DockTool)
        if toolClass is None:
            return
        isSingleton = toolClass.isSingleton()
        if isSingleton:
            # check if already registered
            if name in [t.name() for t in self._tools]:
                for tool in self._tools:
                    if tool.name() == name:
                        tool.show()
                        tool.onShow()
                        # Highlight window
                        print("highlight", tool.uniqueName())
                return
        ToolInstance = self.createToolInstanceByClass(packageName, name, DockTool)
        if ToolInstance:
            self.registerToolInstance(ToolInstance)
            if settings is not None:
                ToolInstance.restoreState(settings)
                if not self.parent.restoreDockWidget(ToolInstance):
                    # handle if ui state was not restored
                    pass
            else:
                self.parent.addDockWidget(ToolInstance.defaultDockArea(), ToolInstance)
            ToolInstance.setAppInstance(self)
            ToolInstance.onShow()
        return ToolInstance

    def loadFromFile(self, filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)
            self.loadFromData(data, clearHistory=True)
            self.currentFileName = filePath
            EditorHistory().saveState("Open {}".format(os.path.basename(self.currentFileName)))


    def loadFromData(self, data, clearHistory=False):

        # check first if all packages we are trying to load are legal
        missedPackages = set()
        if not validateGraphDataPackages(data, missedPackages):
            msg = "This graph can not be loaded. Following packages not found:\n\n"
            index = 1
            for missedPackageName in missedPackages:
                msg += "{0}. {1}\n".format(index, missedPackageName)
                index += 1
            QMessageBox.critical(self, "Missing dependencies", msg)
            return

        if clearHistory:
            EditorHistory().clear()
            historyTools = self.getRegisteredTools(classNameFilters=["HistoryTool"])
            for historyTools in historyTools:
                historyTools.onClear()

        self.newFile(keepRoot=False)
        # load raw data
        self.graphManager.get().deserialize(data)
        self.fileBeenLoaded.emit()
        self.graphManager.get().selectGraphByName(data["activeGraph"])
        self.updateLabel()
        PathsRegistry().rebuild()


    def load(self):
        name_filter = "Graph files (*.pygraph)"
        savepath = QFileDialog.getOpenFileName(filter=name_filter)
        if type(savepath) in [tuple, list]:
            fpath = savepath[0]
        else:
            fpath = savepath
        if not fpath == '':
            self.loadFromFile(fpath)

    def closeEvent(self, event):
        self.mdiArea.closeAllSubWindows()
        if self.mdiArea.currentSubWindow():
            event.ignore()
        else:
            self.writeSettings()
            event.accept()

    def newFile(self):
        child = self.createMdiChild()
        child.newFile()
        child.show()

        #toolbar = self.populateToolBar()
        self.hidealltool(child.guid)
        # self.instanceDict[child.guid] = child.instance
        # self.toolBarDict[child.guid] = toolbar
        # self.addToolBar(Qt.TopToolBarArea, toolbar)

    def hidealltool(self, VisibleToolBar=None):
        if VisibleToolBar is None:
            VisibleToolBar = self.guid

        for toolbar in self.toolBarDict:
            if toolbar != VisibleToolBar:
                self.toolBarDict[toolbar].setVisible(False)
            else:
                self.toolBarDict[toolbar].setVisible(True)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            existing = self.findMdiChild(fileName)
            if existing:
                self.mdiArea.setActiveSubWindow(existing)
                return

            child = self.createMdiChild()
            if child.loadFile(fileName):
                self.statusBar().showMessage("File loaded", 2000)
                child.show()
            else:
                child.close()

    def save(self):
        if self.activeMdiChild() and self.activeMdiChild().save():
            self.statusBar().showMessage("File saved", 2000)

    def saveAs(self):
        if self.activeMdiChild() and self.activeMdiChild().saveAs():
            self.statusBar().showMessage("File saved", 2000)

    def cut(self):
        if self.activeMdiChild():
            self.activeMdiChild().cut()

    def copy(self):
        if self.activeMdiChild():
            self.activeMdiChild().copy()

    def paste(self):
        if self.activeMdiChild():
            self.activeMdiChild().paste()

    def about(self):
        QMessageBox.about(self, "About MDI",
                          "The <b>MDI</b> example demonstrates how to write multiple "
                          "document interface applications using Qt.")

    def updateMenus(self):
        hasMdiChild = (self.activeMdiChild() is not None)
        self.saveAct.setEnabled(hasMdiChild)
        self.saveAsAct.setEnabled(hasMdiChild)
        self.pasteAct.setEnabled(hasMdiChild)
        self.closeAct.setEnabled(hasMdiChild)
        self.closeAllAct.setEnabled(hasMdiChild)
        self.tileAct.setEnabled(hasMdiChild)
        self.cascadeAct.setEnabled(hasMdiChild)
        self.nextAct.setEnabled(hasMdiChild)
        self.previousAct.setEnabled(hasMdiChild)
        self.separatorAct.setVisible(hasMdiChild)

        '''hasSelection = (self.activeMdiChild() is not None and
                        self.activeMdiChild().textCursor().hasSelection())
        self.cutAct.setEnabled(hasSelection)
        self.copyAct.setEnabled(hasSelection)'''

    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.windowMenu.addAction(self.closeAct)
        self.windowMenu.addAction(self.closeAllAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.tileAct)
        self.windowMenu.addAction(self.cascadeAct)
        self.windowMenu.addSeparator()
        self.windowMenu.addAction(self.nextAct)
        self.windowMenu.addAction(self.previousAct)
        self.windowMenu.addAction(self.separatorAct)

        windows = self.mdiArea.subWindowList()
        self.separatorAct.setVisible(len(windows) != 0)

        for i, window in enumerate(windows):
            child = window.widget()

            text = "%d %s" % (i + 1, window.userFriendlyCurrentFile())
            if i < 9:
                text = '&' + text

            action = self.windowMenu.addAction(text)
            action.setCheckable(True)
            action.setChecked(child is self.activeMdiChild())
            action.triggered.connect(self.windowMapper.map)
            self.windowMapper.setMapping(action, window)


    def createMdiChild(self):
        #instance = self.instance(software="standalone")
        child = pyflowChild(self)
        self.mdiArea.addSubWindow(child)
        self.mdiArea.setBaseSize(200, 200)
        '''child.copyAvailable.connect(self.cutAct.setEnabled)
        child.copyAvailable.connect(self.copyAct.setEnabled)'''
        return child

    def createPackagebBuilder(self):
        self.newFileFromUi(PackageBuilder.PackageBuilder(self))

    def newFileFromUi(self, MDIClass):
        child = MDIClass.ui
        MDIClass.uuid = uuid.uuid4()
        self.mdiArea.addSubWindow(child)
        child.show()

    def createActions(self):
        self.newAct = QAction(QIcon(':/images/new.png'), "&New", self,
                              shortcut=QKeySequence.New, statusTip="Create a new file",
                              triggered=self.newFile)

        self.openAct = QAction(QIcon(':/images/open.png'), "&Open...", self,
                               shortcut=QKeySequence.Open, statusTip="Open an existing file",
                               triggered=self.open)

        self.saveAct = QAction(QIcon(':/images/save.png'), "&Save", self,
                               shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
                                 shortcut=QKeySequence.SaveAs,
                                 statusTip="Save the document under a new name",
                                 triggered=self.saveAs)

        self.exitAct = QAction("E&xit", self, shortcut=QKeySequence.Quit,
                               statusTip="Exit the application",
                               triggered=QApplication.instance().closeAllWindows)

        self.cutAct = QAction(QIcon(':/images/cut.png'), "Cu&t", self,
                              shortcut=QKeySequence.Cut,
                              statusTip="Cut the current selection's contents to the clipboard",
                              triggered=self.cut)

        self.copyAct = QAction(QIcon(':/images/copy.png'), "&Copy", self,
                               shortcut=QKeySequence.Copy,
                               statusTip="Copy the current selection's contents to the clipboard",
                               triggered=self.copy)

        self.pasteAct = QAction(QIcon(':/images/paste.png'), "&Paste", self,
                                shortcut=QKeySequence.Paste,
                                statusTip="Paste the clipboard's contents into the current selection",
                                triggered=self.paste)

        self.closeAct = QAction("Cl&ose", self,
                                statusTip="Close the active window",
                                triggered=self.mdiArea.closeActiveSubWindow)

        self.closeAllAct = QAction("Close &All", self,
                                   statusTip="Close all the windows",
                                   triggered=self.mdiArea.closeAllSubWindows)

        self.tileAct = QAction("&Tile", self, statusTip="Tile the windows",
                               triggered=self.mdiArea.tileSubWindows)

        self.cascadeAct = QAction("&Cascade", self,
                                  statusTip="Cascade the windows",
                                  triggered=self.mdiArea.cascadeSubWindows)

        self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
                               statusTip="Move the focus to the next window",
                               triggered=self.mdiArea.activateNextSubWindow)

        self.previousAct = QAction("Pre&vious", self,
                                   shortcut=QKeySequence.PreviousChild,
                                   statusTip="Move the focus to the previous window",
                                   triggered=self.mdiArea.activatePreviousSubWindow)

        self.separatorAct = QAction(self)
        self.separatorAct.setSeparator(True)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = QSettings('Trolltech', 'MDI Example')
        pos = settings.value('pos', QPoint(200, 200))
        size = settings.value('size', QSize(400, 400))
        self.move(pos)
        self.resize(size)

    def writeSettings(self):
        settings = QtCore.QSettings('Trolltech', 'MDI Example')
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def activeMdiChild(self):
        activeSubWindow = self.mdiArea.activeSubWindow()

        if activeSubWindow:
            try:
                guid = activeSubWindow.widget().guid
                self.hidealltool(guid)
                return activeSubWindow.widget()
            except:
                pass
        return None

    def findMdiChild(self, fileName):
        canonicalFilePath = QFileInfo(fileName).canonicalFilePath()

        for window in self.mdiArea.subWindowList():
            if window.widget().currentFile() == canonicalFilePath:
                return window
        return None

    def switchLayoutDirection(self):
        if self.layoutDirection() == Qt.LeftToRight:
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)

    def setActiveSubWindow(self, window):
        if window:
            self.mdiArea.setActiveSubWindow(window)

    def refreshToolBar(self, instance):

        if instance is None: #The Package is selected but a file has not be loaded/started

            package = "Root"
            toolDict = self.getToolBarLayout()
            toolOrder = ["Packages", "Tools"]

        else: #There is an active instance
            package = "PyFlow"
            #toolDict = instance.getToolBarLayout()

    def getToolBarLayout(self):

        toolBarDict = {}
        pyFlowToolBar = []
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "NewFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "NewFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "OpenFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "SaveFile",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "AlignLeft",
                              "Active": True})
        pyFlowToolBar.append({"Bar": "Bar 1", "Section": "Section 1", "Widget": "Small Button", "Action": "Add Action",
                              "Package": "PyFlow", "PackageGroup": "PyFlow", "Instance": self, "Command": "AlignRight",
                              "Active": True})

        toolBarDict["File"] = pyFlowToolBar

        return toolBarDict

    def updateToolBar(self, tBar, tDict):
        if tDict["Action"] == "Add Action":
            toolAction = self.actionRegisterDict[tDict["Package"]].getAction(tDict["PackageGroup"], tDict["Command"])
            try:
                toolAction.setInstance(tDict["Instance"])
                tBar.addAction(toolAction)
            except:
                pass
        if tDict["Action"] == "Add Separator":
            pass
            '''menuAction.setSeparator(True)
            mBar.addAction(menuAction)'''
        if tDict["Action"] == "Add Children":
            pass

    def showPreferencesWindow(self):
        self.preferencesWindow.show()

    def instance(self, parent=None, software=""):
        assert(software != ""), "Invalid arguments. Please pass you software name as second argument!"
        settings = ConfigManager().getSettings("APP_STATE")

        instance = pyflowChild(self)
        instance.currentSoftware = software
        SessionDescriptor().software = instance.currentSoftware
        return instance

    def unregisterToolInstance(self, instance):
        if instance in self._tools:
            self._tools.remove(instance)

    def registerToolInstance(self, instance):
        """Registers tool instance reference

        This needed to prevent classes from being garbage collected and to save widgets state

        Args:

            instance (ToolBase): Tool to be registered
        """
        self._tools.add(instance)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MDIMain()
    mainWin.show()
    sys.exit(app.exec_())
