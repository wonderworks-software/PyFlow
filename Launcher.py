import sys
from BaseNode import Node
from IntNode import IntNode
from Widget import GraphWidget
from Settings import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = GraphWidget('test')

    node1 = Node('BaseNodeA', widget)
    int_node1 = IntNode('IntNode', widget)
    int_node2 = IntNode('IntNode2', widget)

    node1.add_port(PortTypes.kInput, 'in1')
    node1.add_port(PortTypes.kInput, 'in2')

    widget.scene_widget.addItem(node1)
    widget.scene_widget.addItem(int_node1)
    widget.scene_widget.addItem(int_node2)

    # widget.scene_widget.addItem(node3)

    widget.show()
    sys.exit(app.exec_())
