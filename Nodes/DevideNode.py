from AGraphPySide import BaseNode
from AbstractGraph import *


class DevideNode(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(DevideNode, self).__init__(name, graph)
        AGNode.__init__(self, name, graph)
        self.number = self.add_input_port('number', AGPortDataTypes.tNumeric)
        self.devider = self.add_input_port('devider', AGPortDataTypes.tNumeric)
        self.output = self.add_output_port('output', AGPortDataTypes.tNumeric)
        portAffects(self.number, self.output)
        portAffects(self.devider, self.output)

    def compute(self):

        number = self.number.get_data()
        devider = self.devider.get_data()
        try:
            result = number / float(devider)
            self.output.set_data(result, False)
        except Exception, e:
            print e
