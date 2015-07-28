from PySide import QtGui
from AGraphPySide import *


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    G = GraphWidget('TEST_GRAPH')

    G.show()

    sys.exit(app.exec_())
