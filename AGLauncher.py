from AbstractGraph import *


G = AGraph('TEST_GRAPH')
G.set_debug(True)
# G.set_multithreaded(True)

intNode1 = AGIntNode('intNode1')
intNode1.set_data(4, False)

intNode2 = AGIntNode('intNode2')
intNode2.set_data(6, False)

# intNode3 = AGIntNode('intNode3')
# intNode3.set_data(7, False)


sumNode1 = AGSumNode('SumNode1')
sumNode2 = AGSumNode('SumNode2')
sumNode3 = AGSumNode('SumNode3')

G.add_node(intNode1)
G.add_node(intNode2)
# G.add_node(intNode3)
G.add_node(sumNode1)
G.add_node(sumNode2)
G.add_node(sumNode3)

G.add_edge(sumNode1.inputA, intNode1.output)
G.add_edge(intNode1.output, sumNode3.inputA)
G.add_edge(intNode2.output, sumNode1.inputB)
G.add_edge(intNode2.output, sumNode2.inputB)
G.add_edge(sumNode1.output, sumNode2.inputA)
G.add_edge(sumNode2.output, sumNode3.inputB)

print sumNode3.output.get_data()
intNode2.set_data(5, dirty_propagate=True)
print sumNode3.output.get_data()
# G.plot()
# intNode1.set_data(4)
# print sumNode2.output.get_data()
