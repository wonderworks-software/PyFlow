from AGraphPySide import *
import GraphEditor_ui
import sys


class Highlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None, commandNameList= [], nodes_names = []):
        super(Highlighter, self).__init__(parent)

        # nodeNamePatterns = nodes_names
        # nodeNameFormat = QtGui.QTextCharFormat()
        # nodeNameFormat.setForeground(QtCore.Qt.green)
        # nodeNameFormat.setFontWeight(QtGui.QFont.Bold)

        # self.highlightingRules = [(QtCore.QRegExp(pattern), nodeNameFormat)
        #         for pattern in nodeNamePatterns]

        comandPatterns = commandNameList
        commandNameFormat = QtGui.QTextCharFormat()
        commandNameFormat.setForeground(QtCore.Qt.cyan)
        commandNameFormat.setFontWeight(QtGui.QFont.Bold)


        self.highlightingRules = [(QtCore.QRegExp(pattern), commandNameFormat)
                for pattern in comandPatterns]

        singleLineCommentFormat = QtGui.QTextCharFormat()
        singleLineCommentFormat.setForeground(QtCore.Qt.darkYellow)
        self.highlightingRules.append((QtCore.QRegExp("//[^\n]*"),
                singleLineCommentFormat))

        flagFormat = QtGui.QTextCharFormat()
        flagFormat.setForeground(QtCore.Qt.darkCyan)
        # flagFormat.setFontWeight(QtGui.QFont.Bold)
        self.highlightingRules.append((QtCore.QRegExp("/\w+"),
                flagFormat))


        self.multiLineCommentFormat = QtGui.QTextCharFormat()
        self.multiLineCommentFormat.setForeground(QtCore.Qt.red)

        quotationFormat = QtGui.QTextCharFormat()
        quotationFormat.setForeground(QtCore.Qt.yellow)
        self.highlightingRules.append((QtCore.QRegExp("\'.*\'"),
                quotationFormat))

        functionFormat = QtGui.QTextCharFormat()
        functionFormat.setFontItalic(True)
        functionFormat.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()"),
                functionFormat))

        self.commentStartExpression = QtCore.QRegExp("/\\*")
        self.commentEndExpression = QtCore.QRegExp("\\*/")

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = self.commentEndExpression.indexIn(text, startIndex)

            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

            self.setFormat(startIndex, commentLength,
                    self.multiLineCommentFormat)
            startIndex = self.commentStartExpression.indexIn(text,
                    startIndex + commentLength);


class ConsoleInput(QtGui.QLineEdit):
    def __init__(self, parent, graph):
        super(ConsoleInput, self).__init__(parent)
        self.graph = graph
        self.returnPressed.connect(self.OnReturnPressed)
        self.model = QtGui.QStringListModel()
        self.cmd_list = ["renameNode", "plot", "help", "createNode", "save", "load", "comment", "killNode", "setAttr", "connectAttr", "disconectAttr", "select", "move", "pluginWizard"]
        self.executedCommands = [i for i in self.graph.registeredCommands.iterkeys()] + self.cmd_list
        self.builtinCommands = self.cmd_list
        self.completer = QtGui.QCompleter(self)
        self.model.setStringList(self.executedCommands)
        self.completer.setModel(self.model)
        self.completer.setCompletionMode(self.completer.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(self.completer)
        font = QtGui.QFont("Consolas", 9, QtGui.QFont.Bold, False)
        self.setFont(font)

    def OnReturnPressed(self):
        line = self.text()
        if line not in self.executedCommands:
            self.executedCommands.append(line)
        self.model.setStringList(self.executedCommands)
        self.graph.executeCommand(line)
        self.clear()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)

    app.setStyle(QtGui.QStyleFactory.create("Cleanlooks"));

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

    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")


    class W(QtGui.QMainWindow, GraphEditor_ui.Ui_MainWindow):
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
            self.actionConsole.triggered.connect(self.toggle_console)
            self.actionNode_box.triggered.connect(self.toggle_node_box)
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

        def closeEvent(self, event):
            question = "Shure?"
            reply = QtGui.QMessageBox.question(self, 'Exit', question, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

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
