from AbstractGraph import *


G = AGraph('TEST_GRAPH')

intNode1 = AGIntNode('intNode1')
intNode1.set_data(2, False)

intNode2 = AGIntNode('intNode2')
intNode2.set_data(8, False)

# multNode = AGMultNode('mult1')

intNode3 = AGIntNode('intNode3')
intNode3.set_data(2, False)

discriminant = AGDiscriminantNode('disc1')

# sumNode1 = AGSumNode('SumNode1')
# sumNode2 = AGSumNode('SumNode2')

G.add_node(intNode1)
G.add_node(intNode2)
G.add_node(intNode3)
G.add_node(discriminant)
# G.add_node(intNode3)
# G.add_node(sumNode1)
# G.add_node(sumNode2)

# G.add_edge(intNode1.output, sumNode1.inputA)
# G.add_edge(intNode2.output, sumNode1.inputB)
# G.add_edge(sumNode1.output, sumNode2.inputA)
# G.add_edge(intNode3.output, sumNode2.inputB)
G.add_edge(intNode1.output, discriminant.inputA)
G.add_edge(intNode2.output, discriminant.inputB)
G.add_edge(intNode3.output, discriminant.inputC)

# print sumNode2.output.get_data()
# G.remove_edge(intNode1.output.edge_list[0])
print discriminant.output.get_data()
intNode1.set_data(9)
print discriminant.output.get_data()
G.plot()
# print sumNode2.output.get_data()
