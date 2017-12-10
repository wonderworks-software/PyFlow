from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class FloatToInt(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        ConvertNode.__init__(self, name, graph)
        self.fromType = self.add_input_port('from', DataTypes.Float, hideLabel=True, bCreateInputWidget=False)
        self.toType = self.add_output_port('to', DataTypes.Int, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.fromType, self.toType)

    @staticmethod
    def description():
        return "Converts float to integer"

    def compute(self):
        data = self.fromType.get_data()
        try:
            self.toType.set_data(int(data))
        except Exception, e:
            self.graph.write_to_console("[ERROR] {0}".format(e))
