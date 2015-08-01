from AbstractGraph import *


G = AGraph('TEST_GRAPH')
G.set_debug(True)
# G.set_multithreaded(True)

intNode1 = AGIntNode('intNode1', G)
intNode1.set_data(4, False)

intNode2 = AGIntNode('intNode2', G)
intNode2.set_data(6, False)


sumNode1 = AGSumNode('SumNode1', G)

G.add_node(intNode1, 0, 0)
G.add_node(intNode2, 0, 0)
G.add_node(sumNode1, 0, 0)

G.add_edge(sumNode1.inputA, intNode1.output)
G.add_edge(intNode2.output, sumNode1.inputB)

intNode1.kill()

G.plot()
# G.plot()
# intNode2.set_data(5, dirty_propagate=True)
# print sumNode3.output.get_data()
# intNode1.set_data(4)
# print sumNode2.output.get_data()
