from AbstractGraph import *
from Settings import *
from Node import Node
import math

DESC = '''Degrees to
radians
'''


class DegToRad(Node, NodeBase):
    def __init__(self, name, graph):
        super(DegToRad, self).__init__(name, graph, spacings=Spacings)
        self.inp0 = self.add_input_port('deg', DataTypes.Float)
        self.out0 = self.add_output_port('rad', DataTypes.Float)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Convert'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(math.radians(data), False)
        except Exception as e:
            print(e)
