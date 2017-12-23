from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class StringToInt(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(StringToInt, self).__init__(name, graph)
        self.in_str = self.addInputPin('str', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        self.out_int = self.addOutputPin('int', DataTypes.Int, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.in_str, self.out_int)

    @staticmethod
    def category():
        return 'Convert'

    def compute(self):
        str_data = self.in_str.getData()
        try:
            self.out_int.setData(int(str_data))
        except Exception, e:
            print e
