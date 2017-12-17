from AbstractGraph import *
from Settings import *
from ConvertNode import ConvertNode


class ToString(ConvertNode, NodeBase):
    def __init__(self, name, graph):
        super(ToString, self).__init__(name, graph)
        self.in_data = self.add_input_port('in', DataTypes.Any, hideLabel=True, bCreateInputWidget=False)
        self.out_data = self.add_output_port('out', DataTypes.String, hideLabel=True, bCreateInputWidget=False)
        portAffects(self.in_data, self.out_data)

    @staticmethod
    def category():
        return 'Convert'

    def compute(self):

        out_data = self.in_data.get_data()
        try:
            self.out_data.set_data(str(out_data))
        except Exception, e:
            print e
