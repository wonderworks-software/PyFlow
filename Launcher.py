import sys
from Node import Node
from Widget import GraphWidget
from Settings import *


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = GraphWidget('test')

    custom_colors = Colors()
    custom_colors.kNodeBackgrounds = QtGui.QColor(80, 0, 0, 100)
    node1 = Node('A', widget, 180, custom_colors)
    node2 = Node('B', widget)
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
