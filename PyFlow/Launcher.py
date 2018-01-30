from os import path
import sys
from Qt import QtGui
from Qt import QtCore
from Widget import GraphWidget
from Widget import PluginType, _implementPlugin
from Widget import Direction
from Widget import NodesBox
from Nodes import getNodeNames
from Qt.QtWidgets import QMainWindow
from Qt.QtWidgets import QApplication
from Qt.QtWidgets import QStyleFactory
from Qt.QtWidgets import QTextEdit
from Qt.QtWidgets import QMessageBox
from Qt.QtWidgets import QAction
from Qt.QtWidgets import QInputDialog
from Qt.QtWidgets import QHBoxLayout
from Qt.QtWidgets import QUndoView
import GraphEditor_ui
from VariablesWidget import VariablesWidget
import json


FILE_DIR = path.dirname(__file__)
SETTINGS_PATH = FILE_DIR + "/appConfig.ini"


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
        self.actionHistory.triggered.connect(self.toggleHistory)
        self.dockWidgetUndoStack.setVisible(False)

        self.setMouseTracking(True)

        self.variablesWidget = VariablesWidget(self, self.G)
        self.leftDockGridLayout.addWidget(self.variablesWidget)

    def OnLoadEditorConfig(self, configJson):
        pass

    def createPopupMenu(self):
        pass

    def toggleHistory(self):
        self.dockWidgetUndoStack.setVisible(not self.dockWidgetUndoStack.isVisible())

    def newPlugin(self, pluginType):
        name, result = QInputDialog.getText(self, 'Plugin name', 'Enter plugin name')
        if result:
            _implementPlugin(name, pluginType)

    def closeEvent(self, event):
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

    instance = PyFlow()

    settings = QtCore.QSettings(SETTINGS_PATH, QtCore.QSettings.IniFormat)
    instance.applySettings(settings)

    app.setActiveWindow(instance)
    instance.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
