from AbstractGraph import *
from AGraphPySide.Settings import *
from AGraphPySide import BaseNode

DESC = '''Return the absolute value of a number. The argument may be a plain or long integer or a floating point number. If the argument is a complex number, its magnitude is returned.
'''


class Abs(BaseNode.Node, AGNode):
    def __init__(self, name, graph):
        super(Abs, self).__init__(name, graph, w=50, spacings=Spacings)
        self.inp0 = self.add_input_port('in', AGPortDataTypes.tFloat)
        self.out0 = self.add_output_port('out', AGPortDataTypes.tFloat)
        portAffects(self.inp0, self.out0)

    @staticmethod
    def get_category():
        return 'Math'

    @staticmethod
    def description():
        return DESC

    def compute(self):

        data = self.inp0.get_data()
        try:
            self.out0.set_data(abs(data), False)
        except Exception as e:
            print(e)
