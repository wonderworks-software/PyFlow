from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode


DESC = """flifs boolean
"""


class Not(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Not, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.in_bool = self.add_input_port('in', AGPortDataTypes.tBool)
        self.out_bool = self.add_output_port('out', AGPortDataTypes.tBool)
        portAffects(self.in_bool, self.out_bool)

    @staticmethod
    def get_category():
        return 'Common'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        in_bool = self.in_bool.get_data()
        try:
            self.out_bool.set_data(not in_bool, False)
        except Exception as e:
            print(e)
