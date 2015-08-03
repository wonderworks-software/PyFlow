from PySide import QtGui, QtCore
from AGraphPySide import *
import test_app_ui


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    class W(QtGui.QMainWindow, test_app_ui.Ui_MainWindow):
        def __init__(self):
            super(W, self).__init__()
            self.setupUi(self)
            self.G = GraphWidget('TEST_GRAPH')
            node_box = Widget.NodesBox(self.G)
            node_box.setVisible(True)
            node_box.listWidget._events = False
            node_box.le_nodes._events = False
            self.gridLayout.addWidget(self.G)
            self.verticalLayout.addWidget(node_box)
            self.actionDelete.triggered.connect(self.nodes_instances)
        def nodes_instances(self):
            self.G.scene_widget.clear()


    instance = W()
    instance.show()

    # G = GraphWidget('TEST_GRAPH')
    # G.show()

    try:
        sys.exit(app.exec_())
    except Exception, e:
        print e
