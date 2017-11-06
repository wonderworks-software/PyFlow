from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode

DESC = '''returns minimum element
of iterable object.
'''


class Min(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Min, self).__init__(name, graph, spacings=Spacings)
        self.inp = self.add_input_port('in', AGPortDataTypes.tAny)
        self.out = self.add_output_port('min', AGPortDataTypes.tAny)
        portAffects(self.inp, self.out)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        inp = self.inp.get_data()
        try:
            self.out.set_data(min(inp), False)
        except Exception as e:
            print(e)
