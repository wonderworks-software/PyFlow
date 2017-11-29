from AbstractGraph import *


class AGMultNode(AGNode):
    def __init__(self, name):
        super(AGMultNode, self).__init__(name)
        self.name = name
        self.inputA = self.add_input_port('inpA', DataTypes.Numeric)
        self.inputB = self.add_input_port('inpB', DataTypes.Numeric)
        self.output = self.add_output_port('out', DataTypes.Numeric)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()

        result = inpA_data * inpB_data

        self.output.set_data(result, False)
