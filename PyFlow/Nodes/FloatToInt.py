from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class FloatToInt(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        ConvertNode.__init__(self, name, graph)
        self.fromType = self.addInputPin('from', DataTypes.Float, hideLabel=True, bCreateInputWidget=False)
        self.toType = self.addOutputPin('to', DataTypes.Int, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.fromType, self.toType)

    @staticmethod
    def description():
        return "Converts float to integer"

    def compute(self):
        data = self.fromType.getData()
        try:
            self.toType.setData(int(data))
        except Exception, e:
            self.graph.writeToConsole("[ERROR] {0}".format(e))
