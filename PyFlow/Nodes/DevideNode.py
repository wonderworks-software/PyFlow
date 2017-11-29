from Node import Node
from AbstractGraph import *


class DevideNode(Node, NodeBase):
    def __init__(self, name, graph):
        super(DevideNode, self).__init__(name, graph)

        self.number = self.add_input_port('number', DataTypes.Float)
        self.number.port_connected = self.number_port_connected
        self.number.port_disconnected = self.number_port_disconnected

        self.devider = self.add_input_port('devider', DataTypes.Float)
        self.devider.port_connected = self.devider_port_connected
        self.devider.port_disconnected = self.devider_port_disconnected

        self.output = self.add_output_port('output', DataTypes.Float)
        portAffects(self.number, self.output)
        portAffects(self.devider, self.output)

    def number_port_connected(self):

        print self.number.port_name(), 'connected'

    @staticmethod
    def get_category():
        return 'Math'

    def number_port_disconnected(self):

        print self.number.port_name(), 'disconnected'

    def devider_port_connected(self):

        print self.devider.port_name(), 'connected'

    def devider_port_disconnected(self):

        print self.devider.port_name(), 'disconnected'

    def compute(self):

        number = self.number.get_data()
        devider = self.devider.get_data()
        try:
            result = number / float(devider)
            self.output.set_data(result, False)
        except Exception, e:
            print e
