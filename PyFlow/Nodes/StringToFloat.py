from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class StringToFloat(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(StringToFloat, self).__init__(name, graph)
        self.in_str = self.add_input_port('str', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        self.out_flt = self.add_output_port('float', DataTypes.Float, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.in_str, self.out_flt)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):

        str_data = self.in_str.get_data()
        try:
            self.out_flt.set_data(float(str_data))
        except Exception, e:
            print e
