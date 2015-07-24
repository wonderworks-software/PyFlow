from PySide import QtGui
from AGraphPySide import Widget
from AGraphPySide import IntNode
from AGraphPySide import SumNode


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)

    G = Widget.GraphWidget('TEST_GRAPH')
    G.set_debug(True)
    # G.set_multithreaded(True)

    intNode1 = IntNode.IntNode('int1', G)
    intNode2 = IntNode.IntNode('int2', G)
    intNode3 = IntNode.IntNode('int3', G)

    sumNode1 = SumNode.SumNode('sumNode1', G)
    sumNode2 = SumNode.SumNode('sumNode2', G)
    sumNode3 = SumNode.SumNode('sumNode3', G)

    G.add_node(intNode1, 100, 80)
    G.add_node(intNode2, 50, 400)
    G.add_node(intNode3, 400, 500)
    G.add_node(sumNode1, 300, 300)
    G.add_node(sumNode2, 500, 50)
    G.add_node(sumNode3, 800, 150)

    # G.add_edge(intNode1.output, sumNode1.inputA)
    # G.add_edge(intNode1.output, sumNode2.inputA)
    # G.add_edge(intNode2.output, sumNode1.inputB)
    # G.add_edge(sumNode1.output, sumNode2.inputB)
    # G.add_edge(sumNode2.output, sumNode3.inputA)
    # G.add_edge(intNode3.output, sumNode3.inputB)

    G.show()
    # G.plot()
    sys.exit(app.exec_())
