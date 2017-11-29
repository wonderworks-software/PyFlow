from AGraphPySide.Node import Node
from AbstractGraph import *


class PowNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(PowNode, self).__init__(name, graph)
        self.base = self.add_input_port('base', DataTypes.Float)
        self.power = self.add_input_port('power', DataTypes.Float)
        self.output = self.add_output_port('output', DataTypes.Float)
        portAffects(self.base, self.output)
        portAffects(self.power, self.output)

    @staticmethod
    def get_category():
        return 'Math'

    def compute(self):

        base_data = self.base.get_data()
        power_data = self.power.get_data()
        try:
            result = pow(base_data, power_data)
            self.output.set_data(result, False)
        except Exception, e:
            print e
