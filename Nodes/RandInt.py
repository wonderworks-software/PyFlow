from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode
from random import randint


class RandInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(RandInt, self).__init__(name, graph,
                                      w=120, colors=Colors,
                                      spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.graph = graph
        self.inFrom = self.add_input_port('from', AGPortDataTypes.tNumeric)
        self.inTo = self.add_input_port('to', AGPortDataTypes.tNumeric)
        self.output = self.add_output_port('out', AGPortDataTypes.tNumeric)
        portAffects(self.inFrom, self.output)
        portAffects(self.inTo, self.output)

    def compute(self):

        fromVal = self.inFrom.get_data()
        toVal = self.inTo.get_data()
        try:
            result = randint(fromVal, toVal)
            self.output.set_data(result, True)
        except Exception, e:
            print e

