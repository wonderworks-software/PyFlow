from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode

DESC = '''returns maximum element of iterable object
'''

class Max(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Max, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp0 = self.add_input_port('in', AGPortDataTypes.tAny)
        self.out0 = self.add_output_port('out', AGPortDataTypes.tAny)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(max(data), False)
        except Exception as e:
            print(e)
