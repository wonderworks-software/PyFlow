from AGraphPySide import *
import GraphEditor_ui
import sys
from os import path


FILE_DIR = path.dirname(__file__)


class W(QtGui.QMainWindow, GraphEditor_ui.Ui_MainWindow):
    def __init__(self):
        super(W, self).__init__()
        self.setupUi(self)
        self.G = GraphWidget('MAIN_GRAPH', self)
        self.node_box = Widget.NodesBox(self.G)
        self.node_box.listWidget._events = False
        self.node_box.le_nodes._events = False
        self.SceneLayout.addWidget(self.G)
        self.NodeBoxLayout.addWidget(self.node_box)
        self.node_box.setVisible(True)

        self.actionPlot_graph.triggered.connect(self.G.plot)
        self.actionDelete.triggered.connect(self.on_delete)
        self.actionConsole.triggered.connect(self.toggle_console)
        self.actionNode_box.triggered.connect(self.toggle_node_box)
        self.actionPropertyView.triggered.connect(self.toggle_property_view)
        self.actionMultithreaded.triggered.connect(self.toggle_multithreaded)
        self.actionDebug.triggered.connect(self.toggle_debug)
        self.actionShadows.triggered.connect(self.toggle_shadows)
        self.actionScreenshot.triggered.connect(self.G.screen_shot)
        self.actionClear_scene.triggered.connect(self.on_clear_scene)
        self.actionShortcuts.triggered.connect(self.shortcuts_info)
        self.actionOptions.triggered.connect(self.G.options)
        self.actionGroup_selected.triggered.connect(self.G.commentSelectedNodes)
        self.actionSave.triggered.connect(self.G.save)
        self.actionLoad.triggered.connect(self.G.load)
        self.actionSave_as.triggered.connect(self.G.save_as)
        self.actionAlignLeft.triggered.connect(lambda: self.G.align_selected_nodes(True))
        self.actionAlignUp.triggered.connect(lambda: self.G.align_selected_nodes(False))

        self.horizontal_splitter.setHandleWidth(Spacings.kSplitterHandleWidth)
        self.console.setLineWrapMode(QtGui.QTextEdit.NoWrap)
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
        commands_names = [i for i in self.G.registeredCommands.iterkeys()] + self.consoleInput.cmd_list
        self.highlighter_inst = Highlighter(self.console.document(),
            commands_names,
            self.node_box.get_nodes_file_names()
            )
        self.gridLayout_2.addWidget(self.consoleInput, 2, 0, 1, 1)
        self.dockWidgetConsole.hide()
        self.dockWidgetNodeBox.hide()
        self.setMouseTracking(True)
        self.toggle_console()
        self.toggle_node_box()
        self.toggle_shadows()

    def closeEvent(self, event):
        question = "Shure?"
        reply = QtGui.QMessageBox.question(self, 'Exit', question, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.G.shoutDown()
            event.accept()
        else:
            event.ignore()

    def toggle_property_view(self):
        if self.dockWidgetNodeView.isVisible():
            self.dockWidgetNodeView.setVisible(False)
        else:
            self.dockWidgetNodeView.setVisible(True)

    def toggle_node_box(self):

        if self.node_box.isVisible():
            self.dockWidgetNodeBox.hide()
        else:
            self.dockWidgetNodeBox.show()

    def shortcuts_info(self):

        data = "Ctrl+Shift+N - togle node box\n"
        data += "Ctrl+Shift+C - togle console\n"
        data += "Ctrl+N - new file\n"
        data += "Ctrl+S - save\n"
        data += "Ctrl+Shift+S - save as\n"
        data += "Ctrl+O - open file\n"
        data += "Ctrl+F - frame\n"
        data += "Ctrl+Shift+Alt+C - comment selected nodes\n"
        data += "Ctrl+Shift+Alt+S - toggle nodes shadows\n"
        data += "Ctrl+Alt+M - toggle multithreaded\n"
        data += "Ctrl+Alt+D - toggle debug\n"
        data += "Delete - kill selected nodes\n"
        data += "Ctrl+Shift+A - Align left\n"
        data += "Ctrl+Shift+Q - Align Up\n"

        QtGui.QMessageBox.information(self, "Shortcuts", data)

    def toggle_multithreaded(self):

        self.G.set_multithreaded(not self.G.is_multithreaded())
        if self.G.is_multithreaded():
            self.G.notify("Multithreaded mode enabled", 3000)
        else:
            self.G.notify("Multithreaded mode disabled", 3000)

    def toggle_console(self):

        if self.dockWidgetConsole.isVisible():
            self.dockWidgetConsole.hide()
        else:
            self.dockWidgetConsole.show()

    def on_clear_scene(self):
        for n in self.G.get_nodes():
            n.kill()

    def toggle_debug(self):

        self.G.set_debug(not self.G.is_debug())
        if self.G.is_debug():
            self.G.notify("Debug mode enabled", 3000)
        else:
            self.G.notify("Debug mode disabled", 3000)

    def toggle_shadows(self):

        self.G.set_shadows_enabled(not self.G._shadows)

    def on_delete(self):
        self.G.kill_selected_nodes(True)


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))

    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    darkPalette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(25,25,25))
    darkPalette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
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


    instance = W()
    instance.show()


    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
