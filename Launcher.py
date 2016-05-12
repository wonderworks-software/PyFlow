from AGraphPySide import *
import test_app_ui
import sys
print sys.executable


class ConsoleInput(QtGui.QLineEdit):
    def __init__(self, parent, graph):
        super(ConsoleInput, self).__init__(parent)
        self.graph = graph
        self.returnPressed.connect(self.OnReturnPressed)
        self.model = QtGui.QStringListModel()
        self.executedCommands = ["plot",
        "help",
        "createNode",
        "load",
        "save",
        "killNode",
        "move",
        "select",
        "connectAttr",
        "disconnectAttr",
        "setAttr",
        "comment"]
        self.builtinCommands = [] + self.executedCommands
        self.completer = QtGui.QCompleter(self)
        self.model.setStringList(self.executedCommands)
        self.completer.setModel(self.model)
        self.completer.setCompletionMode(self.completer.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(self.completer)

    def OnReturnPressed(self):
        line = self.text()
        if line not in self.executedCommands:
            self.executedCommands.append(line)
        self.model.setStringList(self.executedCommands)
        self.graph.executeCommand(line)
        self.clear()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)


    class W(QtGui.QMainWindow, test_app_ui.Ui_MainWindow):
        def __init__(self):
            super(W, self).__init__()
            self.setupUi(self)
            self.G = GraphWidget('TEST_GRAPH', self)
            self.node_box = Widget.NodesBox(self.G)
            self.node_box.listWidget._events = False
            self.node_box.le_nodes._events = False
            self.SceneLayout.addWidget(self.G)
            self.NodeBoxLayout.addWidget(self.node_box)
            self.node_box.setVisible(True)
            self.actionPlot_graph.triggered.connect(self.G.plot)
            self.actionDelete.triggered.connect(self.z)
            self.cb_multithreaded.toggled.connect(self.toggle_multithreaded)
            self.cb_debug.toggled.connect(self.toggle_debug)
            self.cb_shadows.toggled.connect(self.toggle_shadows)
            self.actionConsole.triggered.connect(self.toggle_console)
            self.actionNode_box.triggered.connect(self.toggle_node_box)
            self.horizontal_splitter.setHandleWidth(Spacings.kSplitterHandleWidth)
            self.console.setReadOnly(True)
            self.console.setStyleSheet('background-color: rgb(49, 49, 49);'+\
                                       'font: 8pt "Consolas";'+\
                                       'color: rgb(200, 200, 200);'
                                       )
            self.clearConsoleAction = QtGui.QAction('Clear', self)
            self.clearConsoleAction.triggered.connect(lambda: self.console.clear())
            self.console.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
            self.console.addAction(self.clearConsoleAction)
            self.consoleInput = ConsoleInput(self.dockWidgetContents_2, self.G)
            self.gridLayout_2.addWidget(self.consoleInput, 2, 0, 1, 1)

        def toggle_node_box(self):

            if self.node_box.isVisible():
                self.dockWidgetNodeBox.hide()
            else:
                self.dockWidgetNodeBox.show()

        def toggle_multithreaded(self):

            self.G.set_multithreaded(not self.G.is_multithreaded())

        def toggle_console(self):

            if self.dockWidgetConsole.isVisible():
                self.dockWidgetConsole.hide()
            else:
                self.dockWidgetConsole.show()

        def toggle_debug(self):

            self.G.set_debug(not self.G.is_debug())

        def toggle_shadows(self):

            self.G.set_shadows_enabled(not self.G._shadows)

        def z(self):
            for i in self.G.nodes:
                print i.name, i.zValue()
            for i in self.G.groupers:
                print i.zValue()

    instance = W()
    instance.show()

    # G = GraphWidget('TEST_GRAPH')
    # G.show()

    try:
        sys.exit(app.exec_())
    except Exception, e:
        print e
