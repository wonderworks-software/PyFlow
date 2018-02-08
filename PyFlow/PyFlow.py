from os import listdir, path, startfile
import sys
from Qt import QtGui
from Qt import QtCore
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QStyleFactory
from Qt.QtWidgets import QTextEdit
from Qt.QtWidgets import QMessageBox
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QUndoView
from Core.Widget import GraphWidget
from Core.Widget import Direction
from Core.Widget import NodesBox
from Core.VariablesWidget import VariablesWidget
from Core.AGraphCommon import CircularBuffer
import Nodes
import Commands
import FunctionLibraries
import Pins
import GraphEditor_ui
import json
from time import clock
from numpy import mean


FILE_DIR = path.dirname(__file__)
SETTINGS_PATH = FILE_DIR + "/appConfig.ini"
EDITOR_TARGET_FPS = 60


class PluginType:
    pNode = 0
    pCommand = 1
    pFunctionLibrary = 2
    pPin = 3


def _implementPlugin(name, pluginType):
    CommandTemplate = """from Qt.QtWidgets import QUndoCommand


class {0}(QUndoCommand):

    def __init__(self):
        super({0}, self).__init__()

    def undo(self):
        pass

    def redo(self):
        pass
""".format(name)

    NodeTemplate = """from AbstractGraph import *
from Settings import *
from Core import Node


class {0}(Node):
    def __init__(self, name, graph):
        super({0}, self).__init__(name, graph)
        self.inp0 = self.addInputPin('in0', DataTypes.Bool)
        self.out0 = self.addOutputPin('out0', DataTypes.Bool)
        pinAffects(self.inp0, self.out0)

    @staticmethod
    def pinTypeHints():
        '''
            used by nodebox to suggest supported pins
            when drop wire from pin into empty space
        '''
        return {{'inputs': [DataTypes.Bool], 'outputs': [DataTypes.Bool]}}

    @staticmethod
    def category():
        '''
            used by nodebox to place in tree
            to make nested one - use '|' like this ( 'CatName|SubCatName' )
        '''
        return 'Common'

    @staticmethod
    def keywords():
        '''
            used by nodebox filter while typing
        '''
        return []

    @staticmethod
    def description():
        '''
            used by property view and node box widgets
        '''
        return 'default description'

    def compute(self):
        '''
            1) get data from inputs
            2) do stuff
            3) put data to outputs
            4) call output execs
        '''

        str_data = self.inp0.getData()
        try:
            self.out0.setData(str_data.upper())
        except Exception as e:
            print(e)
""".format(name)

    LibraryTemplate = """from Core.FunctionLibrary import *
# import types stuff
from AGraphCommon import *
# import stuff you need
# ...


class {0}(FunctionLibraryBase):
    '''doc string for {0}'''
    def __init__(self):
        super({0}, self).__init__()

    @staticmethod
    @implementNode(returns=(DataTypes.Int, 0), meta={{'Category': 'CategoryName|SubCategory name', 'Keywords': ['+', 'append', 'sum']}})
    def add(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0)):
        '''Sum of two ints.'''
        return A + B

    @staticmethod
    @implementNode(returns=(DataTypes.Float, 0.0), meta={{'Category': 'CategoryName', 'Keywords': ['/']}})
    def divide(A=(DataTypes.Int, 0), B=(DataTypes.Int, 0), result=(DataTypes.Reference, (DataTypes.Bool, False))):
        '''Integer devision.'''
        try:
            d = A / B
            result.setData(True)
            return d
        except:
            result.setData(False)
            return -1

""".format(name)

    PinTemplate = """from Core.Pin import _Pin
from Core.AGraphCommon import *


class {0}(_Pin):
    '''doc string for {0}'''
    def __init__(self, name, parent, dataType, direction, **kwargs):
        super({0}, self).__init__(name, parent, dataType, direction, **kwargs)
        self.setDefaultValue(False)

    def supportedDataTypes(self):
        return (DataTypes.Bool,)

    @staticmethod
    def color():
        return Colors.Bool

    @staticmethod
    def pinDataTypeHint():
        return DataTypes.Bool, False

    def setData(self, data):
        try:
            self._data = bool(data)
        except:
            self._data = self.defaultValue()
        _Pin.setData(self, self._data)
""".format(name)

    if pluginType == PluginType.pNode:
        file_path = "{0}/{1}.py".format(Nodes.__path__[0], name)
        existing_nodes = [n.split(".")[0] for n in listdir(Nodes.__path__[0]) if n.endswith(".py") and "__init__" not in n]

        if name in existing_nodes:
            print("[ERROR] Node {0} already exists! Chose another name".format(name))
            return

        # write to file. delete older if needed
        with open(file_path, "wb") as f:
            f.write(NodeTemplate)
        print("[INFO] Node {0} been created.\nIn order to appear in node box, restart application.".format(name))
        startfile(file_path)

    if pluginType == PluginType.pCommand:
        file_path = "{0}/{1}.py".format(Commands.__path__[0], name)
        existing_commands = [c.split(".")[0] for c in listdir(Commands.__path__[0]) if c.endswith(".py") and "__init__" not in c]
        if name in existing_commands:
            print("[ERROR] Command {0} already exists! Chose another name".format(name))
            return
        # write to file. delete older if needed
        with open(file_path, "wb") as f:
            f.write(CommandTemplate)
        print("[INFO] Command {0} been created.\n Restart application.".format(name))
        startfile(file_path)

    if pluginType == PluginType.pFunctionLibrary:
        filePath = "{0}/{1}.py".format(FunctionLibraries.__path__[0], name)
        existingLibs = [c.split(".")[0] for c in listdir(FunctionLibraries.__path__[0]) if c.endswith(".py") and "__init__" not in c]
        if name in existingLibs:
            print("[ERROR] Function library {0} already exists! Chose another name".format(name))
            return
        # write to file. delete older if needed
        with open(filePath, "wb") as f:
            f.write(LibraryTemplate)
        print("[INFO] Function lib {0} been created.\n Restart application.".format(name))
        startfile(filePath)

    if pluginType == PluginType.pPin:
        filePath = "{0}/{1}.py".format(Pins.__path__[0], name)
        existingPins = [c.split(".")[0] for c in listdir(Pins.__path__[0]) if c.endswith(".py") and "__init__" not in c]
        if name in existingPins:
            print("[ERROR] Pin {0} already exists! Chose another name".format(name))
            return
        # write to file. delete older if needed
        with open(filePath, "wb") as f:
            f.write(PinTemplate)
        print("[INFO] Pin {0} been created.\n Restart application.".format(name))
        startfile(filePath)


