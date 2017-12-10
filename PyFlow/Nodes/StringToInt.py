from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class StringToInt(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(StringToInt, self).__init__(name, graph)
        self.in_str = self.add_input_port('str', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        self.out_int = self.add_output_port('int', DataTypes.Int, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.in_str, self.out_int)

    @staticmethod
    def get_category():
        return 'Convert'

    def compute(self):
        str_data = self.in_str.get_data()
        try:
            self.out_int.set_data(int(str_data))
        except Exception, e:
            print e
