# from PySide import QtGui
import sys

from Basics import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = GraphWidget()

    node1 = Node('Node name', widget, 120, 40)
    node1.add_port(PortTypes.kInput, 'Value', Colors.kBlue)
    node1.add_port(PortTypes.kInput, 'Value2', Colors.kRed)

    widget.scene_widget.addItem(node1)

    widget.show()
    sys.exit(app.exec_())
