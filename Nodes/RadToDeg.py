from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode
import math

DESC = '''Radians to
degrees
'''

class RadToDeg(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(RadToDeg, self).__init__(name, graph, w=150, colors=Colors, spacings=Spacings)
        AGNode.__init__(self, name, graph)
        self.inp0 = self.add_input_port('radians', AGPortDataTypes.tNumeric)
        self.out0 = self.add_output_port('degrees', AGPortDataTypes.tNumeric)
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
