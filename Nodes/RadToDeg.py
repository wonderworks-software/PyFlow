from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide.Node import Node
import math

DESC = '''Radians to
degrees
'''


class RadToDeg(Node, NodeBase):
    def __init__(self, name, graph):
        super(RadToDeg, self).__init__(name, graph, spacings=Spacings)
        self.inp0 = self.add_input_port('rad', DataTypes.Float)
        self.out0 = self.add_output_port('deg', DataTypes.Float)
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
            self.out0.set_data(math.degrees(data), False)
        except Exception as e:
            print(e)
