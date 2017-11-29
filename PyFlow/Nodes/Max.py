from AbstractGraph import *
from Settings import *
from Node import Node

DESC = '''returns maximum element of iterable object
'''


class Max(Node, NodeBase):
    def __init__(self, name, graph):
        super(Max, self).__init__(name, graph, spacings=Spacings)
        self.inp0 = self.add_input_port('in', DataTypes.Any)
        self.out0 = self.add_output_port('out', DataTypes.Any)
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
