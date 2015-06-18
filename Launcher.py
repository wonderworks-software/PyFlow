import sys
from Node import Node
from Widget import GraphWidget
from PySide import QtGui
from Settings import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = GraphWidget()

    node1 = Node('A', widget, 120, 40)
    node2 = Node('B', widget, 120, 40)
    # node3 = Node('C', widget, 120, 40)

    node1.add_port(PortTypes.kOutput, '1', Colors.kBlue)
    node1.add_port(PortTypes.kOutput, '2')

    node2.add_port(PortTypes.kInput, '1')
    node2.add_port(PortTypes.kInput, '2')

    widget.scene_widget.addItem(node1)
    widget.scene_widget.addItem(node2)

    # widget.scene_widget.addItem(node3)

    widget.show()
    sys.exit(app.exec_())
