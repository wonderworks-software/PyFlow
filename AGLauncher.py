from AbstractGraph import *


G = AGraph('TEST_GRAPH')

intNode1 = AGIntNode('intNode1', G)
intNode1.set_data(4, False)

intNode2 = AGIntNode('intNode2', G)
intNode2.set_data(6, False)

sumNode1 = AGSumNode('SumNode1', G)

G.add_node(intNode1)
G.add_node(intNode2)
G.add_node(sumNode1)

G.add_edge(intNode1.output, sumNode1.inputA)
G.add_edge(intNode2.output, sumNode1.inputB)

G.plot()
