from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node
from random import randint

DESC = '''Generates randint from range
'''


class RandInt(Node, NodeBase):
    def __init__(self, name, graph):
        super(RandInt, self).__init__(name, graph, spacings=Spacings)
        self.rangeStart = self.add_input_port('from', DataTypes.Int)
        self.rangeEnd = self.add_input_port('to', DataTypes.Int)
        self.result = self.add_output_port('out', DataTypes.Int)
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
