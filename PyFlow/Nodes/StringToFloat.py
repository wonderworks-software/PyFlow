from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class StringToFloat(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(StringToFloat, self).__init__(name, graph)
        self.in_str = self.addInputPin('str', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        self.out_flt = self.addOutputPin('float', DataTypes.Float, hideLabel=True, bCreateInputWidget=False)
        pinAffects(self.in_str, self.out_flt)

    @staticmethod
    def pinTypeHints():
        return {'inputs': [DataTypes.String], 'outputs': [DataTypes.Float]}

    @staticmethod
    def category():
        return 'Convert'

    def compute(self):

        str_data = self.in_str.getData()
        try:
            self.out_flt.setData(float(str_data))
        except Exception, e:
            print e
