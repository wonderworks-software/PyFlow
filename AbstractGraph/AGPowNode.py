from AbstractGraph import *


class AGMultNode(AGNode):
    def __init__(self, name):
        super(AGMultNode, self).__init__(name)
        self.name = name
        self.inputA = self.add_input_port('inpA')
        self.inputB = self.add_input_port('inpB')
        self.output = self.add_output_port('out')
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()

        result = pow(inpA_data, inpB_data)

        self.output.set_data(result, False)
