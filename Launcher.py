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

    sumNode1 = SumNode.SumNode('sumNode1', G)
    sumNode2 = SumNode.SumNode('sumNode2', G)

    G.add_node(intNode1)
    G.add_node(intNode2)
    G.add_node(sumNode1)
    G.add_node(sumNode2)

    G.add_edge(intNode1.output, sumNode1.inputA)
    G.add_edge(intNode1.output, sumNode2.inputA)
    G.add_edge(intNode2.output, sumNode1.inputB)
    G.add_edge(sumNode1.output, sumNode2.inputB)

    G.show()
    # G.plot()
    sys.exit(app.exec_())
