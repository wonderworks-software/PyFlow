from PySide import QtGui, QtCore
from AGraphPySide import *


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(444, 362)
            self.centralwidget = QtGui.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
            self.gridLayout_2.setObjectName("gridLayout_2")
            self.splitter = QtGui.QSplitter(self.centralwidget)
            self.splitter.setOrientation(QtCore.Qt.Horizontal)
            self.splitter.setObjectName("splitter")
            self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
            self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
            self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.gridLayoutWidget = QtGui.QWidget(self.splitter)
            self.gridLayoutWidget.setObjectName("gridLayoutWidget")
            self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)
            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtGui.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
            self.menuBar = QtGui.QMenuBar(MainWindow)
            self.menuBar.setGeometry(QtCore.QRect(0, 0, 444, 18))
            self.menuBar.setObjectName("menuBar")
            MainWindow.setMenuBar(self.menuBar)
            self.toolBar = QtGui.QToolBar(MainWindow)
            self.toolBar.setObjectName("toolBar")
            MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
            self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))


    class W(QtGui.QMainWindow, Ui_MainWindow):
        def __init__(self):
            super(W, self).__init__()
            self.setupUi(self)
            G = GraphWidget('TEST_GRAPH')
            node_box = Widget.NodesBox(G)
            node_box.setVisible(True)
            node_box.listWidget._events = False
            node_box.le_nodes._events = False
            self.gridLayout.addWidget(G)
            self.verticalLayout.addWidget(node_box)


    instance = W()
    instance.show()

    sys.exit(app.exec_())
