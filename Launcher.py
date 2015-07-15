from AbstractGraph import *


G = AGraph('TEST_GRAPH')

intNode1 = AGIntNode('intNode1')
intNode1.set_data(2, False)

intNode2 = AGIntNode('intNode2')
intNode2.set_data(8, False)

intNode3 = AGIntNode('intNode3')
intNode3.set_data(2, False)


sumNode1 = AGSumNode('SumNode1')
sumNode2 = AGSumNode('SumNode2')

G.add_node(intNode1)
G.add_node(intNode2)
G.add_node(intNode3)
G.add_node(sumNode1)
G.add_node(sumNode2)

G.add_edge(intNode1.output, sumNode1.inputA)
G.add_edge(intNode2.output, sumNode1.inputB)
G.add_edge(sumNode1.output, sumNode2.inputA)
G.add_edge(intNode3.output, sumNode2.inputB)

print sumNode2.output.get_data()
# intNode1.set_data(4)
# G.plot()
# print sumNode2.output.get_data()
