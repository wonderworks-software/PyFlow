from AbstractGraph import *


class AGDiscriminantNode(AGNode):
    def __init__(self, name):
        super(AGDiscriminantNode, self).__init__(name)
        self.inputA = self.add_input_port('inpA', DataTypes.Numeric)
        self.inputB = self.add_input_port('inpB', DataTypes.Numeric)
        self.inputC = self.add_input_port('inpC', DataTypes.Numeric)
        self.output = self.add_output_port('out', DataTypes.Numeric)
        portAffects(self.inputA, self.output)
        portAffects(self.inputB, self.output)
        portAffects(self.inputC, self.output)

    def compute(self):

        inpA_data = self.inputA.get_data()
        inpB_data = self.inputB.get_data()
        inpC_data = self.inputC.get_data()
        try:
            result = pow(inpB_data, 2) - 4*inpA_data*inpC_data
        except Exception, e:
            print self.name, e
            return
        self.output.set_data(result, False)
