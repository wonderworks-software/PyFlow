from AGraphPySide import BaseNode
from AbstractGraph import *


class PowNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(PowNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.base = self.add_input_port('base', AGPortDataTypes.tNumeric)
        self.power = self.add_input_port('power', AGPortDataTypes.tNumeric)
        self.output = self.add_output_port('output', AGPortDataTypes.tNumeric)
        portAffects(self.base, self.output)
        portAffects(self.power, self.output)

    def compute(self):

        base_data = self.base.get_data()
        power_data = self.power.get_data()
        try:
            result = pow(base_data, power_data)
            self.output.set_data(result, True)
        except Exception, e:
            print e
