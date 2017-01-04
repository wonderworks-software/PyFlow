from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode
from random import randint

DESC = '''Generates randint from range
'''

class RandInt(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(RandInt, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.rangeStart = self.add_input_port('from', AGPortDataTypes.tNumeric)
        self.rangeEnd = self.add_input_port('to', AGPortDataTypes.tNumeric)
        self.result = self.add_output_port('out', AGPortDataTypes.tNumeric)
        portAffects(self.rangeStart, self.result)
        portAffects(self.rangeEnd, self.result)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        vFrom = self.rangeStart.get_data()
        vTo = self.rangeEnd.get_data()
        try:
            self.result.set_data(randint(vFrom, vTo), True)
            push(self.result)
        except Exception as e:
            print(e)
