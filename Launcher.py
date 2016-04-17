from AGraphPySide import *
import test_app_ui
import sys
print sys.executable

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
            self.vertical_splitter.setHandleWidth(Spacings.kSplitterHandleWidth)
            self.horizontal_splitter.setHandleWidth(Spacings.kSplitterHandleWidth)
            self.vertical_splitter.setSizes([self.width(), self.height()/10])
            self.console.setReadOnly(True)
            self.console.setStyleSheet('background-color: rgb(49, 49, 49);'+\
                                       'font: 8pt "Consolas";'+\
                                       'color: rgb(200, 200, 200);'
                                       )
            self.console.hide()

        def toggle_node_box(self):

            if self.node_box.isVisible():
                self.NodeBoxWidget.hide()
            else:
                self.NodeBoxWidget.show()

        def toggle_multithreaded(self):

            self.G.set_multithreaded(not self.G.is_multithreaded())

        def toggle_console(self):

            if self.console.isVisible():
                self.console.hide()
            else:
                self.console.show()

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
