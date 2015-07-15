from AbstractGraph import *


class AGDiscriminantNode(AGNode):
    def __init__(self, name):
        super(AGDiscriminantNode, self).__init__(name)
        self.name = name
        self.inputA = self.add_port('inpA', AGPortTypes.kInput)
        self.inputB = self.add_port('inpB', AGPortTypes.kInput)
        self.inputC = self.add_port('inpC', AGPortTypes.kInput)
        self.output = self.add_port('out', AGPortTypes.kOutput)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)
        portAffects(self.inputC, self.output)

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()
        inpC_data = self.inputC.get_data()

        result = pow(inpB_data, 2) - 4*inpA_data*inpC_data

        self.output.set_data(result)
