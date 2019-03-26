import os
import sys
import subprocess
import json
from time import clock
import pkgutil

from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QStyleFactory
from Qt.QtWidgets import QSizePolicy
from Qt.QtWidgets import QTextEdit
from Qt.QtWidgets import QMessageBox
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QUndoView
from Qt.QtWidgets import QToolButton
from Qt.QtWidgets import QPushButton
from Qt.QtWidgets import QSpacerItem

from PyFlow import Packages
from PyFlow.UI.Graph.Widget import GraphWidgetUI
from PyFlow.Core.Common import Direction
from PyFlow.Core.Common import clearLayout
from PyFlow.Core.GraphTree import GraphTree
from PyFlow.Core.AppBase import AppBase
from PyFlow.Core.GraphBase import GraphBase
from PyFlow.UI.Views.InspectorWidget import InspectorWidget
from PyFlow.UI.Views.NodeBox import NodesBox
from PyFlow.UI.Views import GraphEditor_ui
from PyFlow.UI.Views.VariablesWidget import VariablesWidget
from PyFlow.UI.Utils.StyleSheetEditor import StyleSheetEditor
from PyFlow import INITIALIZE


FILE_DIR = os.path.abspath(os.path.dirname(__file__))
SETTINGS_PATH = os.path.join(FILE_DIR, "appConfig.ini")
STYLE_PATH = os.path.join(FILE_DIR, "style.css")
EDITOR_TARGET_FPS = 60


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


## App itself
class PyFlow(QMainWindow, GraphEditor_ui.Ui_MainWindow, AppBase):
    def __init__(self, parent=None):
        super(PyFlow, self).__init__(parent=parent)
        AppBase.__init__(self)
        self.setupUi(self)
        self.listViewUndoStack = QUndoView(self.dockWidgetContents_3)
        self.listViewUndoStack.setObjectName("listViewUndoStack")
        self.gridLayout_6.addWidget(self.listViewUndoStack, 0, 0, 1, 1)

	self.styleSheetEditor = StyleSheetEditor()
        self._currentGraph = GraphWidgetUI(self, graphBase=GraphTree().getRootGraph())
        self.updateGraphTreeLocation()
        GraphTree().onGraphSwitched.connect(self.onRawGraphSwitched)
        self.SceneLayout.addWidget(self._currentGraph)

        self.actionVariables.triggered.connect(self.toggleVariables)
        self.actionPlot_graph.triggered.connect(self._currentGraph.plot)
        self.actionDelete.triggered.connect(self.on_delete)
        self.actionPropertyView.triggered.connect(self.togglePropertyView)
        self.actionScreenshot.triggered.connect(self._currentGraph.screenShot)
        self.actionShortcuts.triggered.connect(self.shortcuts_info)
        self.actionSave.triggered.connect(self._currentGraph.save)
        self.actionLoad.triggered.connect(self._currentGraph.load)
        self.actionSave_as.triggered.connect(self._currentGraph.save_as)
        self.actionAlignLeft.triggered.connect(lambda: self.currentGraph.alignSelectedNodes(Direction.Left))
        self.actionAlignUp.triggered.connect(lambda: self.currentGraph.alignSelectedNodes(Direction.Up))
        self.actionAlignBottom.triggered.connect(lambda: self.currentGraph.alignSelectedNodes(Direction.Down))
        self.actionAlignRight.triggered.connect(lambda: self.currentGraph.alignSelectedNodes(Direction.Right))
        self.actionNew_Node.triggered.connect(lambda: self.newPlugin(PluginType.pNode))
        self.actionNew_Command.triggered.connect(lambda: self.newPlugin(PluginType.pCommand))
        self.actionFunction_Library.triggered.connect(lambda: self.newPlugin(PluginType.pFunctionLibrary))
        self.actionNew_pin.triggered.connect(lambda: self.newPlugin(PluginType.pPin))
        self.actionHistory.triggered.connect(self.toggleHistory)
        self.actionNew.triggered.connect(self._currentGraph.new_file)
        self.dockWidgetUndoStack.setVisible(False)

        self.setMouseTracking(True)

        self.variablesWidget = VariablesWidget(self, self._currentGraph)
        self.leftDockGridLayout.addWidget(self.variablesWidget)

        self._lastClock = 0.0
        self.fps = EDITOR_TARGET_FPS
        self.tick_timer = QtCore.QTimer()
        self.tick_timer.timeout.connect(self.mainLoop)

    def onRawGraphSwitched(self, *args, **kwargs):
        old = kwargs['old']
        new = kwargs['new']
        # TODO: hide current graph contents
        for node in old.nodes.values():
            uiNode = node.getWrapper()()
            uiNode.hide()
        # TODO: show new graph contents
        for node in new.nodes.values():
            uiNode = node.getWrapper()()
            uiNode.show()
        self.updateGraphTreeLocation()

    def updateGraphTreeLocation(self):
        location = GraphTree().location()
        clearLayout(self.layoutGraphPath)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layoutGraphPath.addItem(spacerItem)
        for folderName in location.split('|'):
            index = self.layoutGraphPath.count() - 1
            btn = QPushButton(folderName)

            def onClicked(checked, name=None):
                if GraphTree().switchGraph(name):
                    print('goto', name)
                else:
                    print('skip')
            btn.clicked.connect(lambda chk=False, name=folderName: onClicked(chk, name))
            self.layoutGraphPath.insertWidget(index, btn)

    @property
    def currentGraph(self):
        return self._currentGraph

    @currentGraph.setter
    def currentGraph(self, graph):
        self._currentGraph = graph

    def startMainLoop(self):
        self.tick_timer.start(1000 / EDITOR_TARGET_FPS)

    def mainLoop(self):
        deltaTime = clock() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)

        # Tick UI graph
        self.currentGraph.Tick(deltaTime)

        # Tick all graphs
        # each graph will tick owning raw nodes
        # each raw node will tick it's ui wrapper if it exists
        AppBase.Tick(self, deltaTime)

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

    def closeEvent(self, event):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()
        self._currentGraph.shoutDown()
        # save editor config
        settings = QtCore.QSettings(
            SETTINGS_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup('Editor')
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.endGroup()
        QMainWindow.closeEvent(self, event)

    def applySettings(self, settings):
        self.restoreGeometry(settings.value('Editor/geometry'))
        self.restoreState(settings.value('Editor/windowState'))

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

    def on_delete(self):
        self.currentGraph.killSelectedNodes()

    @staticmethod
    def instance(parent=None):
        settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)
        instance = PyFlow(parent)
        instance.applySettings(settings)
        instance.startMainLoop()
        INITIALIZE()

        # fetch input widgets
        # do it separately from raw classes, since this is ui related code
        for importer, modname, ispkg in pkgutil.iter_modules(Packages.__path__):
            if ispkg:
                mod = importer.find_module(modname).load_module(modname)
                FactoriesPath = mod.__path__[0]
                FactoriesImporter = pkgutil.get_importer(FactoriesPath)
                FactoriesModuleLoader = FactoriesImporter.find_module(
                    'Factories')
                if FactoriesModuleLoader is not None:
                    FactoriesModule = FactoriesModuleLoader.load_module(
                        'Factories')
        return instance