class PyFlow(QMainWindow, GraphEditor_ui.Ui_MainWindow):
    def __init__(self):
        super(PyFlow, self).__init__()
        self.setupUi(self)
        self.listViewUndoStack = QUndoView(self.dockWidgetContents_3)
        self.listViewUndoStack.setObjectName("listViewUndoStack")
        self.gridLayout_6.addWidget(self.listViewUndoStack, 0, 0, 1, 1)

        self.G = GraphWidget('root', self)
        self.SceneLayout.addWidget(self.G)

        self.actionVariables.triggered.connect(self.toggleVariables)
        self.actionPlot_graph.triggered.connect(self.G.plot)
        self.actionDelete.triggered.connect(self.on_delete)
        self.actionPropertyView.triggered.connect(self.toggle_property_view)
        self.actionScreenshot.triggered.connect(self.G.screenShot)
        self.actionShortcuts.triggered.connect(self.shortcuts_info)
        self.actionSave.triggered.connect(self.G.save)
        self.actionLoad.triggered.connect(self.G.load)
        self.actionSave_as.triggered.connect(self.G.save_as)
        self.actionAlignLeft.triggered.connect(lambda: self.G.alignSelectedNodes(Direction.Left))
        self.actionAlignUp.triggered.connect(lambda: self.G.alignSelectedNodes(Direction.Up))
        self.actionAlignBottom.triggered.connect(lambda: self.G.alignSelectedNodes(Direction.Down))
        self.actionAlignRight.triggered.connect(lambda: self.G.alignSelectedNodes(Direction.Right))
        self.actionNew_Node.triggered.connect(lambda: self.newPlugin(PluginType.pNode))
        self.actionNew_Command.triggered.connect(lambda: self.newPlugin(PluginType.pCommand))
        self.actionFunction_Library.triggered.connect(lambda: self.newPlugin(PluginType.pFunctionLibrary))
        self.actionNew_pin.triggered.connect(lambda: self.newPlugin(PluginType.pPin))
        self.actionHistory.triggered.connect(self.toggleHistory)
        self.dockWidgetUndoStack.setVisible(False)

        self.setMouseTracking(True)

        self.variablesWidget = VariablesWidget(self, self.G)
        self.leftDockGridLayout.addWidget(self.variablesWidget)

        self._lastClock = 0.0
        self.fps = EDITOR_TARGET_FPS
        self.tick_timer = QtCore.QTimer()
        self.tick_timer.timeout.connect(self.mainLoop)

    def startMainLoop(self):
        self.tick_timer.start(1000 / EDITOR_TARGET_FPS)

    def mainLoop(self):
        deltaTime = clock() - self._lastClock
        ds = (deltaTime * 1000.0)
        if ds > 0:
            self.fps = int(1000.0 / ds)
        self.G.Tick(deltaTime)
        self._lastClock = clock()

    def createPopupMenu(self):
        pass

    def toggleHistory(self):
        self.dockWidgetUndoStack.setVisible(not self.dockWidgetUndoStack.isVisible())

    def newPlugin(self, pluginType):
        name, result = QInputDialog.getText(self, 'Plugin name', 'Enter plugin name')
        if result:
            _implementPlugin(name, pluginType)

    def closeEvent(self, event):
        self.tick_timer.stop()
        self.tick_timer.timeout.disconnect()
        self.G.shoutDown()
        # save editor config
        settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat, self)
        settings.beginGroup('Editor')
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())
        settings.endGroup()
        QMainWindow.closeEvent(self, event)

    def applySettings(self, settings):
        self.restoreGeometry(settings.value('Editor/geometry'))
        self.restoreState(settings.value('Editor/windowState'))

    def toggle_property_view(self):
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

        data = "Ctrl+Shift+N - togle node box\n"
        data += "Ctrl+N - new file\n"
        data += "Ctrl+S - save\n"
        data += "Ctrl+Shift+S - save as\n"
        data += "Ctrl+O - open file\n"
        data += "Ctrl+F - frame\n"
        data += "C - comment selected nodes\n"
        data += "Delete - kill selected nodes\n"
        data += "Ctrl+Shift+ArrowLeft - Align left\n"
        data += "Ctrl+Shift+ArrowUp - Align Up\n"
        data += "Ctrl+Shift+ArrowRight - Align right\n"
        data += "Ctrl+Shift+ArrowBottom - Align Bottom\n"

        QMessageBox.information(self, "Shortcuts", data)

    def on_delete(self):
        self.G.killSelectedNodes(True)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    app.setStyle(QStyleFactory.create("Cleanlooks"))

    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(50, 50, 50))
    darkPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(35, 35, 35))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(35, 35, 35))
    darkPalette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))

    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)

    app.setPalette(darkPalette)

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da;+ \
        border: 1px solid white;}\
        QWidget:focus {border:2 inset black;}\
        ")

    settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)

    instance = PyFlow()
    instance.applySettings(settings)
    instance.startMainLoop()

    app.setActiveWindow(instance)
    instance.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
